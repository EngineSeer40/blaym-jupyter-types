export const SCHEMA_VERSION = 1;

export interface BlaymEventCausalLangGraph {
  threadId: string;
  checkpointId?: string;
  runId?: string;
  node?: string;
}

export interface BlaymEventCausal {
  executionId?: string;
  cellId?: string;
  sourceRevision?: number;
  langgraph?: BlaymEventCausalLangGraph;
}

/**
 * @additionalProperties false
 */
export interface BlaymEventEnvelope {
  /**
   * @asType integer
   * @minimum 1
   */
  schemaVersion: number;
  /**
   * @format uuid
   */
  eventId: string;
  explorationId: string;
  branchId: string;
  /**
   * @asType integer
   * @minimum 1
   */
  seq: number;
  /**
   * @asType integer
   * @minimum 0
   */
  wallTimeMs: number;
  originId: string;
  type: string;
  payload: Record<string, unknown>;
  causal?: BlaymEventCausal;
}
