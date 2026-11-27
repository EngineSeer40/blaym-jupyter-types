import json
from pathlib import Path

import pytest
from pydantic import ValidationError

import blaym_notebook_types as types

ROOT = Path(__file__).resolve().parents[2]
FIXTURES = ROOT / "fixtures" / "contracts"
VALID = json.loads((FIXTURES / "valid-contracts.json").read_text())
INVALID = json.loads((FIXTURES / "invalid-contracts.json").read_text())
DEFS = json.loads(types.schema_path().read_text())["definitions"]
RECORDER = [c["value"] for c in VALID if c["contract"] == "RecorderEvent"]


def _model(name):
    return getattr(types, name)


def _members(union, key):
    """The names a union accepts, read from the schema's own constants."""
    return {DEFS[m["$ref"].split("/")[-1]]["properties"][key]["const"] for m in DEFS[union]["anyOf"]}


def _values(contract, key):
    return {c["value"][key] for c in VALID if c["contract"] == contract}


def test_valid_fixtures_parse_and_round_trip():
    for case in VALID:
        model = _model(case["contract"]).model_validate(case["value"])
        assert model.model_dump(mode="json", exclude_none=True) == case["value"], case["name"]


def test_invalid_fixtures_are_rejected():
    for case in INVALID:
        with pytest.raises(ValidationError):
            _model(case["contract"]).model_validate(case["value"])


def test_every_event_type_and_result_has_a_fixture():
    events = _members("BlaymEvent", "type")
    assert events
    assert _values("BlaymEvent", "type") == events
    assert {v["type"] for v in RECORDER} == events
    results = _members("RebuildResult", "status")
    assert results
    assert _values("RebuildResult", "status") == results


def test_event_union_picks_the_model_by_type():
    for case in VALID:
        if case["contract"] == "BlaymEvent":
            parsed = types.BlaymEvent.model_validate(case["value"]).root
            assert parsed.type == case["value"]["type"]


def test_recorder_event_becomes_a_blaym_event_with_tick_and_branch():
    for value in RECORDER:
        full = {**value, "tick": 7, "branchId": "branch-main"}
        assert types.BlaymEvent.model_validate(full).root.type == value["type"]


def test_recorder_event_with_a_tick_is_refused():
    for value in RECORDER:
        with pytest.raises(ValidationError):
            types.RecorderEvent.model_validate({**value, "tick": 7})


def test_run_started_codelink_is_optional_and_restricted():
    run = {"runId": "r1", "cellId": "c1", "cellRevision": 1, "runCount": 1}
    assert types.RunStartedPayload.model_validate(run).codeLink is None
    assert types.RunStartedPayload.model_validate({**run, "codeLink": "by_time"}).codeLink == "by_time"
    with pytest.raises(ValidationError):
        types.RunStartedPayload.model_validate({**run, "codeLink": "guess"})
