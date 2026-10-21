"""Offline gates for autonomous training execution; no SAP access."""

import tempfile
import unittest
from pathlib import Path

from src.provisioning.execution_policy import ExecutionCheckpoint, TrainingExecutionPolicy, target_fingerprint
from src.provisioning.phase5 import Phase5ProvisioningEngine, ProvisioningResult, RecoverableReadError


ENV = {"system": "A4H", "client": "600", "user": "ABDELJ"}


def policy_document(mode="AUTONOMOUS_TRAINING"):
    return {
        "mode": mode,
        "workflow_id": "TRAINING_TEST",
        "environment": ENV,
        "approval": {
            "workflow_id": "TRAINING_TEST", "environment": ENV,
            "approved_by": "EXPLICIT_TEST_APPROVER",
            "authorization_evidence": "TEST_FIXTURE_ONLY",
            "operations": ["TRAINING_CUSTOMER", "ORG_ASSIGNMENT"],
            "scopes": ["TRAINING_MASTER_DATA", "ORG_CUSTOMIZING"],
            "target_fingerprints": {
                "TRAINING_CUSTOMER": target_fingerprint(
                    "TRAINING_CUSTOMER", {"customer": "TRAINING"}, {"name": "Training"}),
                "ORG_ASSIGNMENT": target_fingerprint(
                    "ORG_ASSIGNMENT", {"org": "TRAINING"}, {"org": "TRAINING"}),
            },
        },
        "operation_scopes": {
            "TRAINING_CUSTOMER": "TRAINING_MASTER_DATA",
            "ORG_ASSIGNMENT": "ORG_CUSTOMIZING",
        },
        "route_evidence": {
            "TRAINING_CUSTOMER": "tested exact mocked adapter contract",
            "ORG_ASSIGNMENT": "tested exact mocked adapter contract",
        },
        "sensitive_approvals": {},
    }


class FakeBackend:
    writable = True

    def __init__(self, *, write_result=None, lookup_error_once=False):
        self.write_result = write_result or {"accepted": True}
        self.lookup_error_once = lookup_error_once
        self.calls = []

    def lookup(self, operation, target):
        self.calls.append(("lookup", operation))
        if self.lookup_error_once:
            self.lookup_error_once = False
            raise RecoverableReadError("temporary read failure before write")
        return "MISSING"

    def provision(self, operation, target, values):
        self.calls.append(("provision", operation))
        return self.write_result

    def readback(self, operation, target):
        self.calls.append(("readback", operation))
        return target


class ExecutionPolicyTests(unittest.TestCase):
    def test_first_write_needs_no_prior_success(self):
        policy = TrainingExecutionPolicy.from_document(policy_document("CONTROLLED_FIRST_WRITE"))
        policy.authorize("TRAINING_CUSTOMER", {"customer": "TRAINING"}, {"name": "Training"})

    def test_workflow_approval_reused_for_routine_steps(self):
        policy = TrainingExecutionPolicy.from_document(policy_document())
        policy.authorize("TRAINING_CUSTOMER", {"customer": "TRAINING"}, {"name": "Training"})
        policy.authorize("TRAINING_CUSTOMER", {"customer": "TRAINING"}, {"name": "Training"})

    def test_sensitive_change_needs_separate_exact_approval(self):
        document = policy_document()
        policy = TrainingExecutionPolicy.from_document(document)
        with self.assertRaisesRegex(ValueError, "Separate ORG_CUSTOMIZING approval"):
            policy.authorize("ORG_ASSIGNMENT", {"org": "TRAINING"}, {"org": "TRAINING"})
        document["sensitive_approvals"]["ORG_ASSIGNMENT"] = {
            "environment": ENV, "operation": "ORG_ASSIGNMENT",
            "scope": "ORG_CUSTOMIZING", "approved_by": "EXPLICIT_TEST_APPROVER",
            "authorization_evidence": "TEST_FIXTURE_ONLY",
        }
        TrainingExecutionPolicy.from_document(document).authorize(
            "ORG_ASSIGNMENT", {"org": "TRAINING"}, {"org": "TRAINING"})

    def test_wrong_identity_or_missing_route_fails_closed(self):
        document = policy_document()
        document["environment"] = {**ENV, "client": "100"}
        with self.assertRaisesRegex(ValueError, "A4H/600/ABDELJ"):
            TrainingExecutionPolicy.from_document(document)
        document = policy_document()
        document["route_evidence"] = {}
        with self.assertRaisesRegex(ValueError, "route missing"):
            TrainingExecutionPolicy.from_document(document).authorize(
                "TRAINING_CUSTOMER", {"customer": "TRAINING"}, {"name": "Training"})

    def test_approval_does_not_cover_changed_target_or_values(self):
        policy = TrainingExecutionPolicy.from_document(policy_document())
        with self.assertRaisesRegex(ValueError, "Scoped workflow approval missing"):
            policy.authorize("TRAINING_CUSTOMER", {"customer": "OTHER"}, {"name": "Training"})
        with self.assertRaisesRegex(ValueError, "Scoped workflow approval missing"):
            policy.authorize("TRAINING_CUSTOMER", {"customer": "TRAINING"}, {"name": "Other"})

    def test_checkpoint_blocks_ambiguous_retry_and_resumes(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "checkpoint.json"
            checkpoint = ExecutionCheckpoint(path, "TRAINING_TEST")
            checkpoint.before_write("TRAINING_CUSTOMER")
            reloaded = ExecutionCheckpoint(path, "TRAINING_TEST")
            with self.assertRaisesRegex(ValueError, "Prior ATTEMPTED"):
                reloaded.before_write("TRAINING_CUSTOMER")

    def test_engine_first_write_and_readback(self):
        with tempfile.TemporaryDirectory() as directory:
            backend = FakeBackend()
            checkpoint = ExecutionCheckpoint(Path(directory) / "checkpoint.json", "TRAINING_TEST")
            engine = Phase5ProvisioningEngine(
                backend=backend, decisions={"TRAINING_CUSTOMER": {"name": "Training"}},
                execute=True,
                execution_policy=TrainingExecutionPolicy.from_document(policy_document()),
                checkpoint=checkpoint,
            )
            result = engine.ensure_operation("TRAINING_CUSTOMER", {"customer": "TRAINING"}, ("name",))
            self.assertEqual("PROVISIONED_VERIFIED", result.status)
            self.assertEqual("VERIFIED", checkpoint.status("TRAINING_CUSTOMER"))
            self.assertEqual(["lookup", "provision", "readback"], [item[0] for item in backend.calls])

    def test_ambiguous_write_never_retried(self):
        with tempfile.TemporaryDirectory() as directory:
            backend = FakeBackend(write_result={"ambiguous_save": True})
            checkpoint = ExecutionCheckpoint(Path(directory) / "checkpoint.json", "TRAINING_TEST")
            engine = Phase5ProvisioningEngine(
                backend=backend, decisions={"TRAINING_CUSTOMER": {"name": "Training"}},
                execute=True,
                execution_policy=TrainingExecutionPolicy.from_document(policy_document()),
                checkpoint=checkpoint,
            )
            first = engine.ensure_operation("TRAINING_CUSTOMER", {"customer": "TRAINING"}, ("name",))
            second = engine.ensure_operation("TRAINING_CUSTOMER", {"customer": "TRAINING"}, ("name",))
            self.assertEqual("BLOCKED_AMBIGUOUS_SAVE", first.status)
            self.assertEqual("BLOCKED_APPROVAL_OR_ROUTE", second.status)
            self.assertEqual(1, sum(item[0] == "provision" for item in backend.calls))

    def test_certified_prewrite_read_error_retries_once(self):
        backend = FakeBackend(lookup_error_once=True)
        result = Phase5ProvisioningEngine(
            backend=backend, decisions={"TRAINING_CUSTOMER": {"name": "Training"}},
        ).ensure_operation("TRAINING_CUSTOMER", {"customer": "TRAINING"}, ("name",))
        self.assertEqual("WOULD_PROVISION", result.status)
        self.assertEqual(2, sum(item[0] == "lookup" for item in backend.calls))

    def test_blocked_branch_does_not_prevent_independent_approved_branch(self):
        with tempfile.TemporaryDirectory() as directory:
            backend = FakeBackend()
            checkpoint = ExecutionCheckpoint(Path(directory) / "checkpoint.json", "TRAINING_TEST")
            engine = Phase5ProvisioningEngine(
                backend=backend,
                decisions={
                    "ORG_ASSIGNMENT": {"org": "TRAINING"},
                    "TRAINING_CUSTOMER": {"name": "Training"},
                },
                execute=True,
                execution_policy=TrainingExecutionPolicy.from_document(policy_document()),
                checkpoint=checkpoint,
            )
            blocked = engine.ensure_operation("ORG_ASSIGNMENT", {"org": "TRAINING"}, ("org",))
            independent = engine.ensure_operation(
                "TRAINING_CUSTOMER", {"customer": "TRAINING"}, ("name",))
            self.assertEqual("BLOCKED_APPROVAL_OR_ROUTE", blocked.status)
            self.assertEqual("PROVISIONED_VERIFIED", independent.status)
            self.assertEqual(["TRAINING_CUSTOMER"], [item[1] for item in backend.calls if item[0] == "provision"])

    def test_execute_rejects_dry_run_dependency_as_proof(self):
        backend = FakeBackend()
        engine = Phase5ProvisioningEngine(backend=backend, execute=True)
        planned = ProvisioningResult("PARENT", {}, "MISSING", "PROVISION", "WOULD_PROVISION")
        result = engine.ensure_operation(
            "CHILD", {"child": "1"}, (), dependencies=[planned])
        self.assertEqual("BLOCKED_DEPENDENCY", result.status)
        self.assertFalse(any(item[0] == "provision" for item in backend.calls))


if __name__ == "__main__":
    unittest.main()
