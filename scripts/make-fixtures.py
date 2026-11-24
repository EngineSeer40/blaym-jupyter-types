#!/usr/bin/env python3
"""Writes fixtures/contracts/*.json.

The fixture files are the contract examples; this script only keeps the many
invalid cases (one per required field, one per integer minimum) consistent
with the valid examples. Run: python3 scripts/make-fixtures.py
"""
import copy
import json
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "fixtures" / "contracts"
UUIDS = iter(
    f"3f2b8c1e-5a7d-4e19-9c3b-1d2e4f6a{i:04x}" for i in range(1, 1000)
)


def env(type_, payload, tick=1, **extra):
    e = {
        "schemaVersion": 2,
        "eventId": next(UUIDS),
        "explorationId": "exploration-1",
        "branchId": "branch-main",
        "tick": tick,
        "wallTimeMs": 1760000000000 + tick,
        "userId": "local",
        "workspaceId": "local",
        "originId": "origin-1",
        "type": type_,
        "payload": payload,
    }
    e.update(extra)
    return e


ITEM = {
    "outputType": "stream",
    "mimeTypes": ["text/plain"],
    "contentHash": "sha256:ab12",
    "preview": "hello",
    "truncated": False,
    "sizeBytes": 5,
    "searchText": "hello",
}
CELL = {
    "cellId": "cell-1",
    "cellType": "code",
    "code": "print('hello')",
    "revision": 2,
    "metadata": {"tags": ["demo"]},
    "outputs": [{"runId": "run-1", "items": [ITEM]}],
    "runCount": 1,
}
SNAP = {
    "path": "analysis.ipynb",
    "notebookMetadata": {},
    "kernelName": "python3",
    "language": "python",
    "cells": [CELL],
}

EVENTS = {
    "notebook_snapshot": env("notebook_snapshot", SNAP, authorHint="blaym"),
    "cell_inserted": env(
        "cell_inserted",
        {
            "cellId": "cell-2",
            "index": 1,
            "cellType": "markdown",
            "code": "# Title",
            "revision": 1,
            "metadata": {},
        },
        2,
        authorHint="person",
        links={"cellId": "cell-2", "cellRevision": 1},
    ),
    "cell_deleted": env("cell_deleted", {"cellId": "cell-2"}, 3),
    "cell_moved": env(
        "cell_moved", {"cellId": "cell-2", "fromIndex": 1, "toIndex": 0}, 4
    ),
    "cell_type_changed": env(
        "cell_type_changed", {"cellId": "cell-2", "cellType": "raw"}, 5
    ),
    "cell_source_changed": env(
        "cell_source_changed",
        {"cellId": "cell-1", "revision": 3, "code": "print('hi')"},
        6,
        authorHint="ai",
        links={"chatTurnId": "turn-1", "cellId": "cell-1", "cellRevision": 3},
    ),
    "cell_metadata_changed": env(
        "cell_metadata_changed", {"cellId": "cell-1", "metadata": {"tags": []}}, 7
    ),
    "notebook_metadata_changed": env(
        "notebook_metadata_changed", {"metadata": {"title": "x"}}, 8
    ),
    "run_started": env(
        "run_started",
        {"runId": "run-2", "cellId": "cell-1", "cellRevision": 3, "runCount": 2},
        9,
        links={"runId": "run-2"},
    ),
    "run_finished": env(
        "run_finished", {"runId": "run-2", "status": "ok"}, 10
    ),
    "output_added": env(
        "output_added",
        {"runId": "run-2", "cellId": "cell-1", "outputIndex": 0, "item": ITEM},
        11,
    ),
    "output_replaced": env(
        "output_replaced",
        {"runId": "run-2", "cellId": "cell-1", "outputIndex": 0, "item": ITEM},
        12,
    ),
    "outputs_cleared": env(
        "outputs_cleared",
        {"runId": "run-2", "cellId": "cell-1", "wait": True},
        13,
    ),
    "kernel_started": env(
        "kernel_started",
        {"kernelId": "kernel-1", "kernelName": "python3", "language": "python"},
        14,
    ),
    "kernel_restarted": env(
        "kernel_restarted", {"kernelId": "kernel-1", "reason": "unknown"}, 15
    ),
    "notebook_renamed": env(
        "notebook_renamed",
        {"oldPath": "analysis.ipynb", "newPath": "analysis2.ipynb"},
        16,
    ),
    "notebook_copied": env(
        "notebook_copied",
        {
            "oldPath": "analysis.ipynb",
            "newPath": "copy.ipynb",
            "newExplorationId": "exploration-2",
        },
        17,
    ),
    "changed_outside_editor": env(
        "changed_outside_editor", SNAP, 18, authorHint="outside"
    ),
    "chat_message_added": env(
        "chat_message_added",
        {
            "chatSource": "jupyter-ai",
            "messageId": "msg-1",
            "sender": "persona-claude",
            "senderKind": "agent",
            "body": "Done.",
            "chatTimeMs": 1760000000500,
            "agentSessionId": "session-1",
        },
        19,
    ),
    "chat_message_updated": env(
        "chat_message_updated", {"chatSource": "jupyter-ai", "messageId": "msg-1", "body": "Done. More."}, 20
    ),
    "branch_point_created": env(
        "branch_point_created",
        {"parentBranchId": "branch-main", "parentTick": 6, "name": "try b"},
        21,
        branchId="branch-b",
    ),
    "recording_gap_started": env(
        "recording_gap_started",
        {"gapId": "gap-1", "source": "browser", "reason": "no_client"},
        22,
    ),
    "recording_gap_ended": env("recording_gap_ended", {"gapId": "gap-1"}, 23),
}

STATE = {
    "schemaVersion": 2,
    "position": {"branchId": "branch-main", "tick": 20, "lastEventTick": 20, "branchCount": 20},
    "notebook": {"path": "analysis.ipynb", "metadata": {}, "cells": [CELL]},
    "runs": [
        {
            "runId": "run-1",
            "cellId": "cell-1",
            "cellRevision": 2,
            "runCount": 1,
            "status": "unfinished",
            "startedTick": 5,
            "endedTick": 9,
        }
    ],
    "chat": [
        {
            "chatSource": "jupyter-ai",
            "messageId": "msg-1",
            "sender": "persona-claude",
            "senderKind": "agent",
            "body": "Done.",
            "chatTimeMs": 1760000000500,
            "agentSessionId": "session-1",
            "addedTick": 19,
        }
    ],
    "kernel": {
        "status": "running",
        "kernelId": "kernel-1",
        "kernelName": "python3",
        "language": "python",
        "lastRestart": {"kernelId": "kernel-1", "reason": "unknown", "tick": 15},
    },
    "gaps": [
        {
            "gapId": "gap-1",
            "source": "browser",
            "reason": "no_client",
            "startedTick": 12,
            "endedTick": 14,
        }
    ],
    "detachedOutputs": [copy.deepcopy(CELL["outputs"][0])],
    "lastOutsideChange": {"tick": 18},
}

RESULTS = {
    "ok": {"status": "ok", "state": STATE},
    "missing_events": {"status": "missing_events", "firstMissingTick": 7},
    "conflict": {
        "status": "conflict",
        "eventId": EVENTS["cell_deleted"]["eventId"],
        "first": EVENTS["cell_deleted"],
        "second": {
            **EVENTS["cell_deleted"],
            "payload": {"cellId": "cell-9"},
        },
    },
    "invalid_revision": {
        "status": "invalid_revision",
        "eventId": EVENTS["cell_source_changed"]["eventId"],
        "cellId": "cell-1",
        "expectedRevision": 3,
        "actualRevision": 5,
    },
    "unknown_cell": {
        "status": "unknown_cell",
        "eventId": EVENTS["cell_deleted"]["eventId"],
        "cellId": "cell-9",
    },
    "unknown_branch": {"status": "unknown_branch", "branchId": "branch-x"},
    "lineage_loop": {"status": "lineage_loop", "branchIds": ["a", "b"]},
    "invalid_event": {
        "status": "invalid_event",
        "eventId": EVENTS["cell_deleted"]["eventId"],
        "tick": 9,
        "reason": "unknown_run",
        "detail": "run_finished for a run that was never started",
    },
}
INVALID_EVENT_REASONS = [
    "first_event_not_snapshot", "tick_clash", "duplicate_id", "unknown_run",
    "run_not_running", "unknown_message", "unknown_gap", "gap_already_ended",
    "no_output_at_index", "index_out_of_range", "position_mismatch", "invalid_branch_point", "run_cell_mismatch",
]  # fmt: skip
RESULT_TYPES = {
    "ok": "RebuildOk",
    "missing_events": "RebuildMissingEvents",
    "conflict": "RebuildConflict",
    "invalid_revision": "RebuildInvalidRevision",
    "unknown_cell": "RebuildUnknownCell",
    "unknown_branch": "RebuildUnknownBranch",
    "lineage_loop": "RebuildLineageLoop",
    "invalid_event": "RebuildInvalidEvent",
}

# --- valid fixtures --------------------------------------------------------

valid = []
for t, v in EVENTS.items():
    valid.append({"name": f"event {t}", "contract": "BlaymEvent", "value": v})
for k, v in RESULTS.items():
    valid.append({"name": f"result {k}", "contract": "RebuildResult", "value": v})
    valid.append({"name": f"result type {k}", "contract": RESULT_TYPES[k], "value": v})
for r in INVALID_EVENT_REASONS:
    valid.append({"name": f"result invalid_event: {r}", "contract": "RebuildResult", "value": {**RESULTS["invalid_event"], "reason": r}})
for _t, _extra in (
    ("editor jupyterlab", {"editor": "jupyterlab"}),
    ("editor notebook7", {"editor": "notebook7"}),
    ("editor vscode", {"editor": "vscode"}),
    ("editor unknown", {"editor": "unknown"}),
    ("authorConfidence known", {"authorHint": "ai", "authorConfidence": "known"}),
    ("authorConfidence guess", {"authorHint": "ai", "authorConfidence": "guess"}),
):
    valid.append({"name": f"event cell_deleted with {_t}", "contract": "BlaymEvent", "value": {**EVENTS["cell_deleted"], **_extra}})
valid.append({"name": "event kernel_restarted: reason crash", "contract": "BlaymEvent", "value": {**EVENTS["kernel_restarted"], "payload": {"kernelId": "kernel-1", "reason": "crash"}}})
valid.append({"name": "event kernel_restarted: reason requested", "contract": "BlaymEvent", "value": {**EVENTS["kernel_restarted"], "payload": {"kernelId": "kernel-1", "reason": "requested"}}})
valid.append({"name": "event chat_message_added: another chatSource", "contract": "BlaymEvent", "value": {**EVENTS["chat_message_added"], "payload": {**EVENTS["chat_message_added"]["payload"], "chatSource": "vscode-copilot"}}})
valid.append({"name": "event recording_gap_started: reason source_closed", "contract": "BlaymEvent", "value": {**EVENTS["recording_gap_started"], "payload": {"gapId": "gap-1", "source": "chat", "reason": "source_closed"}}})
valid.append({"name": "event cell_inserted with outputs", "contract": "BlaymEvent", "value": {**EVENTS["cell_inserted"], "payload": {**EVENTS["cell_inserted"]["payload"], "outputs": [ITEM]}}})
for t, v in EVENTS.items():
    valid.append({"name": f"recorder event {t}", "contract": "RecorderEvent", "value": {k: x for k, x in v.items() if k not in ("tick", "branchId")}})
_pending = copy.deepcopy(STATE)
_pending["notebook"]["cells"][0]["outputs"][0]["clearPending"] = True
valid.append({"name": "state with clearPending", "contract": "RebuiltState", "value": _pending})
valid.append({"name": "state", "contract": "RebuiltState", "value": STATE})
MINIMAL_STATE = {
    "schemaVersion": 2,
    "position": {"branchId": "branch-main", "tick": 1, "lastEventTick": 1, "branchCount": 1},
    "notebook": {"path": "analysis.ipynb", "metadata": {}, "cells": []},
    "runs": [],
    "chat": [],
    "kernel": {"status": "unknown", "kernelName": "python3", "language": "python"},
    "gaps": [],
    "detachedOutputs": [],
}
valid.append({"name": "state minimal (empty lists, no optional fields)", "contract": "RebuiltState", "value": MINIMAL_STATE})

_det = copy.deepcopy(STATE)
_det["detachedOutputs"][0]["clearPending"] = True
valid.append({"name": "state with detached output pending clear", "contract": "RebuiltState", "value": _det})

# --- invalid fixtures ------------------------------------------------------

SKIP_INTO = {"metadata", "notebookMetadata"}  # free-form records


def optional(ctype, path):
    p = path.replace("first.", "", 1) if path.startswith(("first.", "second.")) else path
    if p in {"authorHint", "links"} and not (
        p == "authorHint" and ctype == "changed_outside_editor"
    ):
        return True
    if p.startswith("links."):
        return True
    if p.endswith("cells.runCount"):
        return True  # NotebookCell.runCount is optional
    return (ctype, p) in {
        ("cell_inserted", "payload.metadata"),
        ("chat_message_added", "payload.agentSessionId"),
    } or p.split(".")[-1] in {
        "searchText",
        "endedTick",
        "agentSessionId",
        "kernelId",
        "lastRestart",
        "lastOutsideChange",
    } and not (
        p.endswith("kernelId") and ctype in ("kernel_started", "kernel_restarted")
    ) and not (p == "kernelId" or p.endswith("lastRestart.kernelId"))


def walk(value, path, ctype, out):
    """Yield (path-as-list, key, is_required) for every dict key."""
    if isinstance(value, dict):
        t = value.get("type") if isinstance(value.get("type"), str) else ctype
        for k, v in value.items():
            p = f"{path}.{k}" if path else k
            if not optional(t, p):
                out.append((p.split("."), t))
            if k not in SKIP_INTO:
                walk(v, p, t, out)
    elif isinstance(value, list):
        for v in value:
            walk(v, path, ctype, out)


def drop(value, parts):
    v = copy.deepcopy(value)
    node = [v]
    for part in parts[:-1]:
        nxt = []
        for n in node:
            c = n[part]
            nxt.extend(c if isinstance(c, list) else [c])
        node = nxt
    for n in node:
        del n[parts[-1]]
    return v


invalid = []


def add_missing(label, contract, value):
    found = []
    walk(value, "", None, found)
    seen = set()
    for parts, _ in found:
        key = ".".join(parts)
        if key in seen:
            continue
        seen.add(key)
        invalid.append(
            {
                "name": f"{label}: missing {key}",
                "contract": contract,
                "value": drop(value, parts),
            }
        )


def setpath(value, parts, new):
    v = copy.deepcopy(value)
    node = v
    for part in parts[:-1]:
        node = node[part][0] if isinstance(node[part], list) else node[part]
    node[parts[-1]] = new
    return v


for t, v in EVENTS.items():
    add_missing(f"event {t}", "BlaymEvent", v)
for k in ("ok", "missing_events", "invalid_revision", "unknown_cell", "unknown_branch", "lineage_loop", "invalid_event"):
    add_missing(f"result {k}", "RebuildResult", RESULTS[k])
add_missing("state", "RebuiltState", STATE)

# Integer minimums: (label, contract, base value, path, below-minimum value)
MINS = []
for t, v in EVENTS.items():
    MINS += [
        (f"event {t}", "BlaymEvent", v, "tick", 0),
        (f"event {t}", "BlaymEvent", v, "tick", 1.5),
        (f"event {t}", "BlaymEvent", v, "wallTimeMs", -1),
        (f"event {t}", "BlaymEvent", v, "wallTimeMs", 1.5),
        (f"event {t}", "BlaymEvent", v, "schemaVersion", 1),
        (f"event {t}", "BlaymEvent", v, "schemaVersion", 3),
    ]
PAYLOAD_MINS = {
    "cell_inserted": ["index", "revision"],
    "cell_moved": ["fromIndex", "toIndex"],
    "cell_source_changed": ["revision"],
    "run_started": ["cellRevision", "runCount"],
    "output_added": ["outputIndex"],
    "output_replaced": ["outputIndex"],
    "chat_message_added": ["chatTimeMs"],
    "branch_point_created": ["parentTick"],
}
for t, names in PAYLOAD_MINS.items():
    for n in names:
        low = -1 if n in ("index", "fromIndex", "toIndex", "outputIndex", "chatTimeMs") else 0
        for bad in (low, 1.5):
            MINS.append((f"event {t}", "BlaymEvent", EVENTS[t], f"payload.{n}", bad))
for bad in (-1, 1.5):
    MINS.append(("event output_added", "BlaymEvent", EVENTS["output_added"], "payload.item.sizeBytes", bad))
for bad in (0, 1.5):
    MINS += [
        ("event notebook_snapshot", "BlaymEvent", EVENTS["notebook_snapshot"], "payload.cells.revision", bad),
        ("event notebook_snapshot", "BlaymEvent", EVENTS["notebook_snapshot"], "payload.cells.runCount", bad),
        ("event cell_source_changed", "BlaymEvent", EVENTS["cell_source_changed"], "links.cellRevision", bad),
    ]
    for p in ("position.tick", "position.lastEventTick", "position.branchCount", "runs.cellRevision", "runs.runCount", "runs.startedTick", "runs.endedTick", "chat.addedTick", "kernel.lastRestart.tick", "gaps.startedTick", "gaps.endedTick", "lastOutsideChange.tick", "notebook.cells.revision"):
        MINS.append(("state", "RebuiltState", STATE, p, bad))
for p in ("chat.chatTimeMs",):
    for bad in (-1, 1.5):
        MINS.append(("state", "RebuiltState", STATE, p, bad))
MINS.append(("result missing_events", "RebuildResult", RESULTS["missing_events"], "firstMissingTick", 0))
MINS.append(("result missing_events", "RebuildResult", RESULTS["missing_events"], "firstMissingTick", 1.5))
for bad in (0, 1.5):
    MINS.append(("result invalid_event", "RebuildResult", RESULTS["invalid_event"], "tick", bad))
for n in ("expectedRevision", "actualRevision"):
    for bad in (0, 1.5):
        MINS.append(("result invalid_revision", "RebuildResult", RESULTS["invalid_revision"], n, bad))

for label, contract, base, path, bad in MINS:
    parts = path.split(".")
    invalid.append(
        {
            "name": f"{label}: {path} = {bad}",
            "contract": contract,
            "value": setpath(base, parts, bad),
        }
    )

# Other invalid cases
extra = copy.deepcopy(EVENTS["cell_deleted"])
extra["extra"] = True
invalid.append({"name": "event cell_deleted: extra top-level key", "contract": "BlaymEvent", "value": extra})
extra = copy.deepcopy(EVENTS["cell_deleted"])
extra["payload"]["extra"] = True
invalid.append({"name": "event cell_deleted: extra payload key", "contract": "BlaymEvent", "value": extra})
bad = copy.deepcopy(EVENTS["cell_deleted"])
bad["eventId"] = "not-a-uuid"
invalid.append({"name": "event cell_deleted: eventId not a uuid", "contract": "BlaymEvent", "value": bad})
bad = copy.deepcopy(EVENTS["cell_deleted"])
bad["type"] = "cell_moved"
invalid.append({"name": "event: type does not match payload", "contract": "BlaymEvent", "value": bad})
bad = copy.deepcopy(EVENTS["cell_deleted"])
bad["type"] = "made_up"
invalid.append({"name": "event: unknown type", "contract": "BlaymEvent", "value": bad})
bad = copy.deepcopy(EVENTS["changed_outside_editor"])
bad["authorHint"] = "person"
invalid.append({"name": "event changed_outside_editor: authorHint not outside", "contract": "BlaymEvent", "value": bad})
bad = copy.deepcopy(EVENTS["run_finished"])
bad["payload"]["status"] = "running"
invalid.append({"name": "event run_finished: status running", "contract": "BlaymEvent", "value": bad})
bad = copy.deepcopy(EVENTS["recording_gap_started"])
bad["payload"]["source"] = "langgraph"
invalid.append({"name": "event recording_gap_started: unknown source", "contract": "BlaymEvent", "value": bad})
bad = copy.deepcopy(EVENTS["kernel_restarted"])
bad["payload"]["reason"] = "exploded"
invalid.append({"name": "event kernel_restarted: unknown reason", "contract": "BlaymEvent", "value": bad})
for _k, _v in (("editor", "emacs"), ("editor", 5), ("authorConfidence", "certain"), ("authorConfidence", 1)):
    bad = copy.deepcopy(EVENTS["cell_deleted"])
    bad[_k] = _v
    invalid.append({"name": f"event cell_deleted: {_k} = {_v!r}", "contract": "BlaymEvent", "value": bad})
for _t in ("chat_message_added", "chat_message_updated"):
    bad = copy.deepcopy(EVENTS[_t])
    bad["payload"]["chatSource"] = 5
    invalid.append({"name": f"event {_t}: chatSource given a number", "contract": "BlaymEvent", "value": bad})
bad = copy.deepcopy(EVENTS["recording_gap_started"])
bad["payload"]["reason"] = "no_such_reason"
invalid.append({"name": "event recording_gap_started: unknown reason", "contract": "BlaymEvent", "value": bad})
bad = copy.deepcopy(STATE)
bad["chat"][0]["chatSource"] = 5
invalid.append({"name": "state: chat chatSource given a number", "contract": "RebuiltState", "value": bad})
bad = copy.deepcopy(EVENTS["cell_deleted"])
bad["causal"] = {"langgraph": {"threadId": "t"}}
invalid.append({"name": "event cell_deleted: old causal field", "contract": "BlaymEvent", "value": bad})
bad = copy.deepcopy(EVENTS["cell_deleted"])
bad["tick"] = "5"
invalid.append({"name": "event cell_deleted: integer field given a string", "contract": "BlaymEvent", "value": bad})
bad = copy.deepcopy(EVENTS["cell_deleted"])
bad["payload"]["cellId"] = 5
invalid.append({"name": "event cell_deleted: string field given a number", "contract": "BlaymEvent", "value": bad})
for _v in ("5", 5.5):
    bad = copy.deepcopy(STATE)
    bad["position"]["lastEventTick"] = _v
    invalid.append({"name": f"state: position.lastEventTick = {_v!r}", "contract": "RebuiltState", "value": bad})
bad = copy.deepcopy(RESULTS["invalid_event"])
bad["reason"] = "whatever"
invalid.append({"name": "result invalid_event: unknown reason", "contract": "RebuildResult", "value": bad})
bad = copy.deepcopy(RESULTS["invalid_event"])
bad["extra"] = 1
invalid.append({"name": "result invalid_event: extra key", "contract": "RebuildResult", "value": bad})
bad = copy.deepcopy(_pending)
bad["notebook"]["cells"][0]["outputs"][0]["clearPending"] = "yes"
invalid.append({"name": "state: clearPending not boolean", "contract": "RebuiltState", "value": bad})
bad = copy.deepcopy(STATE)
del bad["detachedOutputs"]
invalid.append({"name": "state: detachedOutputs missing (empty case)", "contract": "RebuiltState", "value": bad})
bad = copy.deepcopy(MINIMAL_STATE)
del bad["detachedOutputs"]
invalid.append({"name": "state minimal: missing detachedOutputs", "contract": "RebuiltState", "value": bad})
for _v in ("x", {"runId": "r"}, [{"runId": "r"}], [{"runId": 5, "items": []}], [{"runId": "r", "items": [], "clearPending": "yes"}]):
    bad = copy.deepcopy(STATE)
    bad["detachedOutputs"] = _v
    invalid.append({"name": f"state: detachedOutputs wrong type {_v!r}", "contract": "RebuiltState", "value": bad})
bad = copy.deepcopy(RESULTS["ok"])
bad["status"] = "maybe"
invalid.append({"name": "result: unknown status", "contract": "RebuildResult", "value": bad})

# Envelope cases (generic envelope)
ENVELOPE = env("s0_sample", {"hello": "world"}, 1, links={"runId": "run-1", "cellId": "cell-1", "cellRevision": 1})
valid.append({"name": "generic envelope", "contract": "BlaymEventEnvelope", "value": ENVELOPE})
for k in ENVELOPE:
    if k in ("links",):
        continue
    e = copy.deepcopy(ENVELOPE)
    del e[k]
    invalid.append({"name": f"envelope: missing {k}", "contract": "BlaymEventEnvelope", "value": e})
for k, bad in [("tick", 0), ("tick", 1.5), ("wallTimeMs", -1), ("schemaVersion", 1), ("schemaVersion", 3), ("eventId", "not-a-uuid")]:
    e = copy.deepcopy(ENVELOPE)
    e[k] = bad
    invalid.append({"name": f"envelope: {k} = {bad}", "contract": "BlaymEventEnvelope", "value": e})
e = copy.deepcopy(ENVELOPE)
e["links"]["cellRevision"] = 0
invalid.append({"name": "envelope: links.cellRevision = 0", "contract": "BlaymEventEnvelope", "value": e})
e = copy.deepcopy(ENVELOPE)
e["seq"] = 1
invalid.append({"name": "envelope: old seq field", "contract": "BlaymEventEnvelope", "value": e})
e = copy.deepcopy(ENVELOPE)
e["extra"] = True
invalid.append({"name": "envelope: extra top-level key", "contract": "BlaymEventEnvelope", "value": e})

# --- history outline and notification ---------------------------------------
OUTLINE = {
    "schemaVersion": 2,
    "explorationId": "exploration-1",
    "rootBranchId": "branch-main",
    "highestTick": 9,
    "branches": [
        {
            "branchId": "branch-main",
            "name": "main",
            "ownTicks": [1, 2, 3, 4, 5, 8],
            "runSpans": [{"runId": "run-1", "startedTick": 2, "endedTick": 4}, {"runId": "run-2", "startedTick": 5}],
        },
        {
            "branchId": "branch-b",
            "name": "try again",
            "parentBranchId": "branch-main",
            "parentTick": 4,
            "ownTicks": [6, 7, 9],
            "runSpans": [],
        },
    ],
}
OUTLINE_EMPTY = {"schemaVersion": 2, "explorationId": "exploration-1", "rootBranchId": "branch-main", "highestTick": 1,
                 "branches": [{"branchId": "branch-main", "name": "main", "ownTicks": [1], "runSpans": []}]}
ADVANCED = {"explorationId": "exploration-1", "branchId": "branch-main", "tick": 10}
ADVANCED_BRANCH = {**ADVANCED, "branchId": "branch-c", "newBranch": {"branchId": "branch-c", "name": "c", "parentBranchId": "branch-main", "parentTick": 8, "ownTicks": [10], "runSpans": []}}
valid.append({"name": "outline", "contract": "HistoryOutline", "value": OUTLINE})
valid.append({"name": "outline minimal", "contract": "HistoryOutline", "value": OUTLINE_EMPTY})
valid.append({"name": "history advanced", "contract": "HistoryAdvanced", "value": ADVANCED})
valid.append({"name": "history advanced with run started", "contract": "HistoryAdvanced", "value": {**ADVANCED, "runStarted": "run-3"}})
valid.append({"name": "history advanced with runs ended", "contract": "HistoryAdvanced", "value": {**ADVANCED, "runsEnded": ["run-1", "run-2"]}})
valid.append({"name": "history advanced with no runs ended", "contract": "HistoryAdvanced", "value": {**ADVANCED, "runsEnded": []}})
valid.append({"name": "history advanced with new branch", "contract": "HistoryAdvanced", "value": ADVANCED_BRANCH})


def _o(*path_and_value):
    *parts, new = path_and_value
    return setpath(OUTLINE, parts, new)


for k in OUTLINE:
    bad = copy.deepcopy(OUTLINE)
    del bad[k]
    invalid.append({"name": f"outline: missing {k}", "contract": "HistoryOutline", "value": bad})
for k in ("branchId", "name", "ownTicks", "runSpans"):
    bad = copy.deepcopy(OUTLINE)
    del bad["branches"][1][k]
    invalid.append({"name": f"outline: branch missing {k}", "contract": "HistoryOutline", "value": bad})
for k in ("runId", "startedTick"):
    bad = copy.deepcopy(OUTLINE)
    del bad["branches"][0]["runSpans"][0][k]
    invalid.append({"name": f"outline: run span missing {k}", "contract": "HistoryOutline", "value": bad})
for bad_v in (0, 1.5, "9"):
    invalid.append({"name": f"outline: highestTick = {bad_v!r}", "contract": "HistoryOutline", "value": _o("highestTick", bad_v)})
    invalid.append({"name": f"outline: parentTick = {bad_v!r}", "contract": "HistoryOutline", "value": setpath(OUTLINE, ["branches", "parentTick"], bad_v)})
    invalid.append({"name": f"outline: ownTicks item = {bad_v!r}", "contract": "HistoryOutline", "value": setpath(OUTLINE, ["branches", "ownTicks"], [bad_v])})
    invalid.append({"name": f"outline: run span startedTick = {bad_v!r}", "contract": "HistoryOutline", "value": setpath(OUTLINE, ["branches", "runSpans", "startedTick"], bad_v)})
    invalid.append({"name": f"outline: run span endedTick = {bad_v!r}", "contract": "HistoryOutline", "value": setpath(OUTLINE, ["branches", "runSpans", "endedTick"], bad_v)})
    invalid.append({"name": f"history advanced: tick = {bad_v!r}", "contract": "HistoryAdvanced", "value": {**ADVANCED, "tick": bad_v}})
# Duplicate or unsorted ownTicks: the schema forbids duplicates (checked in the TypeScript tests only;
# the generated Python models cannot express uniqueness, and sort order is not expressible at all).
invalid.append({"name": "outline: schemaVersion 1", "contract": "HistoryOutline", "value": _o("schemaVersion", 1)})
invalid.append({"name": "outline: extra key", "contract": "HistoryOutline", "value": {**OUTLINE, "extra": 1}})
invalid.append({"name": "outline: ownTicks not a list", "contract": "HistoryOutline", "value": setpath(OUTLINE, ["branches", "ownTicks"], "1,2")})
for k in ADVANCED:
    invalid.append({"name": f"history advanced: missing {k}", "contract": "HistoryAdvanced", "value": {x: v for x, v in ADVANCED.items() if x != k}})
invalid.append({"name": "history advanced: extra key", "contract": "HistoryAdvanced", "value": {**ADVANCED, "extra": 1}})
for bad_v in (1, ["run-1"]):
    invalid.append({"name": f"history advanced: runStarted = {bad_v!r}", "contract": "HistoryAdvanced", "value": {**ADVANCED, "runStarted": bad_v}})
for bad_v in ("run-1", [1], [["run-1"]]):
    invalid.append({"name": f"history advanced: runsEnded = {bad_v!r}", "contract": "HistoryAdvanced", "value": {**ADVANCED, "runsEnded": bad_v}})
invalid.append({"name": "history advanced: newBranch missing ownTicks", "contract": "HistoryAdvanced", "value": {**ADVANCED_BRANCH, "newBranch": {k: v for k, v in ADVANCED_BRANCH["newBranch"].items() if k != "ownTicks"}}})


_rec = {k: x for k, x in EVENTS["cell_deleted"].items() if k not in ("tick", "branchId")}
invalid.append({"name": "recorder event: carries a tick", "contract": "RecorderEvent", "value": {**_rec, "tick": 3}})
invalid.append({"name": "recorder event: carries a branchId", "contract": "RecorderEvent", "value": {**_rec, "branchId": "branch-main"}})
invalid.append({"name": "recorder event: missing eventId", "contract": "RecorderEvent", "value": {k: x for k, x in _rec.items() if k != "eventId"}})
invalid.append({"name": "recorder event: type and payload of different events", "contract": "RecorderEvent", "value": {**_rec, "payload": {"kernelId": "kernel-1", "reason": "crash"}}})
invalid.append({"name": "event cell_inserted: outputs not a list", "contract": "BlaymEvent", "value": {**EVENTS["cell_inserted"], "payload": {**EVENTS["cell_inserted"]["payload"], "outputs": "x"}}})
# --- service API ---------------------------------------------------------------
_rec_ok = {k: x for k, x in EVENTS["cell_deleted"].items() if k not in ("tick", "branchId")}
_rec_snap = {k: x for k, x in EVENTS["notebook_snapshot"].items() if k not in ("tick", "branchId")}
_inv_result = RESULTS["invalid_event"]
INGEST_REQ = {"explorationId": "exploration-1", "editor": "jupyterlab", "instanceId": "tab-1", "events": [_rec_snap, _rec_ok]}
ACCEPTED = {"status": "accepted", "eventId": _rec_ok["eventId"], "branchId": "branch-main", "tick": 3, "duplicate": False}
REFUSED = {"status": "refused", "eventId": _rec_ok["eventId"], "reason": "not_active_recorder", "detail": "Another editor is recording this notebook."}
REFUSED_INVALID = {**REFUSED, "reason": "invalid_event", "detail": "The run is not running.", "rebuild": _inv_result}
INGEST_RESP = {"apiVersion": 1, "outcomes": [ACCEPTED, {**ACCEPTED, "tick": 3, "duplicate": True}, REFUSED]}
BRANCH_REQ = {"explorationId": "exploration-1", "fromBranchId": "branch-main", "fromTick": 4, "name": "try again"}
BRANCH_OK = {"status": "ok", "branch": OUTLINE["branches"][1]}
BRANCH_REFUSED = {"status": "refused", "reason": "unsettled_moment", "detail": "A cell was still running at that moment."}
ACTIVE_REQ = {"explorationId": "exploration-1", "branchId": "branch-b"}
ACTIVE_OK = {"status": "ok", "branchId": "branch-b"}
ACTIVE_REFUSED = {"status": "refused", "reason": "unknown_branch", "detail": "No such branch."}
CLAIM_REQ = {"explorationId": "exploration-1", "editor": "jupyterlab", "instanceId": "tab-1"}
CLAIM_GRANTED = {"status": "granted"}
CLAIM_REFUSED = {"status": "refused", "holderEditor": "vscode", "detail": "VS Code is recording this notebook."}
PUT_BLOB = {"contentHash": "sha256:ab12", "storedBytes": 120, "originalBytes": 400, "truncated": False}
SINCE_REQ = {"explorationId": "exploration-1", "branchId": "branch-main", "afterTick": 0}
SINCE_RESP = {"apiVersion": 1, "events": [EVENTS["notebook_snapshot"], EVENTS["cell_inserted"]], "outline": OUTLINE}
SEARCH_REQ = {"explorationId": "exploration-1", "query": "residuals"}
SEARCH_HIT = {"branchId": "branch-main", "tick": 5, "kind": "code", "snippet": "plot(residuals)"}
SEARCH_RESP = {"apiVersion": 1, "hits": [SEARCH_HIT]}
LIMITS = {"snapshotInterval": 200, "inlineOutputBytes": 16384, "maxStoredOutputBytes": 10485760,
          "truncatedPreviewBytes": 262144, "indexedTextBytesPerItem": 65536, "chatMessageMaxBytes": 1048576, "blobGzipLevel": 6}
INFO = {"apiVersion": 1, "schemaVersion": 2}


def V(name, contract, value):
    valid.append({"name": name, "contract": contract, "value": value})


def I(name, contract, value):
    invalid.append({"name": name, "contract": contract, "value": value})


def without(d, k):
    return {x: v for x, v in d.items() if x != k}


V("ingest request", "IngestRequest", INGEST_REQ)
V("ingest request with target branch", "IngestRequest", {**INGEST_REQ, "targetBranchId": "branch-b"})
V("ingest request with no events", "IngestRequest", {**INGEST_REQ, "events": []})
V("ingest accepted", "IngestOutcome", ACCEPTED)
V("ingest accepted duplicate", "IngestOutcome", {**ACCEPTED, "duplicate": True})
V("ingest refused", "IngestOutcome", REFUSED)
V("ingest refused invalid event with rebuild", "IngestOutcome", REFUSED_INVALID)
for r in ("unauthorized", "unsupported_schema_version", "unknown_branch", "not_active_recorder", "invalid_event", "conflict", "missing_blob", "bad_first_event"):
    V(f"ingest refusal reason: {r}", "IngestOutcome", {**REFUSED, "reason": r})
V("ingest response", "IngestResponse", INGEST_RESP)
V("create branch request", "CreateBranchRequest", BRANCH_REQ)
V("create branch ok", "CreateBranchResponse", BRANCH_OK)
for r in ("unknown_moment", "moment_not_rebuildable", "unsettled_moment", "not_on_line", "unauthorized"):
    V(f"create branch refused: {r}", "CreateBranchResponse", {**BRANCH_REFUSED, "reason": r})
V("set active branch request", "SetActiveBranchRequest", ACTIVE_REQ)
V("set active branch ok", "SetActiveBranchResponse", ACTIVE_OK)
V("set active branch refused", "SetActiveBranchResponse", ACTIVE_REFUSED)
V("set active branch refused unauthorized", "SetActiveBranchResponse", {**ACTIVE_REFUSED, "reason": "unauthorized"})
V("claim recorder request", "ClaimRecorderRequest", CLAIM_REQ)
V("claim recorder granted", "ClaimRecorderResponse", CLAIM_GRANTED)
V("claim recorder refused", "ClaimRecorderResponse", CLAIM_REFUSED)
V("put blob response", "PutBlobResponse", PUT_BLOB)
V("put blob response truncated", "PutBlobResponse", {**PUT_BLOB, "truncated": True, "originalBytes": 0, "storedBytes": 0})
V("events since request", "EventsSinceRequest", SINCE_REQ)
V("events since response", "EventsSinceResponse", SINCE_RESP)
V("events since response with no events", "EventsSinceResponse", {**SINCE_RESP, "events": []})
V("search request", "SearchRequest", SEARCH_REQ)
V("search request with kinds and limit", "SearchRequest", {**SEARCH_REQ, "kinds": ["code", "chat", "output_text", "table_columns", "chart_text"], "limit": 20})
V("search hit", "SearchHit", SEARCH_HIT)
for k in ("chat", "output_text", "table_columns", "chart_text"):
    V(f"search hit kind: {k}", "SearchHit", {**SEARCH_HIT, "kind": k})
V("search response", "SearchResponse", SEARCH_RESP)
V("store limits", "StoreLimits", LIMITS)
V("store limits empty", "StoreLimits", {})
V("store limits partial", "StoreLimits", {"snapshotInterval": 50})
V("service info", "ServiceInfo", INFO)
STATE_REQ = {"explorationId": "exploration-1", "branchId": "branch-main", "tick": 4}
OUTLINE_REQ = {"explorationId": "exploration-1"}
BLOB_REQ = {"explorationId": "exploration-1", "contentHash": "sha256:ab12"}
V("state at request", "StateAtRequest", STATE_REQ)
V("outline request", "OutlineRequest", OUTLINE_REQ)
V("get blob request", "GetBlobRequest", BLOB_REQ)

# every required field missing
for name, contract, base in (
    ("ingest request", "IngestRequest", INGEST_REQ),
    ("ingest accepted", "IngestOutcome", ACCEPTED),
    ("ingest refused", "IngestOutcome", REFUSED),
    ("ingest response", "IngestResponse", INGEST_RESP),
    ("create branch request", "CreateBranchRequest", BRANCH_REQ),
    ("create branch ok", "CreateBranchResponse", BRANCH_OK),
    ("create branch refused", "CreateBranchResponse", BRANCH_REFUSED),
    ("set active branch request", "SetActiveBranchRequest", ACTIVE_REQ),
    ("set active branch ok", "SetActiveBranchResponse", ACTIVE_OK),
    ("set active branch refused", "SetActiveBranchResponse", ACTIVE_REFUSED),
    ("claim recorder request", "ClaimRecorderRequest", CLAIM_REQ),
    ("claim recorder granted", "ClaimRecorderResponse", CLAIM_GRANTED),
    ("claim recorder refused", "ClaimRecorderResponse", CLAIM_REFUSED),
    ("put blob response", "PutBlobResponse", PUT_BLOB),
    ("events since request", "EventsSinceRequest", SINCE_REQ),
    ("events since response", "EventsSinceResponse", SINCE_RESP),
    ("search request", "SearchRequest", SEARCH_REQ),
    ("search hit", "SearchHit", SEARCH_HIT),
    ("search response", "SearchResponse", SEARCH_RESP),
    ("service info", "ServiceInfo", INFO),
    ("state at request", "StateAtRequest", STATE_REQ),
    ("outline request", "OutlineRequest", OUTLINE_REQ),
    ("get blob request", "GetBlobRequest", BLOB_REQ),
):
    for k in base:
        I(f"{name}: missing {k}", contract, without(base, k))
    I(f"{name}: extra key", contract, {**base, "extra": 1})

I("ingest request: recorder event carries a tick", "IngestRequest", {**INGEST_REQ, "events": [{**_rec_ok, "tick": 3}]})
I("ingest request: events not a list", "IngestRequest", {**INGEST_REQ, "events": _rec_ok})
I("ingest request: target branch not a string", "IngestRequest", {**INGEST_REQ, "targetBranchId": 1})
I("ingest outcome: unknown status", "IngestOutcome", {**ACCEPTED, "status": "maybe"})
I("ingest accepted: duplicate not a boolean", "IngestOutcome", {**ACCEPTED, "duplicate": "no"})
I("ingest accepted: refused fields mixed in", "IngestOutcome", {**ACCEPTED, "reason": "conflict"})
I("ingest refused: unknown reason", "IngestOutcome", {**REFUSED, "reason": "because"})
I("ingest refused: rebuild is not a rebuild result", "IngestOutcome", {**REFUSED, "rebuild": {"status": "fine"}})
I("ingest response: apiVersion 2", "IngestResponse", {**INGEST_RESP, "apiVersion": 2})
I("ingest response: outcomes not a list", "IngestResponse", {**INGEST_RESP, "outcomes": ACCEPTED})
I("create branch refused: unknown reason", "CreateBranchResponse", {**BRANCH_REFUSED, "reason": "no"})
I("create branch ok: branch is not an outline branch", "CreateBranchResponse", {**BRANCH_OK, "branch": {"branchId": "x"}})
I("create branch response: unknown status", "CreateBranchResponse", {**BRANCH_REFUSED, "status": "later"})
I("set active branch refused: unknown reason", "SetActiveBranchResponse", {**ACTIVE_REFUSED, "reason": "no"})
I("claim recorder request: unknown editor", "ClaimRecorderRequest", {**CLAIM_REQ, "editor": "emacs"})
I("claim recorder refused: unknown holder editor", "ClaimRecorderResponse", {**CLAIM_REFUSED, "holderEditor": "emacs"})
I("claim recorder response: unknown status", "ClaimRecorderResponse", {"status": "queued"})
I("put blob response: truncated not a boolean", "PutBlobResponse", {**PUT_BLOB, "truncated": 1})
for bad_v in (-1, 1.5, "1"):
    I(f"put blob response: storedBytes = {bad_v!r}", "PutBlobResponse", {**PUT_BLOB, "storedBytes": bad_v})
    I(f"put blob response: originalBytes = {bad_v!r}", "PutBlobResponse", {**PUT_BLOB, "originalBytes": bad_v})
    I(f"events since request: afterTick = {bad_v!r}", "EventsSinceRequest", {**SINCE_REQ, "afterTick": bad_v})
for bad_v in (0, 1.5, "1"):
    I(f"ingest accepted: tick = {bad_v!r}", "IngestOutcome", {**ACCEPTED, "tick": bad_v})
    I(f"create branch request: fromTick = {bad_v!r}", "CreateBranchRequest", {**BRANCH_REQ, "fromTick": bad_v})
    I(f"search hit: tick = {bad_v!r}", "SearchHit", {**SEARCH_HIT, "tick": bad_v})
    I(f"search request: limit = {bad_v!r}", "SearchRequest", {**SEARCH_REQ, "limit": bad_v})
    I(f"store limits: snapshotInterval = {bad_v!r}", "StoreLimits", {"snapshotInterval": bad_v})
    I(f"store limits: maxStoredOutputBytes = {bad_v!r}", "StoreLimits", {"maxStoredOutputBytes": bad_v})
    I(f"store limits: indexedTextBytesPerItem = {bad_v!r}", "StoreLimits", {"indexedTextBytesPerItem": bad_v})
    I(f"store limits: chatMessageMaxBytes = {bad_v!r}", "StoreLimits", {"chatMessageMaxBytes": bad_v})
for bad_v in (-1, 1.5, "1"):
    I(f"store limits: inlineOutputBytes = {bad_v!r}", "StoreLimits", {"inlineOutputBytes": bad_v})
    I(f"store limits: truncatedPreviewBytes = {bad_v!r}", "StoreLimits", {"truncatedPreviewBytes": bad_v})
for bad_v in (0, 10, 1.5, "6"):
    I(f"store limits: blobGzipLevel = {bad_v!r}", "StoreLimits", {"blobGzipLevel": bad_v})
I("events since response: apiVersion 2", "EventsSinceResponse", {**SINCE_RESP, "apiVersion": 2})
I("events since response: events carry no tick", "EventsSinceResponse", {**SINCE_RESP, "events": [_rec_ok]})
I("events since response: outline not an outline", "EventsSinceResponse", {**SINCE_RESP, "outline": {"explorationId": "x"}})
I("search request: kinds not a list", "SearchRequest", {**SEARCH_REQ, "kinds": "code"})
I("search request: unknown kind", "SearchRequest", {**SEARCH_REQ, "kinds": ["image"]})
I("search request: query not a string", "SearchRequest", {**SEARCH_REQ, "query": 1})
I("search hit: unknown kind", "SearchHit", {**SEARCH_HIT, "kind": "snippet"})
I("search response: hits not a list", "SearchResponse", {**SEARCH_RESP, "hits": SEARCH_HIT})
for bad_v in (0, 1.5, "1"):
    I(f"state at request: tick = {bad_v!r}", "StateAtRequest", {**STATE_REQ, "tick": bad_v})
I("ingest request: unknown editor", "IngestRequest", {**INGEST_REQ, "editor": "emacs"})
I("ingest request: instanceId not a string", "IngestRequest", {**INGEST_REQ, "instanceId": 1})
I("get blob request: contentHash not a string", "GetBlobRequest", {**BLOB_REQ, "contentHash": 1})
I("outline request: explorationId not a string", "OutlineRequest", {"explorationId": 1})
I("service info: apiVersion 2", "ServiceInfo", {**INFO, "apiVersion": 2})
I("service info: schemaVersion 1", "ServiceInfo", {**INFO, "schemaVersion": 1})
I("store limits: extra key", "StoreLimits", {"snapshotInterval": 200, "extra": 1})

# --- service API: adversarial (reviewer) ----------------------------------------
V("store limits: gzip level 1 and 9 (bounds)", "StoreLimits", {"blobGzipLevel": 1})
V("store limits: gzip level 9", "StoreLimits", {"blobGzipLevel": 9})
V("store limits: zero inline and preview bytes", "StoreLimits", {"inlineOutputBytes": 0, "truncatedPreviewBytes": 0})
V("search request: limit 1 (bound)", "SearchRequest", {**SEARCH_REQ, "limit": 1})
V("events since request: afterTick 0 (bound)", "EventsSinceRequest", SINCE_REQ)
V("ingest request: several event kinds", "IngestRequest", {**INGEST_REQ, "events": [_rec_snap, _rec_ok, _rec_snap]})
I("ingest request: second event carries a branchId", "IngestRequest", {**INGEST_REQ, "events": [_rec_snap, {**_rec_ok, "branchId": "branch-main"}]})
I("ingest request: second event carries a tick", "IngestRequest", {**INGEST_REQ, "events": [_rec_snap, {**_rec_ok, "tick": 3}]})
I("ingest request: a full stored event instead of a recorder event", "IngestRequest", {**INGEST_REQ, "events": [EVENTS["cell_deleted"]]})
I("ingest request: second event missing eventId", "IngestRequest", {**INGEST_REQ, "events": [_rec_snap, without(_rec_ok, "eventId")]})
I("ingest request: second event type and payload of different events", "IngestRequest", {**INGEST_REQ, "events": [_rec_snap, {**_rec_ok, "payload": {"kernelId": "kernel-1", "reason": "crash"}}]})
I("ingest request: second event has an unknown type", "IngestRequest", {**INGEST_REQ, "events": [_rec_snap, {**_rec_ok, "type": "cell_exploded"}]})
I("ingest request: an event is null", "IngestRequest", {**INGEST_REQ, "events": [_rec_snap, None]})
I("ingest request: wrong event schema version", "IngestRequest", {**INGEST_REQ, "events": [{**_rec_ok, "schemaVersion": 1}]})
I("ingest outcome: refused with accepted fields (tick)", "IngestOutcome", {**REFUSED, "tick": 3})
I("ingest outcome: refused with accepted fields (branchId, duplicate)", "IngestOutcome", {**REFUSED, "branchId": "branch-main", "duplicate": False})
I("ingest outcome: accepted with refused fields (detail)", "IngestOutcome", {**ACCEPTED, "detail": "x"})
I("ingest outcome: accepted with rebuild", "IngestOutcome", {**ACCEPTED, "rebuild": _inv_result})
I("ingest outcome: no status", "IngestOutcome", without(ACCEPTED, "status"))
I("ingest outcome: status null", "IngestOutcome", {**ACCEPTED, "status": None})
I("ingest outcome: accepted shape under refused status", "IngestOutcome", {**ACCEPTED, "status": "refused"})
I("ingest outcome: refused shape under accepted status", "IngestOutcome", {**REFUSED, "status": "accepted"})
I("ingest outcome: refused rebuild with invalid nested reason", "IngestOutcome", {**REFUSED_INVALID, "rebuild": {**_inv_result, "reason": "nope"}})
I("ingest response: one bad outcome among good", "IngestResponse", {**INGEST_RESP, "outcomes": [ACCEPTED, {**REFUSED, "reason": "because"}]})
I("ingest response: one outcome of mixed members", "IngestResponse", {**INGEST_RESP, "outcomes": [ACCEPTED, {**ACCEPTED, "reason": "conflict", "detail": "x"}]})
I("ingest response: no apiVersion", "IngestResponse", without(INGEST_RESP, "apiVersion"))
I("create branch response: ok with refused fields", "CreateBranchResponse", {**BRANCH_OK, "reason": "unknown_moment", "detail": "x"})
I("create branch response: refused with a branch", "CreateBranchResponse", {**BRANCH_REFUSED, "branch": OUTLINE["branches"][1]})
I("create branch response: no status", "CreateBranchResponse", without(BRANCH_OK, "status"))
I("create branch response: refused shape under ok status", "CreateBranchResponse", {**BRANCH_REFUSED, "status": "ok"})
I("set active branch response: ok with refused fields", "SetActiveBranchResponse", {**ACTIVE_OK, "reason": "unknown_branch", "detail": "x"})
I("set active branch response: refused with branchId", "SetActiveBranchResponse", {**ACTIVE_REFUSED, "branchId": "branch-b"})
I("set active branch response: unknown status", "SetActiveBranchResponse", {**ACTIVE_OK, "status": "maybe"})
I("claim recorder response: granted with holderEditor", "ClaimRecorderResponse", {**CLAIM_GRANTED, "holderEditor": "vscode"})
I("claim recorder response: refused with no holderEditor", "ClaimRecorderResponse", without(CLAIM_REFUSED, "holderEditor"))
I("claim recorder response: no status", "ClaimRecorderResponse", without(CLAIM_REFUSED, "status"))
I("claim recorder response: refused shape under granted status", "ClaimRecorderResponse", {**CLAIM_REFUSED, "status": "granted"})
I("events since response: one event with a tick but an invalid payload", "EventsSinceResponse", {**SINCE_RESP, "events": [EVENTS["cell_inserted"], {**EVENTS["cell_deleted"], "payload": {}}]})
I("events since response: a recorder event (no tick) among stored events", "EventsSinceResponse", {**SINCE_RESP, "events": [EVENTS["cell_inserted"], _rec_ok]})
I("events since response: outline with a bad branch", "EventsSinceResponse", {**SINCE_RESP, "outline": {**OUTLINE, "branches": [{"branchId": "x"}]}})
I("search response: one bad hit among good", "SearchResponse", {**SEARCH_RESP, "hits": [SEARCH_HIT, {**SEARCH_HIT, "kind": "image"}]})
I("search request: kinds with a null", "SearchRequest", {**SEARCH_REQ, "kinds": ["code", None]})
I("store limits: blobGzipLevel true", "StoreLimits", {"blobGzipLevel": True})
I("store limits: blobGzipLevel 6.0 as a string", "StoreLimits", {"blobGzipLevel": "6.0"})
I("store limits: blobGzipLevel -1", "StoreLimits", {"blobGzipLevel": -1})
I("store limits: snapshotInterval true", "StoreLimits", {"snapshotInterval": True})
I("put blob response: truncated null", "PutBlobResponse", {**PUT_BLOB, "truncated": None})
I("service info: schemaVersion 3", "ServiceInfo", {**INFO, "schemaVersion": 3})
I("service info: apiVersion as a string", "ServiceInfo", {**INFO, "apiVersion": "1"})
I("ingest accepted: tick true", "IngestOutcome", {**ACCEPTED, "tick": True})

# --- recording API (S5) ----------------------------------------------------------
_item = CELL["outputs"][0]["items"][0]
RCR_REQ = {"explorationId": "exploration-1", "cellId": "cell-1", "code": "x = 1"}
PREP_REQ = {"explorationId": "exploration-1", "outputs": [{"output_type": "stream", "name": "stdout", "text": "hi\n"}]}
PREP_RESP = {"apiVersion": 1, "items": [_item]}
NB_REG = {"path": "analysis.ipynb", "editor": "jupyterlab", "instanceId": "tab-1", "cellIdsStable": True,
          "fingerprint": {"nbformat": "4.5", "sourceHash": "sha256:ab12"}, "cellAliases": {}}
NB_STATUS = {"apiVersion": 1, "notebookId": "nb-1", "explorationId": "nb-1", "recording": True, "active": True,
             "needsRegister": False, "needsResync": False, "runsOpen": 0, "openGaps": [], "cellRevisions": {"cell-1": 3}, "notices": []}

V("gap reason: switched_off", "BlaymEvent", {**EVENTS["recording_gap_started"], "payload": {**EVENTS["recording_gap_started"]["payload"], "reason": "switched_off"}})
V("ingest refusal reason: run_in_progress", "IngestOutcome", {**REFUSED, "reason": "run_in_progress"})
I("gap reason: unknown value", "BlaymEvent", {**EVENTS["recording_gap_started"], "payload": {**EVENTS["recording_gap_started"]["payload"], "reason": "switched-off"}})
I("ingest refusal reason: unknown value", "IngestOutcome", {**REFUSED, "reason": "run_in_flight"})
I("run output group: snapshot runId must be a string", "RunOutputs", {"runId": 5, "items": []})
V("run output group: snapshot runId", "RunOutputs", {"runId": "snapshot:evt-1", "items": [_item]})

V("resolve cell revision request", "ResolveCellRevisionRequest", RCR_REQ)
V("resolve cell revision request with branch", "ResolveCellRevisionRequest", {**RCR_REQ, "branchId": "branch-main"})
V("resolve cell revision request: empty code", "ResolveCellRevisionRequest", {**RCR_REQ, "code": ""})
I("resolve cell revision request: missing code", "ResolveCellRevisionRequest", without(RCR_REQ, "code"))
I("resolve cell revision request: extra key", "ResolveCellRevisionRequest", {**RCR_REQ, "extra": 1})
I("resolve cell revision request: code null", "ResolveCellRevisionRequest", {**RCR_REQ, "code": None})
V("resolve cell revision ok", "ResolveCellRevisionResponse", {"status": "ok", "cellRevision": 3})
V("resolve cell revision unknown cell", "ResolveCellRevisionResponse", {"status": "unknown_cell"})
V("resolve cell revision code differs", "ResolveCellRevisionResponse", {"status": "code_differs", "currentRevision": 5})
V("resolve cell revision unknown history", "ResolveCellRevisionResponse", {"status": "unknown_history"})
I("resolve cell revision response: ok with revision 0", "ResolveCellRevisionResponse", {"status": "ok", "cellRevision": 0})
I("resolve cell revision response: code differs without current revision", "ResolveCellRevisionResponse", {"status": "code_differs"})
I("resolve cell revision response: unknown status", "ResolveCellRevisionResponse", {"status": "maybe"})
I("resolve cell revision response: ok with currentRevision", "ResolveCellRevisionResponse", {"status": "ok", "cellRevision": 3, "currentRevision": 3})
I("resolve cell revision response: unknown cell with a revision", "ResolveCellRevisionResponse", {"status": "unknown_cell", "cellRevision": 3})

V("prepare outputs request", "PrepareOutputsRequest", PREP_REQ)
V("prepare outputs request: no outputs", "PrepareOutputsRequest", {**PREP_REQ, "outputs": []})
V("prepare outputs request: 200 outputs (bound)", "PrepareOutputsRequest", {**PREP_REQ, "outputs": PREP_REQ["outputs"] * 200})
I("prepare outputs request: 201 outputs", "PrepareOutputsRequest", {**PREP_REQ, "outputs": PREP_REQ["outputs"] * 201})
I("prepare outputs request: an output is a string", "PrepareOutputsRequest", {**PREP_REQ, "outputs": ["stream"]})
I("prepare outputs request: missing explorationId", "PrepareOutputsRequest", without(PREP_REQ, "explorationId"))
V("prepare outputs response", "PrepareOutputsResponse", PREP_RESP)
V("prepare outputs response: no items", "PrepareOutputsResponse", {**PREP_RESP, "items": []})
V("prepare outputs response: two items", "PrepareOutputsResponse", {**PREP_RESP, "items": [_item, _item]})
I("prepare outputs response: missing apiVersion", "PrepareOutputsResponse", without(PREP_RESP, "apiVersion"))
I("prepare outputs response: an item without contentHash", "PrepareOutputsResponse", {**PREP_RESP, "items": [without(_item, "contentHash")]})
I("prepare outputs response: items not a list", "PrepareOutputsResponse", {**PREP_RESP, "items": _item})

V("notebook registration", "NotebookRegistration", NB_REG)
V("notebook registration: old notebook with aliases", "NotebookRegistration", {**NB_REG, "cellIdsStable": False, "cellAliases": {"tmp-1": "cell-1"}, "fingerprint": {"nbformat": "4.4", "sourceHash": "sha256:cd34"}})
V("notebook registration: all options", "NotebookRegistration", {**NB_REG, "setRecording": True, "collaboration": False, "takeover": True,
  "fingerprint": {"nbformat": "4.5", "cellIds": ["cell-1", "cell-2"], "sourceHash": "sha256:ab12"}})
I("notebook registration: missing fingerprint", "NotebookRegistration", without(NB_REG, "fingerprint"))
I("notebook registration: missing cellAliases", "NotebookRegistration", without(NB_REG, "cellAliases"))
I("notebook registration: unknown editor", "NotebookRegistration", {**NB_REG, "editor": "emacs"})
I("notebook registration: fingerprint without sourceHash", "NotebookRegistration", {**NB_REG, "fingerprint": {"nbformat": "4.5"}})
I("notebook registration: extra key", "NotebookRegistration", {**NB_REG, "extra": 1})
I("notebook registration: alias value not a string", "NotebookRegistration", {**NB_REG, "cellAliases": {"tmp-1": 1}})

V("notebook status", "NotebookStatus", NB_STATUS)
V("notebook status: other recorder active", "NotebookStatus", {**NB_STATUS, "active": False, "holderInstanceId": "tab-2", "reason": "other_recorder_active"})
V("notebook status: open gaps, notices and resync", "NotebookStatus", {**NB_STATUS, "needsResync": True, "runsOpen": 2,
  "openGaps": [{"gapId": "gap-1", "source": "browser", "reason": "switched_off"}], "notices": [{"code": "moved"}, {"code": "copied"}]})
I("notebook status: missing cellRevisions", "NotebookStatus", without(NB_STATUS, "cellRevisions"))
I("notebook status: unknown reason", "NotebookStatus", {**NB_STATUS, "reason": "because"})
I("notebook status: negative runsOpen", "NotebookStatus", {**NB_STATUS, "runsOpen": -1})
I("notebook status: open gap with unknown reason", "NotebookStatus", {**NB_STATUS, "openGaps": [{"gapId": "g", "source": "browser", "reason": "nope"}]})
I("notebook status: unknown notice code", "NotebookStatus", {**NB_STATUS, "notices": [{"code": "teleported"}]})
I("notebook status: extra key", "NotebookStatus", {**NB_STATUS, "extra": 1})

names = [c["name"] for c in invalid]
assert len(names) == len(set(names)), [n for n in names if names.count(n) > 1]

(OUT / "valid-contracts.json").write_text(json.dumps(valid, indent=2) + "\n")
(OUT / "invalid-contracts.json").write_text(json.dumps(invalid, indent=2) + "\n")
print(len(valid), "valid,", len(invalid), "invalid")
