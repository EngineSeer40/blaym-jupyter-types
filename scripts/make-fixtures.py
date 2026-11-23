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
names = [c["name"] for c in invalid]
assert len(names) == len(set(names)), [n for n in names if names.count(n) > 1]

(OUT / "valid-contracts.json").write_text(json.dumps(valid, indent=2) + "\n")
(OUT / "invalid-contracts.json").write_text(json.dumps(invalid, indent=2) + "\n")
print(len(valid), "valid,", len(invalid), "invalid")
