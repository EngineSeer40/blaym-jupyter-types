import Ajv from 'ajv';
import addFormats from 'ajv-formats';
import { readFileSync } from 'fs';
import { join } from 'path';
import type { BlaymEventEnvelope } from './contracts';

// Resolved relative to dist/ (or src/) so it works from the built package.
const schema = JSON.parse(
  readFileSync(
    join(__dirname, '..', 'schema', 'blaym-jupyter-contracts.schema.json'),
    'utf8'
  )
);

const BUNDLE_ID = 'blaym-jupyter-contracts';
const ajv = new Ajv({ allErrors: true });
addFormats(ajv);
ajv.addSchema(schema, BUNDLE_ID);

export type ValidateResult<T = unknown> =
  | { ok: true; value: T }
  | { ok: false; errors: string[] };

export type ValidateEnvelopeResult = ValidateResult<BlaymEventEnvelope>;

/** Validate a value against any contract type in the schema bundle. */
export function validateContract<T = unknown>(
  typeName: string,
  value: unknown
): ValidateResult<T> {
  const validate = ajv.getSchema(`${BUNDLE_ID}#/definitions/${typeName}`);
  if (!validate) {
    return { ok: false, errors: [`unknown contract type: ${typeName}`] };
  }
  if (validate(value)) {
    return { ok: true, value: value as T };
  }
  const errors = (validate.errors ?? []).map(e => {
    const where = e.instancePath || '(root)';
    return `${where} ${e.message ?? 'is invalid'}`;
  });
  return { ok: false, errors };
}

export function validateEnvelope(value: unknown): ValidateEnvelopeResult {
  return validateContract<BlaymEventEnvelope>('BlaymEventEnvelope', value);
}
