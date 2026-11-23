import { readFileSync } from "fs";
import { join } from "path";
import { SCHEMA_VERSION, validateContract, validateEnvelope } from "../src";

type Case = { name: string; contract: string; value: unknown };
const load = (name: string): Case[] =>
  JSON.parse(
    readFileSync(join(__dirname, "..", "fixtures", "contracts", name), "utf8"),
  );
const valid = load("valid-contracts.json");
const invalid = load("invalid-contracts.json");

const EVENT_TYPES = [
  "notebook_snapshot",
  "cell_inserted",
  "cell_deleted",
  "cell_moved",
  "cell_type_changed",
  "cell_source_changed",
  "cell_metadata_changed",
  "notebook_metadata_changed",
  "run_started",
  "run_finished",
  "output_added",
  "output_replaced",
  "outputs_cleared",
  "kernel_started",
  "kernel_restarted",
  "notebook_renamed",
  "notebook_copied",
  "changed_outside_editor",
  "chat_message_added",
  "chat_message_updated",
  "branch_point_created",
  "recording_gap_started",
  "recording_gap_ended",
];
const RESULT_STATUSES = [
  "ok",
  "missing_events",
  "conflict",
  "invalid_revision",
  "unknown_cell",
  "unknown_branch",
  "lineage_loop",
  "invalid_event",
];

describe("contract fixtures", () => {
  it("uses schema version 2", () => {
    expect(SCHEMA_VERSION).toBe(2);
  });

  it.each(valid.map((c) => [c.name, c]))("accepts valid: %s", (_n, c) => {
    const k = c as Case;
    const result = validateContract(k.contract, k.value);
    expect(result.ok ? [] : result.errors).toEqual([]);
  });

  it.each(invalid.map((c) => [c.name, c]))("rejects invalid: %s", (_n, c) => {
    const k = c as Case;
    expect(validateContract(k.contract, k.value).ok).toBe(false);
  });

  it("has a valid fixture for every event type", () => {
    const covered = valid
      .filter((c) => c.contract === "BlaymEvent")
      .map((c) => (c.value as { type: string }).type);
    expect(new Set(covered)).toEqual(new Set(EVENT_TYPES));
  });

  it("has a valid fixture for every rebuild result", () => {
    const covered = valid
      .filter((c) => c.contract === "RebuildResult")
      .map((c) => (c.value as { status: string }).status);
    expect(new Set(covered)).toEqual(new Set(RESULT_STATUSES));
  });

  it("has a valid fixture for every invalid_event reason", () => {
    const reasons = valid
      .filter((c) => c.contract === "RebuildResult")
      .map((c) => c.value as { status: string; reason?: string })
      .filter((v) => v.status === "invalid_event")
      .map((v) => v.reason);
    expect(new Set(reasons).size).toBe(13);
  });

  it("has unique invalid case names", () => {
    const names = invalid.map((c) => c.name);
    expect(new Set(names).size).toBe(names.length);
  });

  it("every valid event also passes the generic envelope", () => {
    for (const c of valid.filter((c) => c.contract === "BlaymEvent")) {
      expect(validateEnvelope(c.value).ok).toBe(true);
    }
  });
});

describe("recorder events", () => {
  const recorder = valid.filter((c) => c.contract === "RecorderEvent");

  it("has a recorder fixture for every event type", () => {
    const covered = recorder.map((c) => (c.value as { type: string }).type);
    expect(new Set(covered)).toEqual(new Set(EVENT_TYPES));
  });

  it("becomes a BlaymEvent once the service gives tick and branchId", () => {
    for (const c of recorder) {
      const full = { ...(c.value as object), tick: 7, branchId: "branch-main" };
      expect(validateContract("BlaymEvent", full).ok).toBe(true);
    }
  });

  it("is refused when it carries a tick or branchId", () => {
    for (const c of recorder) {
      const v = c.value as object;
      expect(validateContract("RecorderEvent", { ...v, tick: 7 }).ok).toBe(
        false,
      );
      expect(
        validateContract("RecorderEvent", { ...v, branchId: "b" }).ok,
      ).toBe(false);
    }
  });

  it("is not a BlaymEvent without tick and branchId", () => {
    for (const c of recorder) {
      expect(validateContract("BlaymEvent", c.value).ok).toBe(false);
    }
  });
});

describe("history outline ordering", () => {
  const outline = valid.find((c) => c.name === "outline")!.value as {
    branches: { ownTicks: number[] }[];
  };

  it("rejects duplicate ownTicks (TypeScript schema check only)", () => {
    const bad = JSON.parse(JSON.stringify(outline));
    bad.branches[0].ownTicks = [1, 2, 2];
    expect(validateContract("HistoryOutline", bad).ok).toBe(false);
  });
});

describe("validateContract", () => {
  it("reports an unknown contract type", () => {
    expect(validateContract("Nope", {}).ok).toBe(false);
  });

  it("no longer knows the LangGraph type", () => {
    expect(validateContract("BlaymEventCausalLangGraph", {}).ok).toBe(false);
  });
});
