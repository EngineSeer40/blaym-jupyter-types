# blaym-jupyter-types

The only place Blaym for Jupyter's contracts are defined: TypeScript definitions, the JSON Schema emitted from them, and the Python (Pydantic) models. `blaym-jupyter` imports them and defines none (`blaym-jupyter/docs/adr/0006-contracts-in-types-repo.md`). This is not `blaym-types`, which belongs to the original Blaym (`blaym-app`).

- `src/contracts.ts`: contract definitions: the envelope (`EventBase`, `BlaymEventEnvelope`), one interface per event (23 kinds, told apart by the literal `type`) joined as the union `BlaymEvent`, the rebuilt state (`RebuiltState`) and the rebuild result (`RebuildResult`: `ok` or a typed error). `SCHEMA_VERSION` is 2. Every event has one dense `tick`; a position is `(branchId, tick)`; the branch point event is the first event of the new branch (its envelope `branchId` is the new branch).
- `schema/blaym-jupyter-contracts.schema.json`: one JSON Schema bundle emitted from `src/contracts.ts` for every exported contract type. `npm run schema` also copies it to `python/blaym_jupyter_types/schema/`, so `blaym_jupyter_types.schema_path()` finds it in editable installs and in the wheel.
- `python/blaym_jupyter_types/`: the Python package; `_generated.py` holds the Pydantic models generated from the bundle (never edited by hand). The bundle and fixtures are packaged in the wheel.
- Python models are strict (`--strict-types str int float bool` in `scripts/generate-python.sh`), so they reject what the TypeScript validator rejects: `"5"` for an integer, `5` for a string, `"yes"` for a boolean. Parse with `Model.model_validate(value)` (a dict from `json.loads`) or `Model.model_validate_json(text)`; both are strict about these types. Do not pass `strict=False` or use `model_construct`, which skips validation. `BlaymEvent` and `RebuildResult` are union root models: use `.root` to get the concrete event or result.
- `fixtures/contracts/`: shared fixtures validated in both languages: `valid-contracts.json` (one per event type, per rebuild result, and a state) and `invalid-contracts.json` (each required field missing, each integer minimum broken, and more). Both are written by `npm run fixtures` (`scripts/make-fixtures.py`); each case names the contract it is checked against.
- Built output: `dist/index.js` and `dist/index.d.ts`.
- `docs/event-flow.md`: source of truth for how events flow. A working document; dated copies are kept in `docs/archive/` before any rewrite.

## Development

```bash
npm install
uv venv --python 3.13 .venv        # first time only
uv pip install --python .venv/bin/python -e ".[dev]"
npm run build                      # tsc, schema bundle, Python models
npm test                           # TypeScript tests
npm run python:test                # Python tests
npm run schema:check               # schema drift check
npm run python:check               # Python models drift check
```

Validate any contract in TypeScript with `validateContract(typeName, value)`; `validateEnvelope` is the envelope shortcut.

## License

MIT
