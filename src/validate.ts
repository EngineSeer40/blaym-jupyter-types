import Ajv from 'ajv';
import addFormats from 'ajv-formats';
import { readFileSync } from 'fs';
import { join } from 'path';
import type { BlaymEventEnvelope } from './contracts';

// Resolved relative to dist/ (or src/) so it works from the built package.
const schema = JSON.parse(
  readFileSync(
    join(__dirname, '..', 'schema', 'blaym-event-envelope.schema.json'),
    'utf8'
  )
);

const ajv = new Ajv({ allErrors: true });
addFormats(ajv);
const validate = ajv.compile<BlaymEventEnvelope>(schema);

export type ValidateEnvelopeResult =
  | { ok: true; value: BlaymEventEnvelope }
  | { ok: false; errors: string[] };

export function validateEnvelope(value: unknown): ValidateEnvelopeResult {
  if (validate(value)) {
    return { ok: true, value };
  }
  const errors = (validate.errors ?? []).map(e => {
    const where = e.instancePath || '(root)';
    return `${where} ${e.message ?? 'is invalid'}`;
  });
  return { ok: false, errors };
}
