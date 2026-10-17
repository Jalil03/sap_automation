"""Filesystem-only Phase 4C SAP IMG discovery orchestration."""

from __future__ import annotations

import json
import re
import unicodedata
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

from .protocol import enqueue_request, wait_for_response


EXPECTED_SAP = {"system": "A4H", "client": "600", "user": "ABDELJ"}
TREE_CONTROL_ID = "/app/con[0]/ses[0]/wnd[0]/usr/cntlTREE_CONTROL_CONTAINER/shellcont/shell"
COMPANY_CODE_LEAF = {
    "text": "Traiter, copier, supprimer, contrôler société",
}
SALES_ORGANIZATION_LEAF_TEXT = "Définir, copier, supprimer, contrôler org. commerciale"
ASSIGNMENT_LEAF_TEXTS = {
    "sales_org_company_assignment": "Affecter organisation commerciale à société",
    "distribution_channel_assignment": "Affecter canal de distribution à organisation commerciale",
    "division_assignment": "Affecter secteur d'activité à organisation commerciale",
}
TARGET_ORDER = (
    "company_code",
    "sales_organization",
    "sales_org_company_assignment",
    "distribution_channel_assignment",
    "division_assignment",
)
WRITE_TERMS = {
    "save",
    "sauvegarder",
    "enregistrer",
    "create",
    "creer",
    "new entries",
    "nouvelles entrees",
    "change",
    "modifier",
    "delete",
    "supprimer",
    "copy",
    "copier",
    "activate",
    "activer",
    "release",
    "liberer",
}
TRANSPORT_TERMS = {"transport", "ordre de transport", "demande de transport"}
SENSITIVE_KEYS = {"password", "authorization", "cookie", "token", "secret"}


class DiscoveryBlocked(RuntimeError):
    pass


class GlobalDiscoveryBlocked(DiscoveryBlocked):
    pass


class NavigationNoObservedEffect(DiscoveryBlocked):
    pass


class FilesystemRunnerClient:
    """Client of the JSON request/response protocol; never imports SAP COM code."""

    def exchange(
        self,
        action: str,
        params: dict[str, Any] | None = None,
        timeout_seconds: float = 60.0,
    ) -> tuple[str, dict[str, Any]]:
        queued = enqueue_request(action, params or {})
        request_id = queued["request_id"]
        return request_id, wait_for_response(request_id, timeout_seconds=timeout_seconds)


def _normalized(value: Any) -> str:
    decomposed = unicodedata.normalize("NFKD", str(value or ""))
    return "".join(char for char in decomposed if not unicodedata.combining(char)).casefold()


def _normalized_label(value: Any) -> str:
    return _normalized(value).replace("org.", "organisation")


def _observed_exact_text(
    observed: Any,
    expected: str,
    *,
    allow_trailing_colon: bool = False,
) -> bool:
    """Compare exact labels while tolerating COM's U+FFFD accent substitution."""

    actual = _normalized(observed).strip()
    wanted = _normalized(expected).strip()
    if allow_trailing_colon:
        actual = actual.rstrip(" :")
    pattern = re.escape(actual).replace("\ufffd", ".")
    return re.fullmatch(pattern, wanted) is not None


def _sanitize(value: Any) -> Any:
    if isinstance(value, dict):
        clean = {}
        for key, item in value.items():
            if any(term in str(key).casefold() for term in SENSITIVE_KEYS):
                clean[key] = "<redacted>"
            else:
                clean[key] = _sanitize(item)
        return clean
    if isinstance(value, list):
        return [_sanitize(item) for item in value]
    return value


def _all_text(value: Any) -> list[str]:
    texts: list[str] = []
    if isinstance(value, dict):
        for key, item in value.items():
            if key in {"text", "tooltip", "window_title", "message", "id"} and item:
                texts.append(str(item))
            texts.extend(_all_text(item))
    elif isinstance(value, list):
        for item in value:
            texts.extend(_all_text(item))
    return texts


class Phase4CDiscovery:
    def __init__(
        self,
        client: Any,
        output_dir: Path,
        *,
        now: Callable[[], datetime] | None = None,
        archive_existing: bool = False,
    ) -> None:
        self.client = client
        self.output_dir = Path(output_dir)
        self.snapshots_dir = self.output_dir / "snapshots"
        self.steps_path = self.output_dir / "discovery_steps.jsonl"
        self.summary_path = self.output_dir / "discovery_summary.json"
        self.report_path = self.output_dir / "discovery_report.md"
        self.now = now or (lambda: datetime.now(timezone.utc))
        self.archive_existing = archive_existing
        self.current_screen: dict[str, Any] | None = None
        self.step_number = 0
        self.summary: dict[str, Any] = {
            "sap": dict(EXPECTED_SAP),
            "status": "PARTIAL",
            "targets": {
                target: {
                    "status": "BLOCKED",
                    "img_path": [],
                    "blocker": "not processed",
                }
                for target in TARGET_ORDER
            },
            "next_write_required": None,
            "blockers": [],
        }

    def _prepare_outputs(self) -> None:
        existing = [
            path
            for path in (self.steps_path, self.summary_path, self.report_path)
            if path.exists()
        ]
        if self.snapshots_dir.exists() and any(self.snapshots_dir.iterdir()):
            existing.append(self.snapshots_dir)
        if existing:
            if not self.archive_existing:
                raise DiscoveryBlocked(
                    "resume is not supported; Phase 4C output already exists: "
                    + ", ".join(str(path) for path in existing)
                )
            archive = self.output_dir / "history" / self.now().strftime("%Y%m%dT%H%M%S%fZ")
            archive.mkdir(parents=True, exist_ok=False)
            for path in existing:
                path.replace(archive / path.name)
        self.snapshots_dir.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def _screen(snapshot: dict[str, Any] | None) -> dict[str, Any] | None:
        if snapshot is None:
            return None
        return {
            "transaction": snapshot.get("transaction"),
            "program": snapshot.get("program"),
            "window_title": snapshot.get("window_title"),
            "status_bar": snapshot.get("status_bar"),
        }

    def _write_step(self, payload: dict[str, Any]) -> None:
        with self.steps_path.open("a", encoding="utf-8") as stream:
            stream.write(json.dumps(_sanitize(payload), ensure_ascii=False, sort_keys=True) + "\n")

    def _exchange(
        self,
        action: str,
        params: dict[str, Any] | None,
        target: str,
        decision: str,
    ) -> dict[str, Any]:
        before = self._screen(self.current_screen)
        request_id = "NOT_CREATED"
        response: dict[str, Any]
        try:
            request_id, response = self.client.exchange(action, params or {})
        except Exception as exc:
            self._write_step(
                {
                    "timestamp": self.now().isoformat(),
                    "request_id": request_id,
                    "action": action,
                    "screen_before": before,
                    "target": target,
                    "response_status": "ERROR",
                    "screen_after": None,
                    "decision": decision,
                    "stop_reason": f"runner exchange failed ({type(exc).__name__})",
                }
            )
            raise DiscoveryBlocked(f"runner exchange failed for {action}") from exc

        clean_response = _sanitize(response)
        result = clean_response.get("result")
        after_snapshot = result if isinstance(result, dict) and "transaction" in result else None
        if after_snapshot is not None:
            self.current_screen = after_snapshot
        self._write_step(
            {
                "timestamp": self.now().isoformat(),
                "request_id": request_id,
                "action": action,
                "screen_before": before,
                "target": target,
                "response_status": clean_response.get("status"),
                "screen_after": self._screen(after_snapshot),
                "decision": decision,
                "stop_reason": None if clean_response.get("status") == "SUCCESS" else clean_response.get("error"),
                "navigation_outcome": result.get("navigation_outcome") if isinstance(result, dict) else None,
                "navigation_effect": result.get("navigation_effect") if isinstance(result, dict) else None,
                "img_activity_open": result.get("img_activity_open") if isinstance(result, dict) else None,
            }
        )
        if clean_response.get("status") != "SUCCESS":
            raise DiscoveryBlocked(
                f"runner rejected {action}: {clean_response.get('error')}"
            )
        return clean_response

    def _save_snapshot(self, target: str, snapshot: dict[str, Any]) -> None:
        self.step_number += 1
        path = self.snapshots_dir / f"{self.step_number:03d}_{target}.json"
        path.write_text(
            json.dumps(_sanitize(snapshot), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )

    def _inspect(self, target: str, decision: str) -> dict[str, Any]:
        response = self._exchange("INSPECT", {}, target, decision)
        snapshot = response["result"]
        self._save_snapshot(target, snapshot)
        self._assert_no_popup(snapshot)
        return snapshot

    def _assert_no_popup(self, snapshot: dict[str, Any]) -> None:
        popups = snapshot.get("popups") or []
        if not popups:
            return
        text = " ".join(_all_text(popups))
        normalized = _normalized(text)
        if any(term in normalized for term in TRANSPORT_TERMS):
            raise GlobalDiscoveryBlocked("transport popup detected")
        raise GlobalDiscoveryBlocked("unexpected popup detected")

    def _validate_identity(self, response: dict[str, Any]) -> None:
        observed = response.get("sap") or response.get("result") or {}
        actual = {
            "system": str(observed.get("system", "")).upper(),
            "client": str(observed.get("client", "")),
            "user": str(observed.get("user", "")).upper(),
        }
        if actual != EXPECTED_SAP:
            raise GlobalDiscoveryBlocked(
                f"SAP identity mismatch: expected {EXPECTED_SAP}, got {actual}"
            )

    @staticmethod
    def _tree(snapshot: dict[str, Any]) -> dict[str, Any]:
        trees = [
            tree
            for tree in snapshot.get("tree_controls", [])
            if tree.get("id") == TREE_CONTROL_ID
            and tree.get("type") == "GuiShell"
            and str(tree.get("subtype", "")).casefold() == "tree"
        ]
        if len(trees) != 1:
            raise DiscoveryBlocked(f"expected exactly one observed SAP IMG tree; found {len(trees)}")
        return trees[0]

    @staticmethod
    def _children(tree: dict[str, Any], parent_key: str | None) -> list[dict[str, Any]]:
        return [
            node
            for node in tree.get("nodes", [])
            if node.get("parent_key") == parent_key
        ]

    @staticmethod
    def _node_by_key(tree: dict[str, Any], key: str) -> dict[str, Any]:
        matches = [node for node in tree.get("nodes", []) if node.get("key") == key]
        if len(matches) != 1:
            raise DiscoveryBlocked(f"observed parent node {key!r} is missing or duplicated")
        return matches[0]

    def _record_resolution(
        self,
        target: str,
        requested_text: str,
        parent_key: str | None,
        parent_text: str | None,
        candidates: list[dict[str, Any]],
        selected: dict[str, Any] | None,
        resolution: str,
        stop_reason: str | None = None,
    ) -> None:
        self._write_step(
            {
                "timestamp": self.now().isoformat(),
                "request_id": None,
                "action": "RESOLVE_IMG_NODE",
                "screen_before": self._screen(self.current_screen),
                "target": target,
                "response_status": "SUCCESS" if selected else "BLOCKED",
                "screen_after": self._screen(self.current_screen),
                "decision": "resolve observed IMG direct child",
                "stop_reason": stop_reason,
                "requested_text": requested_text,
                "parent_key": parent_key,
                "parent_text": parent_text,
                "candidate_children": [
                    {
                        "key": node.get("key"),
                        "text": node.get("text"),
                        "level": node.get("level"),
                        "parent_key": node.get("parent_key"),
                    }
                    for node in candidates
                ],
                "selected_key": selected.get("key") if selected else None,
                "resolution": resolution,
            }
        )

    def _resolve_direct_child(
        self,
        target: str,
        tree: dict[str, Any],
        parent_key: str | None,
        requested_text: str,
    ) -> dict[str, Any]:
        parent_text = (
            self._node_by_key(tree, parent_key).get("text") if parent_key is not None else None
        )
        candidates = self._children(tree, parent_key)
        matches = [node for node in candidates if node.get("text") == requested_text]
        if len(matches) != 1:
            reason = (
                f"expected one direct child {requested_text!r} under "
                f"{parent_text!r}/{parent_key!r}; found {len(matches)}"
            )
            self._record_resolution(
                target,
                requested_text,
                parent_key,
                parent_text,
                candidates,
                None,
                "DIRECT_CHILD",
                reason,
            )
            raise DiscoveryBlocked(reason)
        selected = matches[0]
        self._record_resolution(
            target,
            requested_text,
            parent_key,
            parent_text,
            candidates,
            selected,
            "DIRECT_CHILD",
        )
        return selected

    def _path_start_parent(
        self,
        target: str,
        tree: dict[str, Any],
        requested_text: str,
    ) -> str | None:
        roots = self._children(tree, None)
        root_matches = [node for node in roots if node.get("text") == requested_text]
        if len(root_matches) == 1:
            return None
        child_matches: list[dict[str, Any]] = []
        for root in roots:
            child_matches.extend(
                node
                for node in self._children(tree, root.get("key"))
                if node.get("text") == requested_text
            )
        if len(child_matches) == 1:
            return child_matches[0].get("parent_key")
        reason = (
            f"cannot establish a unique observed hierarchy root for {requested_text!r}; "
            f"root_matches={len(root_matches)}, direct_root_children={len(child_matches)}"
        )
        self._record_resolution(
            target,
            requested_text,
            None,
            None,
            roots,
            None,
            "DIRECT_CHILD",
            reason,
        )
        raise DiscoveryBlocked(reason)

    def _resolve_semantic_descendant_path(
        self,
        target: str,
        tree: dict[str, Any],
        parent_key: str,
        required_terms: tuple[str, ...],
        excluded_terms: tuple[str, ...] = (),
    ) -> list[dict[str, Any]]:
        by_key = {node.get("key"): node for node in tree.get("nodes", [])}

        def is_descendant(node: dict[str, Any]) -> bool:
            seen = set()
            current = node.get("parent_key")
            while current is not None and current not in seen:
                if current == parent_key:
                    return True
                seen.add(current)
                current = (by_key.get(current) or {}).get("parent_key")
            return False

        matches = []
        for node in tree.get("nodes", []):
            text = node.get("text")
            if not text or not is_descendant(node):
                continue
            normalized = _normalized(text)
            if all(term in normalized for term in required_terms) and not any(
                term in normalized for term in excluded_terms
            ):
                matches.append(node)
        if len(matches) != 1:
            reason = (
                "semantic descendant selection is ambiguous or absent below observed parent "
                f"{parent_key!r}: required={required_terms}, excluded={excluded_terms}, "
                f"observed={[node.get('text') for node in matches]}"
            )
            parent_text = self._node_by_key(tree, parent_key).get("text")
            self._record_resolution(
                target,
                " & ".join(required_terms),
                parent_key,
                parent_text,
                matches,
                None,
                "OBSERVED_SUBTREE_MATCH",
                reason,
            )
            raise DiscoveryBlocked(reason)

        chain = []
        current = matches[0]
        while current.get("parent_key") != parent_key:
            chain.append(current)
            current = by_key.get(current.get("parent_key"))
            if current is None:
                raise DiscoveryBlocked("broken observed parent chain while resolving semantic descendant")
        chain.append(current)
        chain.reverse()
        return chain

    def _resolve_semantic_branch(
        self,
        target: str,
        snapshot: dict[str, Any],
        parent_key: str,
        required_terms: tuple[str, ...],
        excluded_terms: tuple[str, ...] = (),
        max_depth: int = 4,
    ) -> tuple[dict[str, Any], list[dict[str, Any]]]:
        matches: list[list[dict[str, Any]]] = []
        observed: list[dict[str, Any]] = []
        visited: set[str] = set()

        def matches_terms(node: dict[str, Any]) -> bool:
            normalized = _normalized_label(node.get("text"))
            return bool(normalized) and all(
                _normalized_label(term) in normalized for term in required_terms
            ) and not any(
                _normalized_label(term) in normalized for term in excluded_terms
            )

        def walk(
            current: dict[str, Any],
            current_parent: str,
            depth: int,
            path: list[dict[str, Any]],
        ) -> dict[str, Any]:
            tree = self._tree(current)
            children = self._children(tree, current_parent)
            observed.extend(
                {
                    "key": child.get("key"),
                    "text": child.get("text"),
                    "parent_key": child.get("parent_key"),
                }
                for child in children
            )
            for child in children:
                child_path = path + [child]
                if matches_terms(child):
                    matches.append(child_path)

            if depth >= max_depth:
                return current

            for child in children:
                key = child.get("key")
                if not key or key in visited:
                    continue
                if matches_terms(child):
                    continue
                tree = self._tree(current)
                refreshed = self._node_by_key(tree, key)
                loaded_children = self._children(tree, key)
                node_type = _normalized(refreshed.get("node_type"))
                is_folder = (
                    refreshed.get("expandable") is True
                    or bool(loaded_children)
                    or "folder" in node_type
                )
                if not is_folder:
                    continue
                visited.add(key)
                if not loaded_children:
                    current = self._expand_node(target, current, refreshed)
                current = walk(
                    current,
                    key,
                    depth + 1,
                    path + [refreshed],
                )
            return current

        snapshot = walk(snapshot, parent_key, 0, [])
        if len(matches) != 1:
            reason = (
                "semantic recursive selection is ambiguous or absent below observed parent "
                f"{parent_key!r}: required={required_terms}, excluded={excluded_terms}, "
                f"matches={[path[-1].get('text') for path in matches]}, "
                f"observed={[item.get('text') for item in observed]}"
            )
            tree = self._tree(snapshot)
            parent_text = self._node_by_key(tree, parent_key).get("text")
            self._record_resolution(
                target,
                " & ".join(required_terms),
                parent_key,
                parent_text,
                observed,
                None,
                "RECURSIVE_OBSERVED_BRANCH",
                reason,
            )
            raise DiscoveryBlocked(reason)
        return snapshot, matches[0]

    def _resolve_preferred_leaf(
        self,
        target: str,
        snapshot: dict[str, Any],
        parent_key: str,
        exact_text: str,
        required_terms: tuple[str, ...],
        excluded_terms: tuple[str, ...] = (),
    ) -> tuple[dict[str, Any], list[dict[str, Any]]]:
        tree = self._tree(snapshot)
        children = self._children(tree, parent_key)
        exact = [child for child in children if child.get("text") == exact_text]
        if len(exact) > 1:
            raise DiscoveryBlocked(
                f"multiple exact direct children {exact_text!r} below {parent_key!r}"
            )
        if len(exact) == 1:
            selected = exact[0]
            self._record_resolution(
                target,
                exact_text,
                parent_key,
                self._node_by_key(tree, parent_key).get("text"),
                children,
                selected,
                "EXACT_DIRECT_CHILD",
            )
            return snapshot, [selected]

        normalized_expected = _normalized_label(exact_text)
        normalized = [
            child
            for child in children
            if _normalized_label(child.get("text")) == normalized_expected
        ]
        if len(normalized) > 1:
            raise DiscoveryBlocked(
                f"multiple normalized exact direct children {exact_text!r} below {parent_key!r}"
            )
        if len(normalized) == 1:
            selected = normalized[0]
            self._record_resolution(
                target,
                exact_text,
                parent_key,
                self._node_by_key(tree, parent_key).get("text"),
                children,
                selected,
                "NORMALIZED_EXACT_DIRECT_CHILD",
            )
            return snapshot, [selected]

        return self._resolve_semantic_branch(
            target,
            snapshot,
            parent_key,
            required_terms,
            excluded_terms,
            max_depth=4,
        )

    def _navigate_node(
        self,
        target: str,
        snapshot: dict[str, Any],
        node: dict[str, Any],
        operation: str,
        *,
        require_effect: bool = True,
        item_column: str | None = None,
    ) -> dict[str, Any]:
        tree = self._tree(snapshot)
        if not node.get("key") or not node.get("text"):
            raise DiscoveryBlocked("tree navigation requires an observed key and non-empty text")
        params = {
            "control_id": tree["id"],
            "expected_type": tree["type"],
            "expected_text": node["text"],
            "navigation_operation": operation,
            "node_key": node["key"],
        }
        if operation == "OPEN_IMG_ACTIVITY":
            params["expected_transaction"] = "SIMG"
            if item_column is not None:
                params["item_column"] = item_column
        response = self._exchange(
            "NAVIGATE",
            params,
            target,
            f"{operation} using observed node {node['text']!r}/{node['key']!r}",
        )
        snapshot = response.get("result")
        if not isinstance(snapshot, dict) or "transaction" not in snapshot:
            raise DiscoveryBlocked("NAVIGATE did not return a post-action INSPECT snapshot")
        self._save_snapshot(target, snapshot)
        if operation == "OPEN_IMG_ACTIVITY":
            popup_text = _normalized(" ".join(_all_text(snapshot.get("popups") or [])))
            if any(term in popup_text for term in TRANSPORT_TERMS):
                self._assert_no_popup(snapshot)
        else:
            self._assert_no_popup(snapshot)
        if snapshot.get("navigation_outcome") not in {"SUCCESS", "ALREADY_EXPANDED"} and require_effect:
            raise NavigationNoObservedEffect(
                f"{operation} returned NO_OBSERVED_EFFECT for {node['text']!r}/{node['key']!r}"
            )
        return snapshot

    def _expand_node(self, target: str, snapshot: dict[str, Any], node: dict[str, Any]) -> dict[str, Any]:
        tree = self._tree(snapshot)
        direct_children = self._children(tree, node["key"])
        if direct_children or node.get("children_count"):
            self._write_step(
                {
                    "timestamp": self.now().isoformat(),
                    "request_id": None,
                    "action": "EXPAND_TREE_NODE",
                    "screen_before": self._screen(snapshot),
                    "target": target,
                    "response_status": "SUCCESS",
                    "screen_after": self._screen(snapshot),
                    "decision": "skip ExpandNode because direct children are already loaded",
                    "stop_reason": None,
                    "navigation_outcome": "ALREADY_EXPANDED",
                    "navigation_effect": {
                        "observed": True,
                        "already_expanded": True,
                        "direct_child_count": len(direct_children)
                        if direct_children
                        else node.get("children_count"),
                    },
                }
            )
            return snapshot
        first = self._navigate_node(
            target, snapshot, node, "EXPAND_TREE_NODE", require_effect=False
        )
        if first.get("navigation_outcome") in {"SUCCESS", "ALREADY_EXPANDED"}:
            return self._inspect_after_expand(target, node)

        tree = self._tree(first)
        refreshed = self._node_by_key(tree, node["key"])
        if refreshed.get("selected") is not True:
            selected = self._navigate_node(
                target, first, refreshed, "SELECT_TREE_NODE", require_effect=False
            )
            first = selected
            tree = self._tree(first)
            refreshed = self._node_by_key(tree, node["key"])

        second = self._navigate_node(
            target, first, refreshed, "EXPAND_TREE_NODE", require_effect=False
        )
        if second.get("navigation_outcome") in {"SUCCESS", "ALREADY_EXPANDED"}:
            return self._inspect_after_expand(target, node)

        tree = self._tree(second)
        refreshed = self._node_by_key(tree, node["key"])
        if (
            refreshed.get("expandable") is True
            and "DoubleClickNode" in set(tree.get("native_capabilities", []))
        ):
            alternative = self._navigate_node(
                target,
                second,
                refreshed,
                "DOUBLE_CLICK_TREE_NODE",
                require_effect=False,
            )
            if alternative.get("navigation_outcome") == "SUCCESS":
                return self._inspect_after_expand(target, node)
        raise NavigationNoObservedEffect(
            f"EXPAND_TREE_NODE returned NO_OBSERVED_EFFECT after safe observed alternatives for {node['text']!r}/{node['key']!r}"
        )

    def _inspect_after_expand(
        self,
        target: str,
        node: dict[str, Any],
    ) -> dict[str, Any]:
        fresh = self._inspect(target, "fresh INSPECT after successful tree expansion")
        tree = self._tree(fresh)
        refreshed = self._node_by_key(tree, node["key"])
        children = self._children(tree, refreshed["key"])
        self._write_step(
            {
                "timestamp": self.now().isoformat(),
                "request_id": None,
                "action": "OBSERVE_DIRECT_CHILDREN",
                "screen_before": self._screen(fresh),
                "target": target,
                "response_status": "SUCCESS",
                "screen_after": self._screen(fresh),
                "decision": "resolve exclusively from fresh post-expand INSPECT",
                "stop_reason": None,
                "parent_key": refreshed["key"],
                "parent_text": refreshed.get("text"),
                "children": [
                    {
                        "key": child.get("key"),
                        "text": child.get("text"),
                        "parent_key": child.get("parent_key"),
                    }
                    for child in children
                ],
            }
        )
        return fresh

    @staticmethod
    def _is_maintenance_destination(snapshot: dict[str, Any]) -> bool:
        program = str(snapshot.get("program") or "").upper()
        title = _normalized(snapshot.get("window_title"))
        img_tree_present = any(tree.get("id") == TREE_CONTROL_ID for tree in snapshot.get("tree_controls", []))
        return not img_tree_present and (
            program == "SAPLSVIM"
            or "maintenance" in title
            or "vue de customizing" in title
            or bool(snapshot.get("tables"))
            or bool(snapshot.get("input_fields"))
        )

    @staticmethod
    def _is_documentation_destination(snapshot: dict[str, Any]) -> bool:
        if str(snapshot.get("program") or "").upper() == "SAPMSSY0":
            return True
        text = _normalized(
            " ".join(
                filter(
                    None,
                    [
                        str(snapshot.get("window_title") or ""),
                        str(snapshot.get("program") or ""),
                        " ".join(_all_text(snapshot.get("popups") or [])),
                    ],
                )
            )
        )
        return any(
            term in text
            for term in (
                "documentation",
                "information",
                "afficher hypertexte",
                "hypertexte",
                "aide",
                "help",
                "docu",
            )
        )

    @staticmethod
    def _is_secondary_documentation_info(snapshot: dict[str, Any]) -> bool:
        popups = snapshot.get("popups") or []
        return (
            str(snapshot.get("transaction") or "").upper() == "SIMG"
            and str(snapshot.get("program") or "").upper() == "SAPLDSYH"
            and len(popups) == 1
            and popups[0].get("id") == "/app/con[0]/ses[0]/wnd[1]"
            and not _observed_exact_text(
                popups[0].get("window_title"),
                "Sélection de l'activité",
                allow_trailing_colon=True,
            )
        )

    @staticmethod
    def _is_img_activity_selection_dialog_container(snapshot: dict[str, Any]) -> bool:
        popups = snapshot.get("popups") or []
        return (
            str(snapshot.get("transaction") or "").upper() == "SIMG"
            and str(snapshot.get("program") or "").upper() == "SAPLDSYH"
            and len(popups) == 1
            and popups[0].get("id") == "/app/con[0]/ses[0]/wnd[1]"
            and _observed_exact_text(
                popups[0].get("window_title"),
                "Sélection de l'activité",
                allow_trailing_colon=True,
            )
        )

    @classmethod
    def _is_img_activity_selection_dialog(cls, snapshot: dict[str, Any]) -> bool:
        if not cls._is_img_activity_selection_dialog_container(snapshot):
            return False
        popups = snapshot.get("popups") or []
        observed = _all_text(popups[0])
        return all(
            any(_observed_exact_text(value, expected) for value in observed)
            for expected in {
            "Copier, supprimer, contrôler société",
            "Traiter données société",
            "Sélectionner",
            }
        )

    @staticmethod
    def _legacy_sales_organization_activity_options(snapshot: dict[str, Any]) -> list[str]:
        popups = snapshot.get("popups") or []
        if not popups:
            return []
        options = []
        for value in _all_text(popups[0]):
            normalized = _normalized_label(value)
            if (
                normalized.startswith("traiter")
                and "organisation commerciale" in normalized
                and not any(term in normalized for term in ("copier", "supprimer", "contr"))
                and value not in options
            ):
                options.append(value)
        return options

    @staticmethod
    def _sales_organization_activity_options(snapshot: dict[str, Any]) -> list[str]:
        """Return rows from the exact observed SAPLDSYHTCODES table only."""
        popups = snapshot.get("popups") or []
        if len(popups) != 1:
            return []
        table_id = "/app/con[0]/ses[0]/wnd[1]/usr/tblSAPLDSYHTCODES"
        tables = [
            table for table in popups[0].get("tables") or []
            if table.get("id") == table_id
        ]
        if len(tables) != 1:
            return []
        return [
            str(value["text"])
            for row in tables[0].get("visible_rows") or []
            for value in row.get("values") or []
            if value.get("text")
        ]

    def _select_company_code_activity(
        self,
        target: str,
        snapshot: dict[str, Any],
    ) -> dict[str, Any]:
        if target != "company_code" or not self._is_img_activity_selection_dialog(snapshot):
            raise DiscoveryBlocked(
                "IMG activity-selection dialog is not the exact company-code context"
            )
        response = self._exchange(
            "SELECT_COMPANY_CODE_ACTIVITY",
            {
                "source": "OPEN_IMG_ACTIVITY",
                "target": "company_code",
                "window_id": "/app/con[0]/ses[0]/wnd[1]",
                "expected_transaction": "SIMG",
                "expected_program": "SAPLDSYH",
                "row_text": "Traiter données société",
                "button_text": "Sélectionner",
            },
            target,
            "select exact read-only company-code display activity",
        )
        opened = response.get("result")
        if not isinstance(opened, dict):
            raise DiscoveryBlocked(
                "company-code activity selection returned no readable screen"
            )
        self._save_snapshot(target, opened)
        self._assert_no_popup(opened)
        return opened

    def _select_sales_organization_activity(
        self,
        target: str,
        snapshot: dict[str, Any],
    ) -> dict[str, Any]:
        if (
            target != "sales_organization"
            or not self._is_img_activity_selection_dialog_container(snapshot)
        ):
            raise DiscoveryBlocked(
                "IMG activity-selection dialog is not the Sales Organization context"
            )
        options = self._sales_organization_activity_options(snapshot)
        row_text = "D\u00e9finir l'organisation commerciale"
        forbidden = "Contr\u00f4ler, supprimer, copier l'organisation commerciale"
        if not (
            sum(_observed_exact_text(value, row_text) for value in options) == 1
            and sum(_observed_exact_text(value, forbidden) for value in options) == 1
        ):
            raise DiscoveryBlocked(
                "Sales Organization activity selection is ambiguous; observed options="
                + json.dumps(options, ensure_ascii=False)
            )
        response = self._exchange(
            "SELECT_SALES_ORGANIZATION_ACTIVITY",
            {
                "source": "OPEN_IMG_ACTIVITY",
                "target": "sales_organization",
                "window_id": "/app/con[0]/ses[0]/wnd[1]",
                "expected_transaction": "SIMG",
                "expected_program": "SAPLDSYH",
                "table_id": "/app/con[0]/ses[0]/wnd[1]/usr/tblSAPLDSYHTCODES",
                "row_text": row_text,
                "button_id": "/app/con[0]/ses[0]/wnd[1]/tbar[0]/btn[2]",
                "button_text": "Sélectionner",
            },
            target,
            "select exact observed non-copy Sales Organization processing activity",
        )
        opened = response.get("result")
        if not isinstance(opened, dict):
            raise DiscoveryBlocked(
                "Sales Organization activity selection returned no readable screen"
            )
        self._save_snapshot(target, opened)
        self._assert_no_popup(opened)
        return opened

    def _find_company_code_1010(
        self,
        target: str,
        snapshot: dict[str, Any],
    ) -> dict[str, Any]:
        table_id = "/app/con[0]/ses[0]/wnd[0]/usr/tblSAPL0ORGTCTRL_V_T001"
        matches = [
            table
            for table in snapshot.get("tables") or []
            if table.get("id") == table_id
        ]
        if not (
            target == "company_code"
            and str(snapshot.get("transaction") or "").upper() == "V_T001"
            and str(snapshot.get("program") or "").upper() == "SAPL0ORG"
            and len(matches) == 1
        ):
            return snapshot
        response = self._exchange(
            "FIND_TABLE_VALUE",
            {
                "transaction": "V_T001",
                "program": "SAPL0ORG",
                "table_id": table_id,
                "column": "BUKRS",
                "value": "1010",
            },
            target,
            "read every observable Company Code row using only the vertical scrollbar",
        )
        searched = response.get("result")
        if not isinstance(searched, dict):
            raise DiscoveryBlocked("FIND_TABLE_VALUE returned no readable screen")
        self._save_snapshot(target, searched)
        self._assert_no_popup(searched)
        return searched

    def _close_secondary_documentation_info(
        self,
        target: str,
        snapshot: dict[str, Any],
    ) -> dict[str, Any]:
        if not self._is_secondary_documentation_info(snapshot):
            raise DiscoveryBlocked(
                "IMG secondary documentation/info context is not exactly verified"
            )
        response = self._exchange(
            "CLOSE_IMG_INFO_POPUP",
            {
                "source": "OPEN_IMG_ACTIVITY",
                "window_id": "/app/con[0]/ses[0]/wnd[1]",
                "expected_transaction": "SIMG",
                "expected_program": "SAPLDSYH",
            },
            target,
            "close observed read-only SAPLDSYH documentation/info window",
        )
        restored = response.get("result")
        if not isinstance(restored, dict):
            raise DiscoveryBlocked("closing IMG information window returned no readable screen")
        self._save_snapshot(target, restored)
        self._assert_no_popup(restored)
        self._tree(restored)
        if (
            str(restored.get("program") or "").upper() != "SAPLSHI01"
            or _normalized(restored.get("window_title"))
            != "afficher guide d'implementation"
        ):
            raise DiscoveryBlocked(
                "closing IMG information window did not return to SAPLSHI01 / Afficher guide d'implémentation"
            )
        return restored

    def _back_to_img(self, target: str, snapshot: dict[str, Any]) -> dict[str, Any]:
        response = self._exchange(
            "BACK",
            {},
            target,
            "return from read-only documentation/information destination",
        )
        restored = response.get("result")
        if not isinstance(restored, dict):
            raise DiscoveryBlocked("BACK from IMG documentation returned no readable screen")
        self._save_snapshot(target, restored)
        self._assert_no_popup(restored)
        self._tree(restored)
        if (
            str(restored.get("program") or "").upper() != "SAPLSHI01"
            or _normalized(restored.get("window_title"))
            != "afficher guide d'implementation"
        ):
            raise DiscoveryBlocked(
                "BACK from IMG documentation did not return to SAPLSHI01 / Afficher guide d'implémentation"
            )
        return restored

    def _open_img_activity(
        self,
        target: str,
        snapshot: dict[str, Any],
        leaf: dict[str, Any],
    ) -> dict[str, Any]:
        items = list(leaf.get("items") or [])
        type_5 = [item for item in items if str(item.get("type") or "") == "5"]
        type_4 = [item for item in items if str(item.get("type") or "") == "4"]
        candidates = type_5 or type_4
        if not candidates:
            raise DiscoveryBlocked(
                "OPEN_IMG_ACTIVITY has no observed type 5 link or type 4 button column"
            )

        current = snapshot
        for item in candidates:
            column = item.get("column")
            if not isinstance(column, str) or not column:
                raise DiscoveryBlocked("OPEN_IMG_ACTIVITY observed an invalid item column")
            opened = self._navigate_node(
                target,
                current,
                leaf,
                "OPEN_IMG_ACTIVITY",
                require_effect=False,
                item_column=column,
            )
            if opened.get("navigation_outcome") == "NO_OBSERVED_EFFECT":
                current = opened
                continue
            if self._is_maintenance_destination(opened):
                return opened
            if self._is_img_activity_selection_dialog_container(opened):
                if target == "company_code":
                    return self._select_company_code_activity(target, opened)
                if target == "sales_organization":
                    return self._select_sales_organization_activity(target, opened)
                raise DiscoveryBlocked(
                    "IMG activity-selection dialog is not allowlisted for this target"
                )
            if self._is_secondary_documentation_info(opened):
                current = self._close_secondary_documentation_info(target, opened)
                tree = self._tree(current)
                leaf = self._node_by_key(tree, leaf["key"])
                continue
            if self._is_documentation_destination(opened):
                current = self._back_to_img(target, opened)
                tree = self._tree(current)
                leaf = self._node_by_key(tree, leaf["key"])
                continue
            raise DiscoveryBlocked(
                f"OPEN_IMG_ACTIVITY reached an unknown destination from column {column!r}"
            )
        raise NavigationNoObservedEffect(
            "OPEN_IMG_ACTIVITY returned NO_OBSERVED_EFFECT for all observed type 5/4 columns"
        )

    def _ensure_img(self, target: str) -> dict[str, Any]:
        status = self._exchange("STATUS", {}, target, "verify SAP identity and transaction")
        self._validate_identity(status)
        transaction = str((status.get("sap") or status.get("result") or {}).get("transaction", "")).upper()
        if transaction == "SIMG":
            current = self._inspect(target, "inspect current SIMG screen")
            try:
                self._tree(current)
            except DiscoveryBlocked:
                transaction = "NOT_IMG_ROOT"
            else:
                return current
        if transaction != "SIMG":
            if transaction != "SPRO":
                opened = self._exchange(
                    "OPEN_TRANSACTION",
                    {"transaction": "SPRO"},
                    target,
                    "open allowlisted SPRO transaction",
                )
                self._validate_identity(opened)
            spro = self._inspect(target, "inspect SPRO before opening IMG")
            matches = [
                button
                for button in spro.get("buttons", [])
                if button.get("type") == "GuiButton"
                and button.get("text") == "Guide de référence SAP"
            ]
            if len(matches) != 1:
                raise DiscoveryBlocked(
                    f"expected one observed IMG reference button; found {len(matches)}"
                )
            button = matches[0]
            self._exchange(
                "NAVIGATE",
                {
                    "control_id": button["id"],
                    "expected_type": button["type"],
                    "expected_text": button["text"],
                    "navigation_operation": "PRESS_SAFE_BUTTON",
                },
                target,
                "open SAP implementation guide using observed button",
            )
        snapshot = self._inspect(target, "inspect SAP IMG root")
        if str(snapshot.get("transaction", "")).upper() != "SIMG":
            raise DiscoveryBlocked("SAP IMG did not open in transaction SIMG")
        self._tree(snapshot)
        return snapshot

    def _expand_exact_path(
        self,
        target: str,
        snapshot: dict[str, Any],
        labels: tuple[str, ...],
    ) -> tuple[dict[str, Any], list[dict[str, Any]]]:
        path: list[dict[str, Any]] = []
        tree = self._tree(snapshot)
        parent_key = self._path_start_parent(target, tree, labels[0])
        for label in labels:
            tree = self._tree(snapshot)
            node = self._resolve_direct_child(target, tree, parent_key, label)
            path.append({"key": node["key"], "text": node["text"]})
            if node.get("expanded") is not True:
                snapshot = self._expand_node(target, snapshot, node)
            parent_key = node["key"]
        return snapshot, path

    @staticmethod
    def _write_boundary(snapshot: dict[str, Any]) -> dict[str, Any] | None:
        if (
            str(snapshot.get("transaction", "")).upper() == "SIMG"
            and snapshot.get("program") == "SAPLSHI01"
            and snapshot.get("window_title") == "Afficher guide d'implÃ©mentation"
        ):
            return None
        candidates = []
        for section in ("buttons", "labels"):
            for control in snapshot.get(section, []) or []:
                if control.get("type") == "GuiMenu":
                    continue
                text = " ".join(
                    str(value) for value in (control.get("text"), control.get("tooltip")) if value
                )
                normalized = _normalized(text)
                if any(term in normalized for term in WRITE_TERMS | TRANSPORT_TERMS):
                    candidates.append(
                        {"id": control.get("id"), "type": control.get("type"), "text": text}
                    )
        for section in ("input_fields", "tables"):
            for control in snapshot.get(section, []) or []:
                if control.get("changeable") is True:
                    candidates.append(
                        {
                            "id": control.get("id"),
                            "type": control.get("type"),
                            "text": control.get("text"),
                        }
                    )
        title = str(snapshot.get("window_title") or "")
        if any(term in _normalized(title) for term in WRITE_TERMS | TRANSPORT_TERMS):
            candidates.append({"id": "wnd[0]", "type": "window", "text": title})
        if not candidates:
            return None
        return {"reason": "write-capable controls or context observed", "controls": candidates}

    @staticmethod
    def _classify_company_code_table_search(snapshot: dict[str, Any]) -> dict[str, Any]:
        """Classify a completed V_T001 scan against SAP's authoritative entry total."""
        table_search = dict(snapshot.get("table_value_search") or {})
        if not table_search:
            return table_search
        position_info_id = "/app/con[0]/ses[0]/wnd[0]/usr/txtVIM_POSITION_INFO"
        totals = []
        for field in snapshot.get("input_fields") or []:
            if field.get("id") != position_info_id:
                continue
            match = re.search(r"/\s*(\d+)\s*$", str(field.get("text") or ""))
            if match:
                totals.append(int(match.group(1)))
        sap_total_entries = totals[0] if len(totals) == 1 else None
        # FIND_TABLE_VALUE's rows_read is the size of its absolute-row map and
        # is therefore already deduplicated.  A future producer may make that
        # explicit with unique_rows_read; raw row_count is never completeness.
        unique_rows_read = table_search.get(
            "unique_rows_read", table_search.get("rows_read")
        )
        try:
            unique_rows_read = int(unique_rows_read)
        except (TypeError, ValueError):
            unique_rows_read = None
        table_search["sap_total_entries"] = sap_total_entries
        table_search["unique_rows_read"] = unique_rows_read

        target_found = (
            table_search.get("result") == "FOUND"
            or table_search.get("found_row") is not None
        )
        if target_found:
            table_search["result"] = "FOUND"
        elif (
            sap_total_entries is not None
            and unique_rows_read is not None
            and unique_rows_read >= sap_total_entries
        ):
            table_search["result"] = "CONFIRMED_NOT_FOUND"
            table_search["reason"] = (
                f"target absent after {unique_rows_read} unique BUKRS rows; "
                f"SAP reports {sap_total_entries} total entries"
            )
        else:
            table_search["result"] = "UNKNOWN"
        return table_search

    @staticmethod
    def _screen_evidence(snapshot: dict[str, Any]) -> dict[str, Any]:
        text_values = _all_text(snapshot)
        table_search = Phase4CDiscovery._classify_company_code_table_search(snapshot)
        in_img_guide = (
            str(snapshot.get("transaction", "")).upper() == "SIMG"
            and snapshot.get("program") == "SAPLSHI01"
            and snapshot.get("window_title") == "Afficher guide d'implÃ©mentation"
        )
        contextual_text = " ".join(
            str(value)
            for section in ("buttons", "labels", "input_fields", "tables", "popups")
            for control in snapshot.get(section, []) or []
            if control.get("type") != "GuiMenu"
            for value in (control.get("text"), control.get("tooltip"), control.get("window_title"))
            if value
        )
        return {
            "transaction": snapshot.get("transaction"),
            "program": snapshot.get("program"),
            "window_title": snapshot.get("window_title"),
            "view_or_table": [
                {
                    "id": table.get("id"),
                    "text": table.get("text"),
                    "visible_rows": table.get("visible_rows") or [],
                }
                for table in snapshot.get("tables", []) or []
            ],
            "buttons": [
                {"id": button.get("id"), "text": button.get("text"), "tooltip": button.get("tooltip")}
                for button in snapshot.get("buttons", []) or []
            ],
            "fields": snapshot.get("input_fields", []),
            "value_1010_observed": (
                table_search.get("result")
                if table_search.get("result")
                in {"FOUND", "CONFIRMED_NOT_FOUND", "UNKNOWN"}
                else (
                    "UNKNOWN"
                    if in_img_guide
                    else (
                        "EXISTS"
                        if any(text.strip() == "1010" for text in text_values)
                        else "UNKNOWN"
                    )
                )
            ),
            "table_value_search": table_search or None,
            "transport_observed": (
                "UNKNOWN"
                if in_img_guide
                else (
                    "YES"
                    if any(term in _normalized(contextual_text) for term in TRANSPORT_TERMS)
                    else "UNKNOWN"
                )
            ),
        }

    def _discover_target(self, target: str) -> None:
        snapshot = self._ensure_img(target)
        if target in {"company_code", "sales_organization"}:
            parent_labels = (
                "Structure de l'entreprise",
                "Définition",
                "Comptabilité financière" if target == "company_code" else "Administration des ventes (ADV)",
            )
        else:
            parent_labels = ("Structure de l'entreprise", "Affectation")
        snapshot, path = self._expand_exact_path(target, snapshot, parent_labels)
        tree = self._tree(snapshot)
        parent_key = path[-1]["key"]

        if target == "company_code":
            leaf = self._resolve_direct_child(
                target, tree, parent_key, COMPANY_CODE_LEAF["text"]
            )
        elif target == "sales_organization":
            snapshot, leaf_chain = self._resolve_preferred_leaf(
                target,
                snapshot,
                parent_key,
                SALES_ORGANIZATION_LEAF_TEXT,
                ("definir", "organisation commerciale"),
                ("affect", "societe", "canal", "secteur"),
            )
        else:
            assignment_children = self._children(tree, parent_key)
            adv_matches = [
                child
                for child in assignment_children
                if child.get("text") == "Administration des ventes (ADV)"
            ]
            if len(adv_matches) > 1:
                raise DiscoveryBlocked(
                    "multiple exact Administration des ventes (ADV) nodes observed under Affectation"
                )
            if len(adv_matches) == 1:
                adv = adv_matches[0]
                if adv.get("expanded") is not True:
                    snapshot = self._expand_node(target, snapshot, adv)
                path.append({"key": adv["key"], "text": adv["text"]})
                parent_key = adv["key"]

            if target == "sales_org_company_assignment":
                required_terms = ("organisation commerciale", "societe")
            elif target == "distribution_channel_assignment":
                required_terms = (
                    "canal de distribution",
                    "organisation commerciale",
                )
            else:
                required_terms = (
                    "secteur d'activite",
                    "organisation commerciale",
                )
            snapshot, leaf_chain = self._resolve_preferred_leaf(
                target,
                snapshot,
                parent_key,
                ASSIGNMENT_LEAF_TEXTS[target],
                required_terms,
            )

        if target != "company_code":
            for index, observed_node in enumerate(leaf_chain):
                tree = self._tree(snapshot)
                leaf = self._resolve_direct_child(
                    target,
                    tree,
                    parent_key,
                    observed_node["text"],
                )
                is_leaf = index == len(leaf_chain) - 1
                if not is_leaf and leaf.get("expanded") is not True:
                    snapshot = self._expand_node(target, snapshot, leaf)
                if not is_leaf:
                    path.append({"key": leaf["key"], "text": leaf["text"]})
                    parent_key = leaf["key"]

        path.append({"key": leaf["key"], "text": leaf["text"]})
        target_state = self.summary["targets"][target]
        target_state["img_path"] = path
        target_state["node"] = {"key": leaf["key"], "text": leaf["text"]}

        snapshot = self._open_img_activity(target, snapshot, leaf)
        if target == "company_code":
            snapshot = self._find_company_code_1010(target, snapshot)
        evidence = self._screen_evidence(snapshot)
        boundary = self._write_boundary(snapshot)
        target_state["evidence"] = evidence
        target_state["first_write_action"] = boundary
        target_state["blocker"] = None
        if target == "company_code":
            if evidence["value_1010_observed"] in {"EXISTS", "FOUND"}:
                target_state["status"] = "FOUND"
            elif evidence["value_1010_observed"] == "CONFIRMED_NOT_FOUND":
                target_state["status"] = "DISCOVERED"
            else:
                target_state["status"] = "BLOCKED"
                target_state["blocker"] = "1010 presence/absence is not deterministically visible"
        elif target == "sales_organization":
            target_state["status"] = (
                "FOUND"
                if evidence["value_1010_observed"] == "EXISTS"
                else "DISCOVERED"
            )
        else:
            target_state["status"] = "DISCOVERED"
        if boundary and self.summary["next_write_required"] is None:
            self.summary["next_write_required"] = {
                "target": target,
                **boundary,
            }

    def _write_outputs(self) -> None:
        self.summary_path.write_text(
            json.dumps(_sanitize(self.summary), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        lines = [
            "# Phase 4C live customizing discovery",
            "",
            f"Status: **{self.summary['status']}**",
            "",
            "| Target | Status | Observed IMG path | Transaction | View/table | First write boundary |",
            "|---|---|---|---|---|---|",
        ]
        for name in TARGET_ORDER:
            target = self.summary["targets"][name]
            path = " → ".join(item["text"] for item in target.get("img_path", [])) or "NOT_OBSERVED"
            evidence = target.get("evidence") or {}
            tables = evidence.get("view_or_table") or []
            table_text = ", ".join(item.get("text") or item.get("id") or "" for item in tables) or "NOT_OBSERVED"
            boundary = target.get("first_write_action")
            lines.append(
                f"| {name} | {target.get('status')} | {path} | {evidence.get('transaction') or 'NOT_OBSERVED'} | {table_text} | {boundary.get('reason') if boundary else 'NOT_OBSERVED'} |"
            )
        lines.extend(
            [
                "",
                "## Blockers",
                "",
                *([f"- {item}" for item in self.summary["blockers"]] or ["- None"]),
                "",
                "## Future provisioning order",
                "",
                "Company Code → Sales Organization → Sales Org/Company assignment → Distribution Channel assignment → Division/Sales Area assignment.",
                "",
                "No SAP value was created, changed, copied, deleted, saved, released, or transported.",
            ]
        )
        self.report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    def run(self) -> dict[str, Any]:
        self._prepare_outputs()
        try:
            initial = self._exchange("STATUS", {}, "bootstrap", "validate SAP identity")
            self._validate_identity(initial)
            for target in TARGET_ORDER:
                try:
                    self._discover_target(target)
                except GlobalDiscoveryBlocked:
                    raise
                except DiscoveryBlocked as exc:
                    target_state = self.summary["targets"][target]
                    target_state["status"] = "BLOCKED"
                    target_state["blocker"] = str(exc)
                    self.summary["blockers"].append(f"{target}: {exc}")
            target_statuses = [self.summary["targets"][name]["status"] for name in TARGET_ORDER]
            if all(status == "DISCOVERED" for status in target_statuses):
                self.summary["status"] = "COMPLETE_READY_FOR_PREPARE"
            elif (
                self.summary["targets"]["company_code"]["status"] in {"FOUND", "MISSING"}
                and self.summary["targets"]["sales_organization"]["status"] in {"FOUND", "DISCOVERED"}
                and all(
                    self.summary["targets"][name]["status"] == "DISCOVERED"
                    for name in TARGET_ORDER[2:]
                )
            ):
                self.summary["status"] = "COMPLETE/PARTIAL_READY_FOR_PREPARE"
            elif all(status in {"FOUND", "MISSING", "DISCOVERED"} for status in target_statuses):
                self.summary["status"] = "SUCCESS"
            elif all(status == "BLOCKED" for status in target_statuses):
                self.summary["status"] = "BLOCKED"
            else:
                self.summary["status"] = "PARTIAL"
        except DiscoveryBlocked as exc:
            processed = any(
                self.summary["targets"][name].get("blocker") != "not processed"
                or self.summary["targets"][name].get("img_path")
                for name in TARGET_ORDER
            )
            self.summary["status"] = "PARTIAL" if processed else "BLOCKED"
            self.summary["blockers"].append(str(exc))
        self._write_outputs()
        return self.summary


def compact_summary(summary: dict[str, Any], output_dir: Path) -> str:
    labels = {
        "company_code": "Company Code",
        "sales_organization": "Sales Organization",
        "sales_org_company_assignment": "Sales Org → Company",
        "distribution_channel_assignment": "Distribution Channel assignment",
        "division_assignment": "Division assignment",
    }
    lines = ["PHASE 4C LIVE DISCOVERY", ""]
    for key in TARGET_ORDER:
        lines.append(f"{labels[key]}: {summary['targets'][key]['status']}")
    next_write = summary.get("next_write_required")
    lines.extend(
        [
            "",
            "Next write required:",
            next_write.get("reason") if next_write else "NOT_DETERMINED",
            "",
            "Outputs:",
            str(Path(output_dir) / "discovery_summary.json"),
            str(Path(output_dir) / "discovery_report.md"),
            str(Path(output_dir) / "discovery_steps.jsonl"),
            str(Path(output_dir) / "snapshots"),
        ]
    )
    return "\n".join(lines)
