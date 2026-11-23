/**
 * Blaym for Jupyter contracts. This file is the single source: the JSON Schema
 * bundle and the Python models are generated from it (never edited by hand).
 *
 * Ordering: every event has one `tick`, a dense running order (1, 2, 3, ...)
 * for the whole notebook history, given by Blaym's service. A position is
 * `(branchId, tick)`. Clock time (`wallTimeMs`) is only a label.
 */
export const SCHEMA_VERSION = 2;

// ---------------------------------------------------------------------------
// Shared building blocks
// ---------------------------------------------------------------------------

export type CellType = 'code' | 'markdown' | 'raw';

/**
 * Who made a change, as far as Blaym can tell. How sure it is, is in
 * `authorConfidence`; with `unknown` there is nothing to be sure about.
 */
export type AuthorHint = 'person' | 'ai' | 'outside' | 'blaym' | 'unknown';

/**
 * How sure Blaym is about `authorHint`. `known` when the editor or tool gives
 * a signal (for example an AI action announcement, or an agent edit matched to
 * its saved chat turn); `guess` when inferred (for example by timing). Leave
 * it out with `authorHint: 'unknown'`. The UI says when it is a guess.
 */
export type AuthorConfidence = 'known' | 'guess';

/** Which editor recorded an event. */
export type Editor = 'jupyterlab' | 'notebook7' | 'vscode' | 'unknown';

/** Where an event came from in the notebook, run, or chat. */
export interface EventLinks {
  runId?: string;
  cellId?: string;
  /**
   * @asType integer
   * @minimum 1
   */
  cellRevision?: number;
  chatTurnId?: string;
}

/** Which recorder could not see something (ADR 0005). */
export type GapSource = 'browser' | 'kernel' | 'chat' | 'files' | 'service';

/** Why a recorder could not see (ADR 0005). */
export type GapReason =
  | 'no_client'
  | 'kernel_restart'
  | 'server_unavailable'
  | 'source_closed'
  | 'unknown';

/**
 * `crash` only where the editor reports it; in Jupyter a crash looks like a
 * restart and stays `unknown`.
 */
export type RestartReason = 'requested' | 'crash' | 'unknown';

export type ChatSenderKind = 'person' | 'agent';

export type KernelStatus = 'unknown' | 'running';

export type RunFinishStatus = 'ok' | 'error' | 'interrupted';

/** `unfinished`: the run never reported a finish (for example a kernel restart). */
export type RunStatus = RunFinishStatus | 'running' | 'unfinished';

export type OutputType =
  | 'stream'
  | 'display_data'
  | 'execute_result'
  | 'error';

/**
 * One output item: a preview and a content hash, never the full bytes.
 * @additionalProperties false
 */
export interface OutputItem {
  outputType: OutputType;
  mimeTypes: string[];
  /** Hash of the full content (large content lives beside the history). */
  contentHash: string;
  /** Inline preview, possibly shortened. */
  preview: string;
  truncated: boolean;
  /**
   * @asType integer
   * @minimum 0
   */
  sizeBytes: number;
  /** Search text; filled by the recorder (S5), empty until then. */
  searchText?: string;
}

/**
 * The outputs one run produced for a cell.
 * @additionalProperties false
 */
export interface RunOutputs {
  /**
   * For outputs that arrived with an inserted cell and no run, `pasted:<eventId>`
   * (the `cell_inserted` event's id), made by the rebuilder, never by a recorder.
   */
  runId: string;
  items: OutputItem[];
  /**
   * Set by `outputs_cleared` with `wait: true`; the next `output_added` for the
   * run replaces `items` and clears the flag (Jupyter's "clear and wait").
   */
  clearPending?: boolean;
}

/**
 * A cell as it is in a snapshot and in the rebuilt state. `outputs` are grouped
 * by the run that produced them; the latest run is what Jupyter shows.
 * @additionalProperties false
 */
export interface NotebookCell {
  cellId: string;
  cellType: CellType;
  code: string;
  /**
   * @asType integer
   * @minimum 1
   */
  revision: number;
  metadata: Record<string, unknown>;
  outputs: RunOutputs[];
  /**
   * @asType integer
   * @minimum 1
   */
  runCount?: number;
}

/**
 * Fields every event has.
 * @additionalProperties false
 */
export interface EventBase {
  schemaVersion: 2;
  /** @format uuid */
  eventId: string;
  /** The notebook's history. */
  explorationId: string;
  /** Made by Blaym's service, never by a browser. */
  branchId: string;
  /**
   * Dense running order for the whole history, from the writer.
   * @asType integer
   * @minimum 1
   */
  tick: number;
  /**
   * Clock time in milliseconds; a label only, never used for order.
   * @asType integer
   * @minimum 0
   */
  wallTimeMs: number;
  /** "local" in the first version. */
  userId: string;
  /** "local" in the first version. */
  workspaceId: string;
  /**
   * One recorder instance (for example one browser tab, one kernel listener,
   * one chat reader). Never an editor: that is `editor`.
   */
  originId: string;
  editor?: Editor;
  authorHint?: AuthorHint;
  authorConfidence?: AuthorConfidence;
  links?: EventLinks;
}

/**
 * The generic envelope: any event, with the type and payload left open.
 * Use it to check the envelope before looking at the payload.
 * @additionalProperties false
 */
export interface BlaymEventEnvelope extends EventBase {
  type: string;
  payload: Record<string, unknown>;
}

// ---------------------------------------------------------------------------
// Payloads
// ---------------------------------------------------------------------------

/**
 * The whole notebook. Also the shape of an outside change.
 * @additionalProperties false
 */
export interface NotebookSnapshotPayload {
  path: string;
  notebookMetadata: Record<string, unknown>;
  kernelName: string;
  language: string;
  cells: NotebookCell[];
}

/** @additionalProperties false */
export interface CellInsertedPayload {
  cellId: string;
  /**
   * @asType integer
   * @minimum 0
   */
  index: number;
  cellType: CellType;
  code: string;
  /**
   * Always 1 for a new cell.
   * @asType integer
   * @minimum 1
   */
  revision: number;
  metadata?: Record<string, unknown>;
  /**
   * For cells that arrive with outputs and no run (a paste, or an AI tool
   * inserting a cell with outputs). Shown as the cell's outputs, linked to no
   * run: the rebuilder groups them under `pasted:<eventId>` (see `RunOutputs.runId`).
   */
  outputs?: OutputItem[];
}

/** @additionalProperties false */
export interface CellDeletedPayload {
  cellId: string;
}

/** @additionalProperties false */
export interface CellMovedPayload {
  cellId: string;
  /**
   * @asType integer
   * @minimum 0
   */
  fromIndex: number;
  /**
   * @asType integer
   * @minimum 0
   */
  toIndex: number;
}

/** @additionalProperties false */
export interface CellTypeChangedPayload {
  cellId: string;
  cellType: CellType;
}

/** @additionalProperties false */
export interface CellSourceChangedPayload {
  cellId: string;
  /**
   * Exactly the previous revision + 1.
   * @asType integer
   * @minimum 1
   */
  revision: number;
  /** The cell's whole new code, not a patch. */
  code: string;
}

/** @additionalProperties false */
export interface CellMetadataChangedPayload {
  cellId: string;
  /** The cell's whole new (allowed) metadata. */
  metadata: Record<string, unknown>;
}

/** @additionalProperties false */
export interface NotebookMetadataChangedPayload {
  /** The notebook's whole new (allowed) metadata. */
  metadata: Record<string, unknown>;
}

/** @additionalProperties false */
export interface RunStartedPayload {
  runId: string;
  cellId: string;
  /**
   * The revision of the code that was sent to the kernel.
   * @asType integer
   * @minimum 1
   */
  cellRevision: number;
  /**
   * @asType integer
   * @minimum 1
   */
  runCount: number;
}

/** @additionalProperties false */
export interface RunFinishedPayload {
  runId: string;
  status: RunFinishStatus;
}

/** @additionalProperties false */
export interface OutputAddedPayload {
  runId: string;
  cellId: string;
  /**
   * @asType integer
   * @minimum 0
   */
  outputIndex: number;
  item: OutputItem;
}

/** @additionalProperties false */
export interface OutputReplacedPayload {
  runId: string;
  cellId: string;
  /**
   * @asType integer
   * @minimum 0
   */
  outputIndex: number;
  item: OutputItem;
}

/** @additionalProperties false */
export interface OutputsClearedPayload {
  runId: string;
  cellId: string;
  /** "Clear and wait": the clear takes effect when the next output arrives. */
  wait: boolean;
}

/** @additionalProperties false */
export interface KernelStartedPayload {
  kernelId: string;
  kernelName: string;
  language: string;
}

/** @additionalProperties false */
export interface KernelRestartedPayload {
  kernelId: string;
  reason: RestartReason;
}

/** @additionalProperties false */
export interface NotebookRenamedPayload {
  oldPath: string;
  newPath: string;
}

/** @additionalProperties false */
export interface NotebookCopiedPayload {
  oldPath: string;
  newPath: string;
  /** A copy starts a new history. */
  newExplorationId: string;
}

/** @additionalProperties false */
export interface ChatMessageAddedPayload {
  /** The chat reader, for example `jupyter-ai` or `vscode-copilot`. */
  chatSource: string;
  /** The message's id in its source; unique within its `chatSource`. */
  messageId: string;
  /** The person's id, or the agent persona id. */
  sender: string;
  senderKind: ChatSenderKind;
  body: string;
  /**
   * Time from the chat, in milliseconds.
   * @asType integer
   * @minimum 0
   */
  chatTimeMs: number;
  agentSessionId?: string;
}

/** @additionalProperties false */
export interface ChatMessageUpdatedPayload {
  chatSource: string;
  messageId: string;
  /** The message's whole new body (a streamed reply growing). */
  body: string;
}

/**
 * The envelope `branchId` is the NEW branch: this is the first event of that
 * branch. Its line is the parent's events up to `parentTick`, then its own.
 * @additionalProperties false
 */
export interface BranchPointCreatedPayload {
  parentBranchId: string;
  /**
   * The last parent event the branch includes (at least 1: the first event is
   * always a snapshot).
   * @asType integer
   * @minimum 1
   */
  parentTick: number;
  name: string;
}

/** @additionalProperties false */
export interface RecordingGapStartedPayload {
  gapId: string;
  source: GapSource;
  reason: GapReason;
}

/** @additionalProperties false */
export interface RecordingGapEndedPayload {
  gapId: string;
}

// ---------------------------------------------------------------------------
// Events: the envelope fields, a literal `type`, and the typed payload
// ---------------------------------------------------------------------------

/** @additionalProperties false */
export interface NotebookSnapshot extends EventBase {
  type: 'notebook_snapshot';
  payload: NotebookSnapshotPayload;
}

/** @additionalProperties false */
export interface CellInserted extends EventBase {
  type: 'cell_inserted';
  payload: CellInsertedPayload;
}

/** @additionalProperties false */
export interface CellDeleted extends EventBase {
  type: 'cell_deleted';
  payload: CellDeletedPayload;
}

/** @additionalProperties false */
export interface CellMoved extends EventBase {
  type: 'cell_moved';
  payload: CellMovedPayload;
}

/** @additionalProperties false */
export interface CellTypeChanged extends EventBase {
  type: 'cell_type_changed';
  payload: CellTypeChangedPayload;
}

/** @additionalProperties false */
export interface CellSourceChanged extends EventBase {
  type: 'cell_source_changed';
  payload: CellSourceChangedPayload;
}

/** @additionalProperties false */
export interface CellMetadataChanged extends EventBase {
  type: 'cell_metadata_changed';
  payload: CellMetadataChangedPayload;
}

/** @additionalProperties false */
export interface NotebookMetadataChanged extends EventBase {
  type: 'notebook_metadata_changed';
  payload: NotebookMetadataChangedPayload;
}

/** @additionalProperties false */
export interface RunStarted extends EventBase {
  type: 'run_started';
  payload: RunStartedPayload;
}

/** @additionalProperties false */
export interface RunFinished extends EventBase {
  type: 'run_finished';
  payload: RunFinishedPayload;
}

/** @additionalProperties false */
export interface OutputAdded extends EventBase {
  type: 'output_added';
  payload: OutputAddedPayload;
}

/** @additionalProperties false */
export interface OutputReplaced extends EventBase {
  type: 'output_replaced';
  payload: OutputReplacedPayload;
}

/** @additionalProperties false */
export interface OutputsCleared extends EventBase {
  type: 'outputs_cleared';
  payload: OutputsClearedPayload;
}

/** @additionalProperties false */
export interface KernelStarted extends EventBase {
  type: 'kernel_started';
  payload: KernelStartedPayload;
}

/** @additionalProperties false */
export interface KernelRestarted extends EventBase {
  type: 'kernel_restarted';
  payload: KernelRestartedPayload;
}

/** @additionalProperties false */
export interface NotebookRenamed extends EventBase {
  type: 'notebook_renamed';
  payload: NotebookRenamedPayload;
}

/** @additionalProperties false */
export interface NotebookCopied extends EventBase {
  type: 'notebook_copied';
  payload: NotebookCopiedPayload;
}

/**
 * The notebook as found in the file. The rebuilder replaces the notebook with
 * it. `authorHint` is always `outside`. The UI may still call it "changed
 * outside Jupyter" in JupyterLab.
 * @additionalProperties false
 */
export interface ChangedOutsideEditor extends EventBase {
  type: 'changed_outside_editor';
  authorHint: 'outside';
  payload: NotebookSnapshotPayload;
}

/** @additionalProperties false */
export interface ChatMessageAdded extends EventBase {
  type: 'chat_message_added';
  payload: ChatMessageAddedPayload;
}

/** @additionalProperties false */
export interface ChatMessageUpdated extends EventBase {
  type: 'chat_message_updated';
  payload: ChatMessageUpdatedPayload;
}

/** @additionalProperties false */
export interface BranchPointCreated extends EventBase {
  type: 'branch_point_created';
  payload: BranchPointCreatedPayload;
}

/** @additionalProperties false */
export interface RecordingGapStarted extends EventBase {
  type: 'recording_gap_started';
  payload: RecordingGapStartedPayload;
}

/** @additionalProperties false */
export interface RecordingGapEnded extends EventBase {
  type: 'recording_gap_ended';
  payload: RecordingGapEndedPayload;
}

/** Every event Blaym records, told apart by `type`. */
export type BlaymEvent =
  | NotebookSnapshot
  | CellInserted
  | CellDeleted
  | CellMoved
  | CellTypeChanged
  | CellSourceChanged
  | CellMetadataChanged
  | NotebookMetadataChanged
  | RunStarted
  | RunFinished
  | OutputAdded
  | OutputReplaced
  | OutputsCleared
  | KernelStarted
  | KernelRestarted
  | NotebookRenamed
  | NotebookCopied
  | ChangedOutsideEditor
  | ChatMessageAdded
  | ChatMessageUpdated
  | BranchPointCreated
  | RecordingGapStarted
  | RecordingGapEnded;

/**
 * An event as a recorder sends it: any `BlaymEvent` without `tick` and
 * `branchId`, which Blaym's service gives (plan D14). `eventId` stays: the
 * recorder makes it and the service uses it to drop duplicates.
 */
type FromRecorder<E> = Omit<E, 'tick' | 'branchId'>;

export type RecorderEvent =
  | FromRecorder<NotebookSnapshot>
  | FromRecorder<CellInserted>
  | FromRecorder<CellDeleted>
  | FromRecorder<CellMoved>
  | FromRecorder<CellTypeChanged>
  | FromRecorder<CellSourceChanged>
  | FromRecorder<CellMetadataChanged>
  | FromRecorder<NotebookMetadataChanged>
  | FromRecorder<RunStarted>
  | FromRecorder<RunFinished>
  | FromRecorder<OutputAdded>
  | FromRecorder<OutputReplaced>
  | FromRecorder<OutputsCleared>
  | FromRecorder<KernelStarted>
  | FromRecorder<KernelRestarted>
  | FromRecorder<NotebookRenamed>
  | FromRecorder<NotebookCopied>
  | FromRecorder<ChangedOutsideEditor>
  | FromRecorder<ChatMessageAdded>
  | FromRecorder<ChatMessageUpdated>
  | FromRecorder<BranchPointCreated>
  | FromRecorder<RecordingGapStarted>
  | FromRecorder<RecordingGapEnded>;

// ---------------------------------------------------------------------------
// Rebuilt state: what the notebook, outputs and chat looked like at a position
// ---------------------------------------------------------------------------

/** @additionalProperties false */
export interface StatePosition {
  branchId: string;
  /**
   * The tick that was asked for (where the user is looking). It may fall between events.
   * @asType integer
   * @minimum 1
   */
  tick: number;
  /**
   * The tick of the last event on the line at or before `tick`; the content reflects this event.
   * @asType integer
   * @minimum 1
   */
  lastEventTick: number;
  /**
   * Which event this is along the branch's line (1 to n), counted up to `lastEventTick`; worked out, not stored.
   * @asType integer
   * @minimum 1
   */
  branchCount: number;
}

/** @additionalProperties false */
export interface RunState {
  runId: string;
  cellId: string;
  /**
   * The revision that was sent, even if the cell was edited during the run.
   * @asType integer
   * @minimum 1
   */
  cellRevision: number;
  /**
   * @asType integer
   * @minimum 1
   */
  runCount: number;
  status: RunStatus;
  /**
   * @asType integer
   * @minimum 1
   */
  startedTick: number;
  /**
   * Tick of the finish, or of the restart that left it unfinished.
   * @asType integer
   * @minimum 1
   */
  endedTick?: number;
}

/** @additionalProperties false */
export interface ChatMessageState {
  chatSource: string;
  messageId: string;
  sender: string;
  senderKind: ChatSenderKind;
  /** The latest body. */
  body: string;
  /**
   * @asType integer
   * @minimum 0
   */
  chatTimeMs: number;
  agentSessionId?: string;
  /**
   * Tick of the event that added it.
   * @asType integer
   * @minimum 1
   */
  addedTick: number;
}

/** @additionalProperties false */
export interface KernelRestartMarker {
  kernelId: string;
  reason: RestartReason;
  /**
   * @asType integer
   * @minimum 1
   */
  tick: number;
}

/** @additionalProperties false */
export interface KernelState {
  status: KernelStatus;
  kernelId?: string;
  kernelName: string;
  language: string;
  lastRestart?: KernelRestartMarker;
}

/** @additionalProperties false */
export interface GapState {
  gapId: string;
  source: GapSource;
  reason: GapReason;
  /**
   * @asType integer
   * @minimum 1
   */
  startedTick: number;
  /**
   * Absent while the gap is open.
   * @asType integer
   * @minimum 1
   */
  endedTick?: number;
}

/** @additionalProperties false */
export interface OutsideChangeMarker {
  /**
   * @asType integer
   * @minimum 1
   */
  tick: number;
}

/** @additionalProperties false */
export interface NotebookState {
  path: string;
  metadata: Record<string, unknown>;
  cells: NotebookCell[];
}

/**
 * The full state at a position. Nothing in it depends on how it was computed.
 * @additionalProperties false
 */
export interface RebuiltState {
  schemaVersion: 2;
  position: StatePosition;
  notebook: NotebookState;
  runs: RunState[];
  chat: ChatMessageState[];
  kernel: KernelState;
  gaps: GapState[];
  /**
   * Output groups of runs whose cell no longer exists, shown in review as
   * "output from a deleted cell". A run's output events address the run, so
   * output that arrives after its cell was deleted is kept here, not dropped.
   */
  detachedOutputs: RunOutputs[];
  lastOutsideChange?: OutsideChangeMarker;
}

// ---------------------------------------------------------------------------
// Rebuild result: a state, or a typed error. Never a guess.
// ---------------------------------------------------------------------------

/** @additionalProperties false */
export interface RebuildOk {
  status: 'ok';
  state: RebuiltState;
}

/** @additionalProperties false */
export interface RebuildMissingEvents {
  status: 'missing_events';
  /**
   * @asType integer
   * @minimum 1
   */
  firstMissingTick: number;
}

/** @additionalProperties false */
export interface RebuildConflict {
  status: 'conflict';
  eventId: string;
  /** The event as first stored. */
  first: BlaymEvent;
  /** The event with the same id but different content. */
  second: BlaymEvent;
}

/** @additionalProperties false */
export interface RebuildInvalidRevision {
  status: 'invalid_revision';
  eventId: string;
  cellId: string;
  /**
   * @asType integer
   * @minimum 1
   */
  expectedRevision: number;
  /**
   * @asType integer
   * @minimum 1
   */
  actualRevision: number;
}

/** @additionalProperties false */
export interface RebuildUnknownCell {
  status: 'unknown_cell';
  eventId: string;
  cellId: string;
}

/** @additionalProperties false */
export interface RebuildUnknownBranch {
  status: 'unknown_branch';
  branchId: string;
}

/** @additionalProperties false */
export interface RebuildLineageLoop {
  status: 'lineage_loop';
  /** The branches that form the loop. */
  branchIds: string[];
}

/** Why an event cannot apply to the history built so far. */
export type InvalidEventReason =
  | 'first_event_not_snapshot'
  | 'tick_clash'
  | 'duplicate_id'
  | 'unknown_run'
  | 'run_not_running'
  | 'unknown_message'
  | 'unknown_gap'
  | 'gap_already_ended'
  | 'no_output_at_index'
  | 'index_out_of_range'
  | 'position_mismatch'
  | 'invalid_branch_point'
  | 'run_cell_mismatch';

/** @additionalProperties false */
export interface RebuildInvalidEvent {
  status: 'invalid_event';
  eventId: string;
  /**
   * @asType integer
   * @minimum 1
   */
  tick: number;
  reason: InvalidEventReason;
  /** A short plain-language explanation. */
  detail: string;
}

export type RebuildResult =
  | RebuildOk
  | RebuildMissingEvents
  | RebuildConflict
  | RebuildInvalidRevision
  | RebuildUnknownCell
  | RebuildUnknownBranch
  | RebuildLineageLoop
  | RebuildInvalidEvent;

// ---------------------------------------------------------------------------
// History outline: the shape of a history, with no notebook content
// ---------------------------------------------------------------------------

/**
 * A run on one branch, from the tick it started to the tick it finished.
 * @additionalProperties false
 */
export interface OutlineRunSpan {
  runId: string;
  /**
   * @asType integer
   * @minimum 1
   */
  startedTick: number;
  /**
   * Absent while the run is still open on this branch's line. Otherwise the first
   * tick on this branch's line that closes the run (its finish, or a kernel
   * restart). It is not before `startedTick`.
   * @asType integer
   * @minimum 1
   */
  endedTick?: number;
}

/**
 * One branch in the outline. The root branch has no parent; every other
 * branch names its parent and the parent's last tick that it includes.
 * @additionalProperties false
 */
export interface OutlineBranch {
  branchId: string;
  name: string;
  parentBranchId?: string;
  /**
   * The parent's last tick included in this branch. Absent only for the root.
   * @asType integer
   * @minimum 1
   */
  parentTick?: number;
  /**
   * Ticks of this branch's own events, sorted from lowest to highest, none twice.
   * @uniqueItems true
   */
  ownTicks: Tick[];
  /**
   * The runs that matter on this branch's own part of its line: runs started on
   * its own events, plus runs started on an ancestor that were still open at this
   * branch's branch point (their `startedTick` lies on the parent's part of the
   * line). Runs that closed before the branch point are not listed; for a moment
   * at or before the branch point, the spans of the ancestor that owns that tick
   * apply. This lets a branch only be started from a settled moment.
   */
  runSpans: OutlineRunSpan[];
}

/**
 * A positive whole number: the running order of one event.
 * @asType integer
 * @minimum 1
 */
export type Tick = number;

/**
 * The shape of a notebook's history: its branches, which tick belongs to
 * which branch, and where runs started and finished. It is derived from the
 * recorded events and can always be rebuilt from them. It holds no notebook
 * content, so it is small enough to send whole.
 * @additionalProperties false
 */
export interface HistoryOutline {
  schemaVersion: 2;
  explorationId: string;
  rootBranchId: string;
  /**
   * The highest stored tick that has no missing tick below it.
   * @asType integer
   * @minimum 1
   */
  highestTick: number;
  branches: OutlineBranch[];
}

/**
 * Sent when new history is stored. It only says what is new; the receiver
 * asks for whatever it is missing.
 * @additionalProperties false
 */
export interface HistoryAdvanced {
  explorationId: string;
  /** The branch that received the new event. */
  branchId: string;
  /**
   * The new highest stored tick.
   * @asType integer
   * @minimum 1
   */
  tick: number;
  /** Present when the new event created a branch. Its entry already carries the spans it inherits. */
  newBranch?: OutlineBranch;
  /**
   * Present when the new event started a run: the id of the run whose span
   * starts at this tick on `branchId`.
   */
  runStarted?: string;
  /**
   * Present when the new event closed runs: the ids of the runs whose span on
   * `branchId`'s line ends at this tick. A finished run closes one; a kernel
   * restart closes every run still open on that line, so it may list several.
   * Only runs listed in that branch's `runSpans` are meant.
   */
  runsEnded?: string[];
}
