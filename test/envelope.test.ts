import { validateEnvelope } from '../src';

const valid = () => ({
  schemaVersion: 1,
  eventId: '3f2b8c1e-5a4d-4e7b-9c1a-2d6e8f0a1b3c',
  explorationId: 'exp-1',
  branchId: 'main',
  seq: 1,
  wallTimeMs: 1700000000000,
  originId: 'origin-1',
  type: 's0_sample',
  payload: { hello: 'world' },
  causal: { langgraph: { threadId: 't-1' } }
});

function expectFail(value: unknown, fragment: string) {
  const result = validateEnvelope(value);
  expect(result.ok).toBe(false);
  if (!result.ok) {
    expect(result.errors.length).toBeGreaterThan(0);
    expect(result.errors.join('\n')).toContain(fragment);
  }
}

describe('validateEnvelope', () => {
  it('accepts a valid envelope', () => {
    const result = validateEnvelope(valid());
    expect(result.ok).toBe(true);
  });

  it('rejects a missing seq', () => {
    const { seq, ...rest } = valid();
    expectFail(rest, 'seq');
  });

  it('rejects a non-integer seq', () => {
    expectFail({ ...valid(), seq: 1.5 }, '/seq');
  });

  it('rejects a non-UUID eventId', () => {
    expectFail({ ...valid(), eventId: 'not-a-uuid' }, '/eventId');
  });

  it('rejects seq of 0 (minimum 1)', () => {
    expectFail({ ...valid(), seq: 0 }, '/seq');
  });

  it('rejects an unknown key inside causal', () => {
    expectFail({ ...valid(), causal: { bogus: 1 } }, '/causal');
  });

  it('rejects an extra top-level key', () => {
    expectFail({ ...valid(), extra: true }, 'additional properties');
  });
});
