import json
from pathlib import Path

import pytest
from pydantic import ValidationError

import blaym_jupyter_types as types

ROOT = Path(__file__).resolve().parents[2]
FIXTURES = ROOT / "fixtures" / "contracts"
VALID = json.loads((FIXTURES / "valid-contracts.json").read_text())
INVALID = json.loads((FIXTURES / "invalid-contracts.json").read_text())

EVENT_TYPES = [
    "notebook_snapshot", "cell_inserted", "cell_deleted", "cell_moved",
    "cell_type_changed", "cell_source_changed", "cell_metadata_changed",
    "notebook_metadata_changed", "run_started", "run_finished", "output_added",
    "output_replaced", "outputs_cleared", "kernel_started", "kernel_restarted",
    "notebook_renamed", "notebook_copied", "changed_outside_editor",
    "chat_message_added", "chat_message_updated", "branch_point_created",
    "recording_gap_started", "recording_gap_ended",
]  # fmt: skip


def _model(name):
    return getattr(types, name)


@pytest.mark.parametrize("case", VALID, ids=[c["name"] for c in VALID])
def test_valid_fixture_parses_and_round_trips(case):
    model = _model(case["contract"]).model_validate(case["value"])
    assert model.model_dump(mode="json", exclude_none=True) == case["value"]


@pytest.mark.parametrize("case", INVALID, ids=[c["name"] for c in INVALID])
def test_invalid_fixture_rejected(case):
    with pytest.raises(ValidationError):
        _model(case["contract"]).model_validate(case["value"])


def test_every_event_type_has_a_valid_fixture():
    covered = {
        c["value"]["type"] for c in VALID if c["contract"] == "BlaymEvent"
    }
    assert covered == set(EVENT_TYPES)


def test_every_result_type_has_a_valid_fixture():
    covered = {c["value"]["status"] for c in VALID if c["contract"] == "RebuildResult"}
    assert covered == {
        "ok", "missing_events", "conflict", "invalid_revision",
        "unknown_cell", "unknown_branch", "lineage_loop", "invalid_event",
    }  # fmt: skip


def test_every_invalid_event_reason_has_a_valid_fixture():
    reasons = {
        c["value"]["reason"]
        for c in VALID
        if c["contract"] == "RebuildResult" and c["value"]["status"] == "invalid_event"
    }
    assert len(reasons) == 13


def test_event_union_picks_the_model_by_type():
    for case in VALID:
        if case["contract"] == "BlaymEvent":
            parsed = types.BlaymEvent.model_validate(case["value"]).root
            assert parsed.type == case["value"]["type"]


RECORDER = [c["value"] for c in VALID if c["contract"] == "RecorderEvent"]


def test_every_event_type_has_a_recorder_fixture():
    assert {v["type"] for v in RECORDER} == set(EVENT_TYPES)


@pytest.mark.parametrize("value", RECORDER, ids=[v["type"] for v in RECORDER])
def test_recorder_event_becomes_a_blaym_event_with_tick_and_branch(value):
    full = {**value, "tick": 7, "branchId": "branch-main"}
    assert types.BlaymEvent.model_validate(full).root.type == value["type"]


@pytest.mark.parametrize("value", RECORDER, ids=[v["type"] for v in RECORDER])
def test_recorder_event_with_tick_or_branch_is_refused(value):
    with pytest.raises(ValidationError):
        types.RecorderEvent.model_validate({**value, "tick": 7})
    with pytest.raises(ValidationError):
        types.RecorderEvent.model_validate({**value, "branchId": "b"})


@pytest.mark.parametrize("value", RECORDER, ids=[v["type"] for v in RECORDER])
def test_recorder_event_alone_is_not_a_blaym_event(value):
    with pytest.raises(ValidationError):
        types.BlaymEvent.model_validate(value)


def test_langgraph_is_gone():
    assert not hasattr(types, "BlaymEventCausalLangGraph")
    assert not hasattr(types, "BlaymEventCausal")


def test_schema_bundle_readable_from_the_package():
    path = types.schema_path()
    assert path.is_file()
    bundle = json.loads(path.read_text())
    assert "BlaymEvent" in bundle["definitions"]
    assert path.read_bytes() == (
        ROOT / "schema" / "blaym-jupyter-contracts.schema.json"
    ).read_bytes()
