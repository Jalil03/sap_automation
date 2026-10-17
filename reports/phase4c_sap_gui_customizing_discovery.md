# Phase 4C — SAP GUI customizing discovery

## Outcome

The generic, fail-closed `NAVIGATE` contract is implemented and validated offline. No SAP write, field change, generic Enter, `sendVKey(0)`, Save, or transport action is exposed by the filesystem request protocol.

Live discovery is **PAUSED_PENDING_RUNNER_RESTART**. The current Windows runner must be restarted manually to load the corrected tree-label extraction before the filesystem-only agent loop can continue.

## Live evidence retained

The latest successful, sanitized `INSPECT` evidence confirms:

- system/client/user: `A4H / 600 / ABDELJ`
- transaction: `SIMG`
- window title: `Afficher guide d'implémentation`
- tree control: `/app/con[0]/ses[0]/wnd[0]/usr/cntlTREE_CONTROL_CONTAINER/shellcont/shell`
- tree type/subtype: `GuiShell / Tree`
- node keys: observed
- node labels before this fix: empty

The empty labels were not replaced by visual assumptions. The corrected inspector first calls `GetNodeTextByKey(key)`. If that native call is unavailable, fails, or returns no text, it uses `GetColumnNames()` plus `GetItemText(key, observed_column)` only when both native column-tree APIs are exposed. Otherwise it returns `text: null` and a structured `extraction_error`.

## READ-only navigation contract

`NAVIGATE` accepts only these hard-coded operations:

- `PRESS_SAFE_BUTTON`
- `SELECT_TREE_NODE`
- `EXPAND_TREE_NODE`
- `COLLAPSE_TREE_NODE`
- `DOUBLE_CLICK_TREE_NODE`
- `OPEN_IMG_ACTIVITY`
- `SELECT_TAB`
- `FOCUS_CONTROL`
- `BACK`

Every request must carry the exact observed `control_id`, `expected_type`, `expected_text` (nullable only when unavailable), and `navigation_operation`; tree operations additionally require `node_key`. The runner re-reads the live control and refuses any ID, type, text, node, or SAP identity mismatch.

The blocklist is applied before navigation to the control text, node text, tooltip, window title, and status-bar context. It includes Save/Sauvegarder/Enregistrer, Create/Créer, New Entries/Nouvelles entrées, Change/Modifier, Delete/Supprimer, Release/Libérer, Transport, Copy/Copier, and Activate/Activer. The protocol rejects `SET_TEXT`, `SEND_VKEY_0`, and every operation outside the explicit allowlist.

One read-only exception is pinned to the fully observed company-code activity only: transaction `SIMG`, the exact IMG tree control, node key `05  4      3`, exact text `Traiter, copier, supprimer, contrôler société`, and operation `SELECT_TREE_NODE` or `DOUBLE_CLICK_TREE_NODE`. It does not permit any button press, field modification, copy, delete, create, save, or transport action.

`INSPECT` now reports visible control types and tree controls with bounded node key/text enumeration. This supports the controlled loop:

`INSPECT → read response JSON → NAVIGATE → read response JSON → INSPECT`

## Automated discovery bundle

`scripts/run_phase4c_live_discovery.py` implements this loop as a filesystem-protocol client. It has no SAP COM import or direct session access. It validates `A4H/600/ABDELJ`, uses only observed controls and tree nodes, re-inspects after every navigation, records sanitized evidence, and fails closed on identity mismatches, ambiguous nodes, unexpected popups, transport prompts, rejected requests, or pre-existing output that would require an unsafe resume.

IMG paths are resolved hierarchically. Each node now carries its observed order, level, and parent key. A native parent API is used only when it returns an actually observed key; otherwise the relationship is reconstructed deterministically from the observed key level and tree order. Every path step searches only the direct children of the current parent. Duplicate labels in other branches are therefore valid, while duplicate direct children remain blocking. Resolution diagnostics, including all candidate children and the selected key, are written to `discovery_steps.jsonl`.

On an explicit script rerun, the previous output bundle is preserved under `runtime/sap_discovery/phase4c/history/` before the new run starts. The current SAP state is always revalidated with `STATUS` and `INSPECT`; an existing `SIMG` screen is reused when valid.

The script was not executed live by Codex. The user must start it manually while the separately launched local runner is active.

## Customizing discovery matrix

Only actually observed facts are reported. The five target activities have not yet been reached with the new navigation loop.

| Object | Actually observed path | Transaction | View/table | Final screen reached | Automation possibility | First write-producing control | Transport observable |
|---|---|---|---|---|---|---|---|
| Company Code `1010` | `SPRO` → `Guide de référence SAP` → IMG root; deeper path `NOT_OBSERVED` | `SIMG` | `NOT_OBSERVED` | `Afficher guide d'implémentation` | READ navigation possible after manual runner restart and label-bearing INSPECT | `NOT_OBSERVED` | `NOT_OBSERVED` |
| Sales Organization `1010` | `SPRO` → `Guide de référence SAP` → IMG root; deeper path `NOT_OBSERVED` | `SIMG` | `NOT_OBSERVED` | `Afficher guide d'implémentation` | READ navigation possible after manual runner restart and label-bearing INSPECT | `NOT_OBSERVED` | `NOT_OBSERVED` |
| Sales Organization → Company Code | `SPRO` → `Guide de référence SAP` → IMG root; deeper path `NOT_OBSERVED` | `SIMG` | `NOT_OBSERVED` | `Afficher guide d'implémentation` | READ navigation possible after manual runner restart and label-bearing INSPECT | `NOT_OBSERVED` | `NOT_OBSERVED` |
| Distribution Channel assignment | `SPRO` → `Guide de référence SAP` → IMG root; deeper path `NOT_OBSERVED` | `SIMG` | `NOT_OBSERVED` | `Afficher guide d'implémentation` | READ navigation possible after manual runner restart and label-bearing INSPECT | `NOT_OBSERVED` | `NOT_OBSERVED` |
| Division assignment / sales area `1010/10/00` | `SPRO` → `Guide de référence SAP` → IMG root; deeper path `NOT_OBSERVED` | `SIMG` | `NOT_OBSERVED` | `Afficher guide d'implémentation` | READ navigation possible after manual runner restart and label-bearing INSPECT | `NOT_OBSERVED` | `NOT_OBSERVED` |

## Stop policy

Discovery stops before interacting with any screen or control whose live text, tooltip, title, or status context indicates creation, change, deletion, copy, activation, save, release, or transport. At that boundary, only an `INSPECT` response may be retained; no field or value is modified.

## Robust navigation-effect verification

The latest user-supplied live evidence resolves the Company Code IMG path through the exact leaf `05  4      3`, but shows that `DoubleClickNode` left transaction `SIMG`, program `SAPLSHI01`, and the IMG window unchanged. That attempt is therefore classified as `NO_OBSERVED_EFFECT`; it is not treated as an opened activity and does not prove whether Company Code `1010` exists. The corresponding evidence values remain `UNKNOWN`. The observed ADV expansion without a state or descendant change is classified the same way.

Every navigation now captures an `INSPECT` snapshot before and after the native call and records transaction/program/window changes, new windows, user-area signature changes, tree disappearance, node counts, descendant counts, new node keys, and expanded/selected-state changes. `EXPAND_TREE_NODE` succeeds only after an observed expanded-state or descendant increase. `OPEN_IMG_ACTIVITY` succeeds only after an observed screen transition.

Tree inspection records only protected, actually exposed native capabilities and metadata: columns, item type/text/tooltip/icon, node type, folder state, children, selected node, and focused item. `OPEN_IMG_ACTIVITY` uses `DoubleClickItem(node_key, observed_column)` when `DoubleClickItem` is exposed and exactly one observed item column carries the verified node label. It otherwise uses exposed `DoubleClickNode(node_key)`. If neither choice is unambiguous, it fails closed. The actual method available and effective in A4H remains subject to the next manual live run.

Generic `GuiMenu` entries in the unchanged `SIMG / SAPLSHI01 / Afficher guide d'implÃ©mentation` context are excluded from write-boundary and transport detection. A boundary must come from the active target screen, such as a non-menu New Entries/Create/Copy/Save control, a changeable business field/table, or a transport popup. Targets are processed independently after non-global blockers; identity and popup safety failures still stop globally.

## Validation

- Targeted SAP GUI/discovery tests: **70 passed**.
- Full repository suite: **276 passed**.
- Live SAP writes: **0**.
- Live `NAVIGATE` operations in this update: **0**.
- SAP Script Recorder usage: **none**.

## Continuation gate

The user must manually restart the local runner so it imports the updated source, then manually launch `scripts/run_phase4c_live_discovery.py`. The orchestrator will issue a fresh `INSPECT` and will only construct `NAVIGATE` requests from labels, keys, types, and control IDs present in those responses. No key is copied from the pre-fix blank-label evidence except the explicitly approved company-code tuple above.

## Phase 5 implementation follow-up — assignment LOOKUP

Later Phase 4C captures reached the three assignment maintenance tables. Their exact live-observed contracts are retained in:

- `runtime/sap_discovery/phase4c/snapshots/031_sales_org_company_assignment.json`
- `runtime/sap_discovery/phase4c/snapshots/043_distribution_channel_assignment.json`
- `runtime/sap_discovery/phase4c/snapshots/055_division_assignment.json`

The captures identify transaction `SIMG`, program `SAPLCUST_ASSIGN_SD`, the three exact table IDs and their code-field IDs. Captured table sizes were 52, 79, and 71 rows respectively; runtime lookup reads the current SAP-reported row count and scans via the table scrollbar instead of relying on those captured counts. The observed IMG path is `Structure de l'entreprise` → `Affectation` → `Administration des ventes (ADV)`, with exact activity keys `05  4      1`, `05  4      2`, and `05  4      3`.

Phase 5 now implements tuple LOOKUP and existence READBACK for these assignments. Provisioning remains blocked because no captured add-row/write transition or deterministic save-and-transport outcome establishes how a missing assignment may be created. No customer or product SAP GUI lookup/readback screen contract is present in the retained evidence; those operations remain fail-closed.
