import { readFileSync } from "fs";
import { join } from "path";
import { validateContract } from "../src";

type Case = { name: string; contract: string; value: unknown };
const read = (...p: string[]) =>
  JSON.parse(readFileSync(join(__dirname, "..", ...p), "utf8"));
const valid: Case[] = read("fixtures", "contracts", "valid-contracts.json");
const invalid: Case[] = read("fixtures", "contracts", "invalid-contracts.json");
const defs = read("schema", "blaym-jupyter-contracts.schema.json").definitions;

// The names a union accepts, read from the schema's own constants.
const members = (union: string, key: string): Set<string> =>
  new Set(
    defs[union].anyOf.map(
      (m: { $ref: string }) =>
        defs[m.$ref.split("/").pop()!].properties[key].const,
    ),
  );
const valuesOf = (contract: string, key: string) =>
  new Set(
    valid
      .filter((c) => c.contract === contract)
      .map((c) => (c.value as Record<string, string>)[key]),
  );
const recorder = valid.filter((c) => c.contract === "RecorderEvent");

it("accepts every valid fixture", () => {
  for (const c of valid) {
    const result = validateContract(c.contract, c.value);
    expect([c.name, result.ok ? [] : result.errors]).toEqual([c.name, []]);
  }
});

it("rejects every invalid fixture", () => {
  for (const c of invalid) {
    expect([c.name, validateContract(c.contract, c.value).ok]).toEqual([
      c.name,
      false,
    ]);
  }
});

it("has a fixture for every event type and every rebuild result", () => {
  const events = members("BlaymEvent", "type");
  expect(events.size).toBeGreaterThan(0);
  expect(valuesOf("BlaymEvent", "type")).toEqual(events);
  expect(valuesOf("RecorderEvent", "type")).toEqual(events);
  const results = members("RebuildResult", "status");
  expect(results.size).toBeGreaterThan(0);
  expect(valuesOf("RebuildResult", "status")).toEqual(results);
});

it("turns a recorder event into a BlaymEvent once tick and branchId are added", () => {
  for (const c of recorder) {
    const full = { ...(c.value as object), tick: 7, branchId: "branch-main" };
    expect(validateContract("BlaymEvent", full).ok).toBe(true);
  }
});

it("refuses a recorder event that carries a tick", () => {
  for (const c of recorder) {
    const v = c.value as object;
    expect(validateContract("RecorderEvent", { ...v, tick: 7 }).ok).toBe(false);
  }
});

it("rejects duplicate ownTicks (TypeScript schema check only)", () => {
  const bad = JSON.parse(
    JSON.stringify(valid.find((c) => c.name === "outline")!.value),
  );
  bad.branches[0].ownTicks = [1, 2, 2];
  expect(validateContract("HistoryOutline", bad).ok).toBe(false);
});
