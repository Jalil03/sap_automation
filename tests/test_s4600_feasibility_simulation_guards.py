"""Offline flags only: never call any SAP function."""
import unittest
from types import SimpleNamespace
from scripts.simulate_s4600_ex27_32_billing_no_commit import require_simulation_only

def fake_function(testrun,posting):
    return SimpleNamespace(Exports=[SimpleNamespace(Name='TESTRUN',Value=testrun),SimpleNamespace(Name='POSTING',Value=posting)])

class SimulationGuardTests(unittest.TestCase):
    def test_simulation_flags_allowed(self):require_simulation_only(fake_function('X',''))
    def test_real_run_rejected(self):
        with self.assertRaises(RuntimeError):require_simulation_only(fake_function('',''))
    def test_posting_rejected_even_with_testrun(self):
        with self.assertRaises(RuntimeError):require_simulation_only(fake_function('X','X'))
    def test_missing_flags_fail_closed(self):
        with self.assertRaises(RuntimeError):require_simulation_only(fake_function(None,None))

if __name__=='__main__':unittest.main()
