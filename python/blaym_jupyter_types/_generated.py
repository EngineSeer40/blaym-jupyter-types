# GENERATED FILE - DO NOT EDIT.
# Source schema: schema/blaym-jupyter-contracts.schema.json (blaym-jupyter-types).
# Regenerate with: npm run python:generate

from __future__ import annotations

from enum import StrEnum
from typing import Annotated, Any, Literal
from uuid import UUID

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    RootModel,
    StrictBool,
    StrictFloat,
    StrictInt,
    StrictStr,
)


class ApiVersion(RootModel[Literal[1]]):
    root: Annotated[
        Literal[1],
        Field(
            description='The version of the service API itself (separate from `schemaVersion`).'
        ),
    ]


class AuthorConfidence(StrEnum):
    known = 'known'
    guess = 'guess'


class AuthorHint(StrEnum):
    person = 'person'
    ai = 'ai'
    outside = 'outside'
    blaym = 'blaym'
    unknown = 'unknown'


class BranchPointCreatedPayload(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    name: StrictStr
    parentBranchId: StrictStr
    parentTick: Annotated[
        StrictInt,
        Field(
            description='The last parent event the branch includes (at least 1: the first event is always a snapshot).',
            ge=1,
        ),
    ]


class CellDeletedPayload(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    cellId: StrictStr


class CellMetadataChangedPayload(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    cellId: StrictStr
    metadata: Annotated[
        dict[str, Any], Field(description="The cell's whole new (allowed) metadata.")
    ]


class CellMovedPayload(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    cellId: StrictStr
    fromIndex: Annotated[StrictInt, Field(ge=0)]
    toIndex: Annotated[StrictInt, Field(ge=0)]


class CellOutputsClearedPayload(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    cellId: StrictStr


class CellSourceChangedPayload(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    cellId: StrictStr
    code: Annotated[
        StrictStr, Field(description="The cell's whole new code, not a patch.")
    ]
    revision: Annotated[
        StrictInt, Field(description='Exactly the previous revision + 1.', ge=1)
    ]


class CellType(StrEnum):
    code = 'code'
    markdown = 'markdown'
    raw = 'raw'


class CellTypeChangedPayload(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    cellId: StrictStr
    cellType: CellType


class ChatMessageUpdatedPayload(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    body: Annotated[
        StrictStr,
        Field(description="The message's whole new body (a streamed reply growing)."),
    ]
    chatSource: StrictStr
    messageId: StrictStr


class ChatSenderKind(StrEnum):
    person = 'person'
    agent = 'agent'


class ClaimRecorderGranted(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    status: Literal['granted']


class CreateBranchRefusalReason(StrEnum):
    unknown_moment = 'unknown_moment'
    moment_not_rebuildable = 'moment_not_rebuildable'
    unsettled_moment = 'unsettled_moment'
    not_on_line = 'not_on_line'
    unauthorized = 'unauthorized'


class CreateBranchRefused(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    detail: Annotated[
        StrictStr, Field(description='A short plain-language explanation.')
    ]
    reason: CreateBranchRefusalReason
    status: Literal['refused']


class CreateBranchRequest(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    explorationId: StrictStr
    fromBranchId: StrictStr
    fromTick: Annotated[StrictInt, Field(ge=1)]
    name: StrictStr


class Editor(StrEnum):
    jupyterlab = 'jupyterlab'
    notebook7 = 'notebook7'
    vscode = 'vscode'
    unknown = 'unknown'


class EventLinks(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    cellId: StrictStr | None = None
    cellRevision: Annotated[StrictInt | None, Field(ge=1)] = None
    chatTurnId: StrictStr | None = None
    runId: StrictStr | None = None


class EventsBetweenRequest(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    branchId: StrictStr
    explorationId: StrictStr
    fromTick: Annotated[StrictInt, Field(ge=1)]
    maxEvents: Annotated[
        StrictInt | None,
        Field(
            description='At most this many events; the default is 500 and the maximum 2,000.',
            ge=1,
            le=2000,
        ),
    ] = None
    toTick: Annotated[StrictInt, Field(ge=1)]


class EventsSinceRequest(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    afterTick: Annotated[
        StrictInt,
        Field(
            description='Events with a higher tick are returned; 0 means from the start.',
            ge=0,
        ),
    ]
    branchId: StrictStr
    explorationId: StrictStr


class GapReason(StrEnum):
    no_client = 'no_client'
    kernel_restart = 'kernel_restart'
    server_unavailable = 'server_unavailable'
    source_closed = 'source_closed'
    switched_off = 'switched_off'
    unknown = 'unknown'


class GapSource(StrEnum):
    browser = 'browser'
    kernel = 'kernel'
    chat = 'chat'
    files = 'files'
    service = 'service'


class GapState(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    endedTick: Annotated[
        StrictInt | None, Field(description='Absent while the gap is open.', ge=1)
    ] = None
    gapId: StrictStr
    reason: GapReason
    source: GapSource
    startedTick: Annotated[StrictInt, Field(ge=1)]


class GetBlobRequest(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    contentHash: StrictStr
    explorationId: StrictStr


class IngestAccepted(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    branchId: StrictStr
    duplicate: StrictBool
    eventId: StrictStr
    status: Literal['accepted']
    tick: Annotated[StrictInt, Field(ge=1)]


class IngestRefusalReason(StrEnum):
    unauthorized = 'unauthorized'
    unsupported_schema_version = 'unsupported_schema_version'
    unknown_branch = 'unknown_branch'
    not_active_recorder = 'not_active_recorder'
    invalid_event = 'invalid_event'
    conflict = 'conflict'
    missing_blob = 'missing_blob'
    bad_first_event = 'bad_first_event'
    run_in_progress = 'run_in_progress'


class InvalidEventReason(StrEnum):
    first_event_not_snapshot = 'first_event_not_snapshot'
    tick_clash = 'tick_clash'
    duplicate_id = 'duplicate_id'
    unknown_run = 'unknown_run'
    run_not_running = 'run_not_running'
    unknown_message = 'unknown_message'
    unknown_gap = 'unknown_gap'
    gap_already_ended = 'gap_already_ended'
    no_output_at_index = 'no_output_at_index'
    index_out_of_range = 'index_out_of_range'
    position_mismatch = 'position_mismatch'
    invalid_branch_point = 'invalid_branch_point'
    run_cell_mismatch = 'run_cell_mismatch'


class KernelStartedPayload(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    kernelId: StrictStr
    kernelName: StrictStr
    language: StrictStr


class KernelStatus(StrEnum):
    unknown = 'unknown'
    running = 'running'


class NotebookCopiedPayload(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    newExplorationId: Annotated[
        StrictStr, Field(description='A copy starts a new history.')
    ]
    newPath: StrictStr
    oldPath: StrictStr


class NotebookFingerprint(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    cellIds: Annotated[
        list[StrictStr] | None,
        Field(
            description="The notebook's own cell ids, when it has stable ones (nbformat 4.5 or newer)."
        ),
    ] = None
    nbformat: Annotated[
        StrictStr,
        Field(description='nbformat version as `major.minor`, for example `4.5`.'),
    ]
    sourceHash: Annotated[StrictStr, Field(description='Hash of all cell sources.')]


class NotebookMetadataChangedPayload(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    metadata: Annotated[
        dict[str, Any],
        Field(description="The notebook's whole new (allowed) metadata."),
    ]


class NotebookNoticeCode(StrEnum):
    moved = 'moved'
    copied = 'copied'


class NotebookRegistration(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    cellAliases: Annotated[
        dict[str, StrictStr],
        Field(
            description="The editor's temporary cell id to Blaym's cell id, where they differ."
        ),
    ]
    cellIdsStable: Annotated[
        StrictBool,
        Field(
            description="True when the editor's cell ids are the notebook's own stable ids."
        ),
    ]
    collaboration: Annotated[
        StrictBool | None,
        Field(
            description='True when the editor reports collaboration mode (not supported yet).'
        ),
    ] = None
    editor: Editor
    fingerprint: NotebookFingerprint
    instanceId: Annotated[
        StrictStr,
        Field(description='One recorder instance (for example one browser tab).'),
    ]
    path: StrictStr
    setRecording: Annotated[
        StrictBool | None,
        Field(
            description='Switch recording on or off for this notebook; absent leaves it as it is.'
        ),
    ] = None
    takeover: Annotated[
        StrictBool | None,
        Field(
            description='Ask to become the active recorder even if another instance holds it.'
        ),
    ] = None


class NotebookRenamedPayload(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    newPath: StrictStr
    oldPath: StrictStr


class NotebookStatusReason(StrEnum):
    other_recorder_active = 'other_recorder_active'
    collaboration_not_supported = 'collaboration_not_supported'


class OpenGap(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    gapId: StrictStr
    reason: GapReason
    source: GapSource


class OutlineRequest(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    explorationId: StrictStr


class OutlineRunSpan(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    endedTick: Annotated[
        StrictInt | None,
        Field(
            description="Absent while the run is still open on this branch's line. Otherwise the first tick on this branch's line that closes the run (its finish, or a kernel restart). It is not before `startedTick`.",
            ge=1,
        ),
    ] = None
    runId: StrictStr
    startedTick: Annotated[StrictInt, Field(ge=1)]


class OutputType(StrEnum):
    stream = 'stream'
    display_data = 'display_data'
    execute_result = 'execute_result'
    error = 'error'


class OutputsClearedPayload(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    cellId: StrictStr
    runId: StrictStr
    wait: Annotated[
        StrictBool,
        Field(
            description='"Clear and wait": the clear takes effect when the next output arrives.'
        ),
    ]


class OutsideChangeMarker(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    tick: Annotated[StrictInt, Field(ge=1)]


class PrepareOutputsRequest(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    explorationId: StrictStr
    outputs: Annotated[
        list[dict[str, Any]],
        Field(description='Raw nbformat output objects.', max_length=200),
    ]


class PutBlobResponse(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    contentHash: StrictStr
    originalBytes: Annotated[StrictInt, Field(ge=0)]
    storedBytes: Annotated[StrictInt, Field(ge=0)]
    truncated: StrictBool


class RebuildInvalidEvent(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    detail: Annotated[
        StrictStr, Field(description='A short plain-language explanation.')
    ]
    eventId: StrictStr
    reason: InvalidEventReason
    status: Literal['invalid_event']
    tick: Annotated[StrictInt, Field(ge=1)]


class RebuildInvalidRevision(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    actualRevision: Annotated[StrictInt, Field(ge=1)]
    cellId: StrictStr
    eventId: StrictStr
    expectedRevision: Annotated[StrictInt, Field(ge=1)]
    status: Literal['invalid_revision']


class RebuildLineageLoop(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    branchIds: Annotated[
        list[StrictStr], Field(description='The branches that form the loop.')
    ]
    status: Literal['lineage_loop']


class RebuildMissingEvents(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    firstMissingTick: Annotated[StrictInt, Field(ge=1)]
    status: Literal['missing_events']


class RebuildUnknownBranch(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    branchId: StrictStr
    status: Literal['unknown_branch']


class RebuildUnknownCell(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    cellId: StrictStr
    eventId: StrictStr
    status: Literal['unknown_cell']


class RecorderEvent3(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    authorConfidence: AuthorConfidence | None = None
    authorHint: AuthorHint | None = None
    editor: Editor | None = None
    eventId: UUID
    explorationId: Annotated[StrictStr, Field(description="The notebook's history.")]
    links: EventLinks | None = None
    originId: Annotated[
        StrictStr,
        Field(
            description='One recorder instance (for example one browser tab, one kernel listener, one chat reader). Never an editor: that is `editor`.'
        ),
    ]
    payload: CellDeletedPayload
    schemaVersion: Literal[2]
    type: Literal['cell_deleted']
    userId: Annotated[StrictStr, Field(description='"local" in the first version.')]
    wallTimeMs: Annotated[
        StrictInt,
        Field(
            description='Clock time in milliseconds; a label only, never used for order.',
            ge=0,
        ),
    ]
    workspaceId: Annotated[
        StrictStr, Field(description='"local" in the first version.')
    ]


class RecorderEvent4(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    authorConfidence: AuthorConfidence | None = None
    authorHint: AuthorHint | None = None
    editor: Editor | None = None
    eventId: UUID
    explorationId: Annotated[StrictStr, Field(description="The notebook's history.")]
    links: EventLinks | None = None
    originId: Annotated[
        StrictStr,
        Field(
            description='One recorder instance (for example one browser tab, one kernel listener, one chat reader). Never an editor: that is `editor`.'
        ),
    ]
    payload: CellMovedPayload
    schemaVersion: Literal[2]
    type: Literal['cell_moved']
    userId: Annotated[StrictStr, Field(description='"local" in the first version.')]
    wallTimeMs: Annotated[
        StrictInt,
        Field(
            description='Clock time in milliseconds; a label only, never used for order.',
            ge=0,
        ),
    ]
    workspaceId: Annotated[
        StrictStr, Field(description='"local" in the first version.')
    ]


class RecorderEvent5(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    authorConfidence: AuthorConfidence | None = None
    authorHint: AuthorHint | None = None
    editor: Editor | None = None
    eventId: UUID
    explorationId: Annotated[StrictStr, Field(description="The notebook's history.")]
    links: EventLinks | None = None
    originId: Annotated[
        StrictStr,
        Field(
            description='One recorder instance (for example one browser tab, one kernel listener, one chat reader). Never an editor: that is `editor`.'
        ),
    ]
    payload: CellTypeChangedPayload
    schemaVersion: Literal[2]
    type: Literal['cell_type_changed']
    userId: Annotated[StrictStr, Field(description='"local" in the first version.')]
    wallTimeMs: Annotated[
        StrictInt,
        Field(
            description='Clock time in milliseconds; a label only, never used for order.',
            ge=0,
        ),
    ]
    workspaceId: Annotated[
        StrictStr, Field(description='"local" in the first version.')
    ]


class RecorderEvent6(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    authorConfidence: AuthorConfidence | None = None
    authorHint: AuthorHint | None = None
    editor: Editor | None = None
    eventId: UUID
    explorationId: Annotated[StrictStr, Field(description="The notebook's history.")]
    links: EventLinks | None = None
    originId: Annotated[
        StrictStr,
        Field(
            description='One recorder instance (for example one browser tab, one kernel listener, one chat reader). Never an editor: that is `editor`.'
        ),
    ]
    payload: CellOutputsClearedPayload
    schemaVersion: Literal[2]
    type: Literal['cell_outputs_cleared']
    userId: Annotated[StrictStr, Field(description='"local" in the first version.')]
    wallTimeMs: Annotated[
        StrictInt,
        Field(
            description='Clock time in milliseconds; a label only, never used for order.',
            ge=0,
        ),
    ]
    workspaceId: Annotated[
        StrictStr, Field(description='"local" in the first version.')
    ]


class RecorderEvent7(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    authorConfidence: AuthorConfidence | None = None
    authorHint: AuthorHint | None = None
    editor: Editor | None = None
    eventId: UUID
    explorationId: Annotated[StrictStr, Field(description="The notebook's history.")]
    links: EventLinks | None = None
    originId: Annotated[
        StrictStr,
        Field(
            description='One recorder instance (for example one browser tab, one kernel listener, one chat reader). Never an editor: that is `editor`.'
        ),
    ]
    payload: CellSourceChangedPayload
    schemaVersion: Literal[2]
    type: Literal['cell_source_changed']
    userId: Annotated[StrictStr, Field(description='"local" in the first version.')]
    wallTimeMs: Annotated[
        StrictInt,
        Field(
            description='Clock time in milliseconds; a label only, never used for order.',
            ge=0,
        ),
    ]
    workspaceId: Annotated[
        StrictStr, Field(description='"local" in the first version.')
    ]


class RecorderEvent8(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    authorConfidence: AuthorConfidence | None = None
    authorHint: AuthorHint | None = None
    editor: Editor | None = None
    eventId: UUID
    explorationId: Annotated[StrictStr, Field(description="The notebook's history.")]
    links: EventLinks | None = None
    originId: Annotated[
        StrictStr,
        Field(
            description='One recorder instance (for example one browser tab, one kernel listener, one chat reader). Never an editor: that is `editor`.'
        ),
    ]
    payload: CellMetadataChangedPayload
    schemaVersion: Literal[2]
    type: Literal['cell_metadata_changed']
    userId: Annotated[StrictStr, Field(description='"local" in the first version.')]
    wallTimeMs: Annotated[
        StrictInt,
        Field(
            description='Clock time in milliseconds; a label only, never used for order.',
            ge=0,
        ),
    ]
    workspaceId: Annotated[
        StrictStr, Field(description='"local" in the first version.')
    ]


class RecorderEvent9(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    authorConfidence: AuthorConfidence | None = None
    authorHint: AuthorHint | None = None
    editor: Editor | None = None
    eventId: UUID
    explorationId: Annotated[StrictStr, Field(description="The notebook's history.")]
    links: EventLinks | None = None
    originId: Annotated[
        StrictStr,
        Field(
            description='One recorder instance (for example one browser tab, one kernel listener, one chat reader). Never an editor: that is `editor`.'
        ),
    ]
    payload: NotebookMetadataChangedPayload
    schemaVersion: Literal[2]
    type: Literal['notebook_metadata_changed']
    userId: Annotated[StrictStr, Field(description='"local" in the first version.')]
    wallTimeMs: Annotated[
        StrictInt,
        Field(
            description='Clock time in milliseconds; a label only, never used for order.',
            ge=0,
        ),
    ]
    workspaceId: Annotated[
        StrictStr, Field(description='"local" in the first version.')
    ]


class RecorderEvent14(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    authorConfidence: AuthorConfidence | None = None
    authorHint: AuthorHint | None = None
    editor: Editor | None = None
    eventId: UUID
    explorationId: Annotated[StrictStr, Field(description="The notebook's history.")]
    links: EventLinks | None = None
    originId: Annotated[
        StrictStr,
        Field(
            description='One recorder instance (for example one browser tab, one kernel listener, one chat reader). Never an editor: that is `editor`.'
        ),
    ]
    payload: OutputsClearedPayload
    schemaVersion: Literal[2]
    type: Literal['outputs_cleared']
    userId: Annotated[StrictStr, Field(description='"local" in the first version.')]
    wallTimeMs: Annotated[
        StrictInt,
        Field(
            description='Clock time in milliseconds; a label only, never used for order.',
            ge=0,
        ),
    ]
    workspaceId: Annotated[
        StrictStr, Field(description='"local" in the first version.')
    ]


class RecorderEvent15(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    authorConfidence: AuthorConfidence | None = None
    authorHint: AuthorHint | None = None
    editor: Editor | None = None
    eventId: UUID
    explorationId: Annotated[StrictStr, Field(description="The notebook's history.")]
    links: EventLinks | None = None
    originId: Annotated[
        StrictStr,
        Field(
            description='One recorder instance (for example one browser tab, one kernel listener, one chat reader). Never an editor: that is `editor`.'
        ),
    ]
    payload: KernelStartedPayload
    schemaVersion: Literal[2]
    type: Literal['kernel_started']
    userId: Annotated[StrictStr, Field(description='"local" in the first version.')]
    wallTimeMs: Annotated[
        StrictInt,
        Field(
            description='Clock time in milliseconds; a label only, never used for order.',
            ge=0,
        ),
    ]
    workspaceId: Annotated[
        StrictStr, Field(description='"local" in the first version.')
    ]


class RecorderEvent17(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    authorConfidence: AuthorConfidence | None = None
    authorHint: AuthorHint | None = None
    editor: Editor | None = None
    eventId: UUID
    explorationId: Annotated[StrictStr, Field(description="The notebook's history.")]
    links: EventLinks | None = None
    originId: Annotated[
        StrictStr,
        Field(
            description='One recorder instance (for example one browser tab, one kernel listener, one chat reader). Never an editor: that is `editor`.'
        ),
    ]
    payload: NotebookRenamedPayload
    schemaVersion: Literal[2]
    type: Literal['notebook_renamed']
    userId: Annotated[StrictStr, Field(description='"local" in the first version.')]
    wallTimeMs: Annotated[
        StrictInt,
        Field(
            description='Clock time in milliseconds; a label only, never used for order.',
            ge=0,
        ),
    ]
    workspaceId: Annotated[
        StrictStr, Field(description='"local" in the first version.')
    ]


class RecorderEvent18(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    authorConfidence: AuthorConfidence | None = None
    authorHint: AuthorHint | None = None
    editor: Editor | None = None
    eventId: UUID
    explorationId: Annotated[StrictStr, Field(description="The notebook's history.")]
    links: EventLinks | None = None
    originId: Annotated[
        StrictStr,
        Field(
            description='One recorder instance (for example one browser tab, one kernel listener, one chat reader). Never an editor: that is `editor`.'
        ),
    ]
    payload: NotebookCopiedPayload
    schemaVersion: Literal[2]
    type: Literal['notebook_copied']
    userId: Annotated[StrictStr, Field(description='"local" in the first version.')]
    wallTimeMs: Annotated[
        StrictInt,
        Field(
            description='Clock time in milliseconds; a label only, never used for order.',
            ge=0,
        ),
    ]
    workspaceId: Annotated[
        StrictStr, Field(description='"local" in the first version.')
    ]


class RecorderEvent21(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    authorConfidence: AuthorConfidence | None = None
    authorHint: AuthorHint | None = None
    editor: Editor | None = None
    eventId: UUID
    explorationId: Annotated[StrictStr, Field(description="The notebook's history.")]
    links: EventLinks | None = None
    originId: Annotated[
        StrictStr,
        Field(
            description='One recorder instance (for example one browser tab, one kernel listener, one chat reader). Never an editor: that is `editor`.'
        ),
    ]
    payload: ChatMessageUpdatedPayload
    schemaVersion: Literal[2]
    type: Literal['chat_message_updated']
    userId: Annotated[StrictStr, Field(description='"local" in the first version.')]
    wallTimeMs: Annotated[
        StrictInt,
        Field(
            description='Clock time in milliseconds; a label only, never used for order.',
            ge=0,
        ),
    ]
    workspaceId: Annotated[
        StrictStr, Field(description='"local" in the first version.')
    ]


class RecorderEvent22(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    authorConfidence: AuthorConfidence | None = None
    authorHint: AuthorHint | None = None
    editor: Editor | None = None
    eventId: UUID
    explorationId: Annotated[StrictStr, Field(description="The notebook's history.")]
    links: EventLinks | None = None
    originId: Annotated[
        StrictStr,
        Field(
            description='One recorder instance (for example one browser tab, one kernel listener, one chat reader). Never an editor: that is `editor`.'
        ),
    ]
    payload: BranchPointCreatedPayload
    schemaVersion: Literal[2]
    type: Literal['branch_point_created']
    userId: Annotated[StrictStr, Field(description='"local" in the first version.')]
    wallTimeMs: Annotated[
        StrictInt,
        Field(
            description='Clock time in milliseconds; a label only, never used for order.',
            ge=0,
        ),
    ]
    workspaceId: Annotated[
        StrictStr, Field(description='"local" in the first version.')
    ]


class RecordingGapEndedPayload(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    gapId: StrictStr


class RecordingGapStartedPayload(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    gapId: StrictStr
    reason: GapReason
    source: GapSource


class ResolveCellRevisionCodeDiffers(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    currentRevision: Annotated[StrictInt, Field(ge=1)]
    status: Literal['code_differs']


class ResolveCellRevisionOk(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    cellRevision: Annotated[StrictInt, Field(ge=1)]
    status: Literal['ok']


class ResolveCellRevisionRequest(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    branchId: StrictStr | None = None
    cellId: StrictStr
    code: StrictStr
    explorationId: StrictStr


class ResolveCellRevisionUnknownCell(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    status: Literal['unknown_cell']


class ResolveCellRevisionUnknownHistory(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    status: Literal['unknown_history']


class RestartReason(StrEnum):
    requested = 'requested'
    crash = 'crash'
    unknown = 'unknown'


class RunFinishStatus(StrEnum):
    ok = 'ok'
    error = 'error'
    interrupted = 'interrupted'


class RunFinishedPayload(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    runId: StrictStr
    status: RunFinishStatus


class RunStartedPayload(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    cellId: StrictStr
    cellRevision: Annotated[
        StrictInt,
        Field(
            description='The revision of the code that was sent to the kernel.', ge=1
        ),
    ]
    runCount: Annotated[StrictInt, Field(ge=1)]
    runId: StrictStr


class RunStatus(
    RootModel[RunFinishStatus | Literal['running'] | Literal['unfinished']]
):
    root: Annotated[
        RunFinishStatus | Literal['running'] | Literal['unfinished'],
        Field(
            description='`unfinished`: the run never reported a finish (for example a kernel restart).'
        ),
    ]


class SearchHitKind(StrEnum):
    code = 'code'
    chat = 'chat'
    output_text = 'output_text'
    table_columns = 'table_columns'
    chart_text = 'chart_text'


class SearchRequest(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    explorationId: StrictStr
    kinds: list[SearchHitKind] | None = None
    limit: Annotated[StrictInt | None, Field(ge=1)] = None
    query: StrictStr


class ServiceInfo(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    apiVersion: ApiVersion
    schemaVersion: Annotated[
        Literal[2], Field(description='The event schema version the service accepts.')
    ]


class SetActiveBranchOk(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    branchId: StrictStr
    status: Literal['ok']


class SetActiveBranchRefusalReason(StrEnum):
    unknown_branch = 'unknown_branch'
    unauthorized = 'unauthorized'


class SetActiveBranchRefused(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    detail: Annotated[
        StrictStr, Field(description='A short plain-language explanation.')
    ]
    reason: SetActiveBranchRefusalReason
    status: Literal['refused']


class SetActiveBranchRequest(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    branchId: StrictStr
    explorationId: StrictStr


class SetActiveBranchResponse(RootModel[SetActiveBranchOk | SetActiveBranchRefused]):
    root: SetActiveBranchOk | SetActiveBranchRefused


class StateAtRequest(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    branchId: StrictStr
    explorationId: StrictStr
    tick: Annotated[StrictInt, Field(ge=1)]


class StatePosition(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    branchCount: Annotated[
        StrictInt,
        Field(
            description="Which event this is along the branch's line (1 to n), counted up to `lastEventTick`; worked out, not stored.",
            ge=1,
        ),
    ]
    branchId: StrictStr
    lastEventTick: Annotated[
        StrictInt,
        Field(
            description='The tick of the last event on the line at or before `tick`; the content reflects this event.',
            ge=1,
        ),
    ]
    tick: Annotated[
        StrictInt,
        Field(
            description='The tick that was asked for (where the user is looking). It may fall between events.',
            ge=1,
        ),
    ]


class StoreLimits(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    blobGzipLevel: Annotated[
        StrictInt | None,
        Field(description='Blob compression, gzip level (6).', ge=1, le=9),
    ] = None
    chatMessageMaxBytes: Annotated[
        StrictInt | None,
        Field(description='Largest chat message kept (1048576).', ge=1),
    ] = None
    indexedTextBytesPerItem: Annotated[
        StrictInt | None, Field(description='Text indexed per item (65536).', ge=1)
    ] = None
    inlineOutputBytes: Annotated[
        StrictInt | None,
        Field(
            description='Output kept inline in the event, up to this size (16384).',
            ge=0,
        ),
    ] = None
    maxStoredOutputBytes: Annotated[
        StrictInt | None,
        Field(description='Largest output stored in full (10485760).', ge=1),
    ] = None
    snapshotInterval: Annotated[
        StrictInt | None,
        Field(description='Events between kept snapshots (200).', ge=1),
    ] = None
    truncatedPreviewBytes: Annotated[
        StrictInt | None,
        Field(description='Preview kept of a truncated output (262144).', ge=0),
    ] = None


class Tick(RootModel[StrictInt]):
    root: Annotated[
        StrictInt,
        Field(
            description='A positive whole number: the running order of one event.', ge=1
        ),
    ]


class TimelineIndexRequest(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    branchId: StrictStr
    explorationId: StrictStr
    fromTick: Annotated[StrictInt | None, Field(ge=1)] = None
    limit: Annotated[
        StrictInt | None,
        Field(
            description='At most this many entries; the default and the maximum are 5,000.',
            ge=1,
            le=5000,
        ),
    ] = None
    toTick: Annotated[StrictInt | None, Field(ge=1)] = None


class TimelineKind(StrEnum):
    edit = 'edit'
    insert = 'insert'
    delete = 'delete'
    move = 'move'
    type = 'type'
    run_started = 'run_started'
    run_ok = 'run_ok'
    run_error = 'run_error'
    run_interrupted = 'run_interrupted'
    chart = 'chart'
    table = 'table'
    text_output = 'text_output'
    chat_prompt = 'chat_prompt'
    chat_reply = 'chat_reply'
    kernel_start = 'kernel_start'
    kernel_restart = 'kernel_restart'
    outside = 'outside'
    gap = 'gap'
    branch_point = 'branch_point'
    snapshot = 'snapshot'
    other = 'other'


class BlaymEventEnvelope(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    authorConfidence: AuthorConfidence | None = None
    authorHint: AuthorHint | None = None
    branchId: Annotated[
        StrictStr, Field(description="Made by Blaym's service, never by a browser.")
    ]
    editor: Editor | None = None
    eventId: UUID
    explorationId: Annotated[StrictStr, Field(description="The notebook's history.")]
    links: EventLinks | None = None
    originId: Annotated[
        StrictStr,
        Field(
            description='One recorder instance (for example one browser tab, one kernel listener, one chat reader). Never an editor: that is `editor`.'
        ),
    ]
    payload: dict[str, Any]
    schemaVersion: Literal[2]
    tick: Annotated[
        StrictInt,
        Field(
            description='Dense running order for the whole history, from the writer.',
            ge=1,
        ),
    ]
    type: StrictStr
    userId: Annotated[StrictStr, Field(description='"local" in the first version.')]
    wallTimeMs: Annotated[
        StrictInt,
        Field(
            description='Clock time in milliseconds; a label only, never used for order.',
            ge=0,
        ),
    ]
    workspaceId: Annotated[
        StrictStr, Field(description='"local" in the first version.')
    ]


class BranchPointCreated(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    authorConfidence: AuthorConfidence | None = None
    authorHint: AuthorHint | None = None
    branchId: Annotated[
        StrictStr, Field(description="Made by Blaym's service, never by a browser.")
    ]
    editor: Editor | None = None
    eventId: UUID
    explorationId: Annotated[StrictStr, Field(description="The notebook's history.")]
    links: EventLinks | None = None
    originId: Annotated[
        StrictStr,
        Field(
            description='One recorder instance (for example one browser tab, one kernel listener, one chat reader). Never an editor: that is `editor`.'
        ),
    ]
    payload: BranchPointCreatedPayload
    schemaVersion: Literal[2]
    tick: Annotated[
        StrictInt,
        Field(
            description='Dense running order for the whole history, from the writer.',
            ge=1,
        ),
    ]
    type: Literal['branch_point_created']
    userId: Annotated[StrictStr, Field(description='"local" in the first version.')]
    wallTimeMs: Annotated[
        StrictInt,
        Field(
            description='Clock time in milliseconds; a label only, never used for order.',
            ge=0,
        ),
    ]
    workspaceId: Annotated[
        StrictStr, Field(description='"local" in the first version.')
    ]


class CellDeleted(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    authorConfidence: AuthorConfidence | None = None
    authorHint: AuthorHint | None = None
    branchId: Annotated[
        StrictStr, Field(description="Made by Blaym's service, never by a browser.")
    ]
    editor: Editor | None = None
    eventId: UUID
    explorationId: Annotated[StrictStr, Field(description="The notebook's history.")]
    links: EventLinks | None = None
    originId: Annotated[
        StrictStr,
        Field(
            description='One recorder instance (for example one browser tab, one kernel listener, one chat reader). Never an editor: that is `editor`.'
        ),
    ]
    payload: CellDeletedPayload
    schemaVersion: Literal[2]
    tick: Annotated[
        StrictInt,
        Field(
            description='Dense running order for the whole history, from the writer.',
            ge=1,
        ),
    ]
    type: Literal['cell_deleted']
    userId: Annotated[StrictStr, Field(description='"local" in the first version.')]
    wallTimeMs: Annotated[
        StrictInt,
        Field(
            description='Clock time in milliseconds; a label only, never used for order.',
            ge=0,
        ),
    ]
    workspaceId: Annotated[
        StrictStr, Field(description='"local" in the first version.')
    ]


class CellMetadataChanged(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    authorConfidence: AuthorConfidence | None = None
    authorHint: AuthorHint | None = None
    branchId: Annotated[
        StrictStr, Field(description="Made by Blaym's service, never by a browser.")
    ]
    editor: Editor | None = None
    eventId: UUID
    explorationId: Annotated[StrictStr, Field(description="The notebook's history.")]
    links: EventLinks | None = None
    originId: Annotated[
        StrictStr,
        Field(
            description='One recorder instance (for example one browser tab, one kernel listener, one chat reader). Never an editor: that is `editor`.'
        ),
    ]
    payload: CellMetadataChangedPayload
    schemaVersion: Literal[2]
    tick: Annotated[
        StrictInt,
        Field(
            description='Dense running order for the whole history, from the writer.',
            ge=1,
        ),
    ]
    type: Literal['cell_metadata_changed']
    userId: Annotated[StrictStr, Field(description='"local" in the first version.')]
    wallTimeMs: Annotated[
        StrictInt,
        Field(
            description='Clock time in milliseconds; a label only, never used for order.',
            ge=0,
        ),
    ]
    workspaceId: Annotated[
        StrictStr, Field(description='"local" in the first version.')
    ]


class CellMoved(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    authorConfidence: AuthorConfidence | None = None
    authorHint: AuthorHint | None = None
    branchId: Annotated[
        StrictStr, Field(description="Made by Blaym's service, never by a browser.")
    ]
    editor: Editor | None = None
    eventId: UUID
    explorationId: Annotated[StrictStr, Field(description="The notebook's history.")]
    links: EventLinks | None = None
    originId: Annotated[
        StrictStr,
        Field(
            description='One recorder instance (for example one browser tab, one kernel listener, one chat reader). Never an editor: that is `editor`.'
        ),
    ]
    payload: CellMovedPayload
    schemaVersion: Literal[2]
    tick: Annotated[
        StrictInt,
        Field(
            description='Dense running order for the whole history, from the writer.',
            ge=1,
        ),
    ]
    type: Literal['cell_moved']
    userId: Annotated[StrictStr, Field(description='"local" in the first version.')]
    wallTimeMs: Annotated[
        StrictInt,
        Field(
            description='Clock time in milliseconds; a label only, never used for order.',
            ge=0,
        ),
    ]
    workspaceId: Annotated[
        StrictStr, Field(description='"local" in the first version.')
    ]


class CellOutputsCleared(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    authorConfidence: AuthorConfidence | None = None
    authorHint: AuthorHint | None = None
    branchId: Annotated[
        StrictStr, Field(description="Made by Blaym's service, never by a browser.")
    ]
    editor: Editor | None = None
    eventId: UUID
    explorationId: Annotated[StrictStr, Field(description="The notebook's history.")]
    links: EventLinks | None = None
    originId: Annotated[
        StrictStr,
        Field(
            description='One recorder instance (for example one browser tab, one kernel listener, one chat reader). Never an editor: that is `editor`.'
        ),
    ]
    payload: CellOutputsClearedPayload
    schemaVersion: Literal[2]
    tick: Annotated[
        StrictInt,
        Field(
            description='Dense running order for the whole history, from the writer.',
            ge=1,
        ),
    ]
    type: Literal['cell_outputs_cleared']
    userId: Annotated[StrictStr, Field(description='"local" in the first version.')]
    wallTimeMs: Annotated[
        StrictInt,
        Field(
            description='Clock time in milliseconds; a label only, never used for order.',
            ge=0,
        ),
    ]
    workspaceId: Annotated[
        StrictStr, Field(description='"local" in the first version.')
    ]


class CellSourceChanged(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    authorConfidence: AuthorConfidence | None = None
    authorHint: AuthorHint | None = None
    branchId: Annotated[
        StrictStr, Field(description="Made by Blaym's service, never by a browser.")
    ]
    editor: Editor | None = None
    eventId: UUID
    explorationId: Annotated[StrictStr, Field(description="The notebook's history.")]
    links: EventLinks | None = None
    originId: Annotated[
        StrictStr,
        Field(
            description='One recorder instance (for example one browser tab, one kernel listener, one chat reader). Never an editor: that is `editor`.'
        ),
    ]
    payload: CellSourceChangedPayload
    schemaVersion: Literal[2]
    tick: Annotated[
        StrictInt,
        Field(
            description='Dense running order for the whole history, from the writer.',
            ge=1,
        ),
    ]
    type: Literal['cell_source_changed']
    userId: Annotated[StrictStr, Field(description='"local" in the first version.')]
    wallTimeMs: Annotated[
        StrictInt,
        Field(
            description='Clock time in milliseconds; a label only, never used for order.',
            ge=0,
        ),
    ]
    workspaceId: Annotated[
        StrictStr, Field(description='"local" in the first version.')
    ]


class CellTypeChanged(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    authorConfidence: AuthorConfidence | None = None
    authorHint: AuthorHint | None = None
    branchId: Annotated[
        StrictStr, Field(description="Made by Blaym's service, never by a browser.")
    ]
    editor: Editor | None = None
    eventId: UUID
    explorationId: Annotated[StrictStr, Field(description="The notebook's history.")]
    links: EventLinks | None = None
    originId: Annotated[
        StrictStr,
        Field(
            description='One recorder instance (for example one browser tab, one kernel listener, one chat reader). Never an editor: that is `editor`.'
        ),
    ]
    payload: CellTypeChangedPayload
    schemaVersion: Literal[2]
    tick: Annotated[
        StrictInt,
        Field(
            description='Dense running order for the whole history, from the writer.',
            ge=1,
        ),
    ]
    type: Literal['cell_type_changed']
    userId: Annotated[StrictStr, Field(description='"local" in the first version.')]
    wallTimeMs: Annotated[
        StrictInt,
        Field(
            description='Clock time in milliseconds; a label only, never used for order.',
            ge=0,
        ),
    ]
    workspaceId: Annotated[
        StrictStr, Field(description='"local" in the first version.')
    ]


class ChatMessageAddedPayload(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    agentSessionId: StrictStr | None = None
    body: StrictStr
    chatSource: Annotated[
        StrictStr,
        Field(
            description='The chat reader, for example `jupyter-ai` or `vscode-copilot`.'
        ),
    ]
    chatTimeMs: Annotated[
        StrictInt, Field(description='Time from the chat, in milliseconds.', ge=0)
    ]
    messageId: Annotated[
        StrictStr,
        Field(
            description="The message's id in its source; unique within its `chatSource`."
        ),
    ]
    sender: Annotated[
        StrictStr, Field(description="The person's id, or the agent persona id.")
    ]
    senderKind: ChatSenderKind


class ChatMessageState(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    addedTick: Annotated[
        StrictInt, Field(description='Tick of the event that added it.', ge=1)
    ]
    agentSessionId: StrictStr | None = None
    body: Annotated[StrictStr, Field(description='The latest body.')]
    chatSource: StrictStr
    chatTimeMs: Annotated[StrictInt, Field(ge=0)]
    messageId: StrictStr
    sender: StrictStr
    senderKind: ChatSenderKind


class ChatMessageUpdated(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    authorConfidence: AuthorConfidence | None = None
    authorHint: AuthorHint | None = None
    branchId: Annotated[
        StrictStr, Field(description="Made by Blaym's service, never by a browser.")
    ]
    editor: Editor | None = None
    eventId: UUID
    explorationId: Annotated[StrictStr, Field(description="The notebook's history.")]
    links: EventLinks | None = None
    originId: Annotated[
        StrictStr,
        Field(
            description='One recorder instance (for example one browser tab, one kernel listener, one chat reader). Never an editor: that is `editor`.'
        ),
    ]
    payload: ChatMessageUpdatedPayload
    schemaVersion: Literal[2]
    tick: Annotated[
        StrictInt,
        Field(
            description='Dense running order for the whole history, from the writer.',
            ge=1,
        ),
    ]
    type: Literal['chat_message_updated']
    userId: Annotated[StrictStr, Field(description='"local" in the first version.')]
    wallTimeMs: Annotated[
        StrictInt,
        Field(
            description='Clock time in milliseconds; a label only, never used for order.',
            ge=0,
        ),
    ]
    workspaceId: Annotated[
        StrictStr, Field(description='"local" in the first version.')
    ]


class ClaimRecorderRefused(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    detail: Annotated[
        StrictStr, Field(description='A short plain-language explanation.')
    ]
    holderEditor: Annotated[
        Editor, Field(description='The editor that holds the lease now.')
    ]
    status: Literal['refused']


class ClaimRecorderRequest(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    editor: Editor
    explorationId: StrictStr
    instanceId: Annotated[
        StrictStr,
        Field(description='One recorder instance (for example one browser tab).'),
    ]


class ClaimRecorderResponse(RootModel[ClaimRecorderGranted | ClaimRecorderRefused]):
    root: ClaimRecorderGranted | ClaimRecorderRefused


class EventBase(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    authorConfidence: AuthorConfidence | None = None
    authorHint: AuthorHint | None = None
    branchId: Annotated[
        StrictStr, Field(description="Made by Blaym's service, never by a browser.")
    ]
    editor: Editor | None = None
    eventId: UUID
    explorationId: Annotated[StrictStr, Field(description="The notebook's history.")]
    links: EventLinks | None = None
    originId: Annotated[
        StrictStr,
        Field(
            description='One recorder instance (for example one browser tab, one kernel listener, one chat reader). Never an editor: that is `editor`.'
        ),
    ]
    schemaVersion: Literal[2]
    tick: Annotated[
        StrictInt,
        Field(
            description='Dense running order for the whole history, from the writer.',
            ge=1,
        ),
    ]
    userId: Annotated[StrictStr, Field(description='"local" in the first version.')]
    wallTimeMs: Annotated[
        StrictInt,
        Field(
            description='Clock time in milliseconds; a label only, never used for order.',
            ge=0,
        ),
    ]
    workspaceId: Annotated[
        StrictStr, Field(description='"local" in the first version.')
    ]


class KernelRestartMarker(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    kernelId: StrictStr
    reason: RestartReason
    tick: Annotated[StrictInt, Field(ge=1)]


class KernelRestartedPayload(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    kernelId: StrictStr
    reason: RestartReason


class KernelStarted(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    authorConfidence: AuthorConfidence | None = None
    authorHint: AuthorHint | None = None
    branchId: Annotated[
        StrictStr, Field(description="Made by Blaym's service, never by a browser.")
    ]
    editor: Editor | None = None
    eventId: UUID
    explorationId: Annotated[StrictStr, Field(description="The notebook's history.")]
    links: EventLinks | None = None
    originId: Annotated[
        StrictStr,
        Field(
            description='One recorder instance (for example one browser tab, one kernel listener, one chat reader). Never an editor: that is `editor`.'
        ),
    ]
    payload: KernelStartedPayload
    schemaVersion: Literal[2]
    tick: Annotated[
        StrictInt,
        Field(
            description='Dense running order for the whole history, from the writer.',
            ge=1,
        ),
    ]
    type: Literal['kernel_started']
    userId: Annotated[StrictStr, Field(description='"local" in the first version.')]
    wallTimeMs: Annotated[
        StrictInt,
        Field(
            description='Clock time in milliseconds; a label only, never used for order.',
            ge=0,
        ),
    ]
    workspaceId: Annotated[
        StrictStr, Field(description='"local" in the first version.')
    ]


class KernelState(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    kernelId: StrictStr | None = None
    kernelName: StrictStr
    language: StrictStr
    lastRestart: KernelRestartMarker | None = None
    status: KernelStatus


class NotebookCopied(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    authorConfidence: AuthorConfidence | None = None
    authorHint: AuthorHint | None = None
    branchId: Annotated[
        StrictStr, Field(description="Made by Blaym's service, never by a browser.")
    ]
    editor: Editor | None = None
    eventId: UUID
    explorationId: Annotated[StrictStr, Field(description="The notebook's history.")]
    links: EventLinks | None = None
    originId: Annotated[
        StrictStr,
        Field(
            description='One recorder instance (for example one browser tab, one kernel listener, one chat reader). Never an editor: that is `editor`.'
        ),
    ]
    payload: NotebookCopiedPayload
    schemaVersion: Literal[2]
    tick: Annotated[
        StrictInt,
        Field(
            description='Dense running order for the whole history, from the writer.',
            ge=1,
        ),
    ]
    type: Literal['notebook_copied']
    userId: Annotated[StrictStr, Field(description='"local" in the first version.')]
    wallTimeMs: Annotated[
        StrictInt,
        Field(
            description='Clock time in milliseconds; a label only, never used for order.',
            ge=0,
        ),
    ]
    workspaceId: Annotated[
        StrictStr, Field(description='"local" in the first version.')
    ]


class NotebookMetadataChanged(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    authorConfidence: AuthorConfidence | None = None
    authorHint: AuthorHint | None = None
    branchId: Annotated[
        StrictStr, Field(description="Made by Blaym's service, never by a browser.")
    ]
    editor: Editor | None = None
    eventId: UUID
    explorationId: Annotated[StrictStr, Field(description="The notebook's history.")]
    links: EventLinks | None = None
    originId: Annotated[
        StrictStr,
        Field(
            description='One recorder instance (for example one browser tab, one kernel listener, one chat reader). Never an editor: that is `editor`.'
        ),
    ]
    payload: NotebookMetadataChangedPayload
    schemaVersion: Literal[2]
    tick: Annotated[
        StrictInt,
        Field(
            description='Dense running order for the whole history, from the writer.',
            ge=1,
        ),
    ]
    type: Literal['notebook_metadata_changed']
    userId: Annotated[StrictStr, Field(description='"local" in the first version.')]
    wallTimeMs: Annotated[
        StrictInt,
        Field(
            description='Clock time in milliseconds; a label only, never used for order.',
            ge=0,
        ),
    ]
    workspaceId: Annotated[
        StrictStr, Field(description='"local" in the first version.')
    ]


class NotebookNotice(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    code: NotebookNoticeCode


class NotebookRenamed(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    authorConfidence: AuthorConfidence | None = None
    authorHint: AuthorHint | None = None
    branchId: Annotated[
        StrictStr, Field(description="Made by Blaym's service, never by a browser.")
    ]
    editor: Editor | None = None
    eventId: UUID
    explorationId: Annotated[StrictStr, Field(description="The notebook's history.")]
    links: EventLinks | None = None
    originId: Annotated[
        StrictStr,
        Field(
            description='One recorder instance (for example one browser tab, one kernel listener, one chat reader). Never an editor: that is `editor`.'
        ),
    ]
    payload: NotebookRenamedPayload
    schemaVersion: Literal[2]
    tick: Annotated[
        StrictInt,
        Field(
            description='Dense running order for the whole history, from the writer.',
            ge=1,
        ),
    ]
    type: Literal['notebook_renamed']
    userId: Annotated[StrictStr, Field(description='"local" in the first version.')]
    wallTimeMs: Annotated[
        StrictInt,
        Field(
            description='Clock time in milliseconds; a label only, never used for order.',
            ge=0,
        ),
    ]
    workspaceId: Annotated[
        StrictStr, Field(description='"local" in the first version.')
    ]


class NotebookStatus(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    active: Annotated[
        StrictBool,
        Field(description='Whether the asking instance is the active recorder.'),
    ]
    apiVersion: ApiVersion
    cellRevisions: Annotated[
        dict[str, StrictFloat],
        Field(description='The tip revision of every cell (never goes down).'),
    ]
    explorationId: StrictStr
    holderInstanceId: StrictStr | None = None
    needsRegister: Annotated[
        StrictBool,
        Field(
            description='The server restarted: register again (and resend the aliases).'
        ),
    ]
    needsResync: Annotated[
        StrictBool,
        Field(description='The recorder should send a fresh `notebook_snapshot`.'),
    ]
    notebookId: Annotated[
        StrictStr,
        Field(
            description="Blaym's id of the notebook; also the history's `explorationId`."
        ),
    ]
    notices: list[NotebookNotice]
    openGaps: list[OpenGap]
    reason: NotebookStatusReason | None = None
    recording: Annotated[
        StrictBool, Field(description='Whether recording is on for this notebook.')
    ]
    runsOpen: Annotated[
        StrictInt, Field(description='Runs of this notebook still running.', ge=0)
    ]


class OutlineBranch(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    branchId: StrictStr
    name: StrictStr
    ownTicks: Annotated[
        list[Tick],
        Field(
            description="Ticks of this branch's own events, sorted from lowest to highest, none twice."
        ),
    ]
    parentBranchId: StrictStr | None = None
    parentTick: Annotated[
        StrictInt | None,
        Field(
            description="The parent's last tick included in this branch. Absent only for the root.",
            ge=1,
        ),
    ] = None
    runSpans: Annotated[
        list[OutlineRunSpan],
        Field(
            description="The runs that matter on this branch's own part of its line: runs started on its own events, plus runs started on an ancestor that were still open at this branch's branch point (their `startedTick` lies on the parent's part of the line). Runs that closed before the branch point are not listed; for a moment at or before the branch point, the spans of the ancestor that owns that tick apply. This lets a branch only be started from a settled moment."
        ),
    ]


class OutputItem(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    contentHash: Annotated[
        StrictStr,
        Field(
            description='Hash of the full content (large content lives beside the history).'
        ),
    ]
    mimeTypes: list[StrictStr]
    outputType: OutputType
    preview: Annotated[
        StrictStr, Field(description='Inline preview, possibly shortened.')
    ]
    searchText: Annotated[
        StrictStr | None,
        Field(
            description='Search text; filled by the recorder (S5), empty until then.'
        ),
    ] = None
    sizeBytes: Annotated[StrictInt, Field(ge=0)]
    truncated: StrictBool


class OutputReplacedPayload(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    cellId: StrictStr
    item: OutputItem
    outputIndex: Annotated[StrictInt, Field(ge=0)]
    runId: StrictStr


class OutputsCleared(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    authorConfidence: AuthorConfidence | None = None
    authorHint: AuthorHint | None = None
    branchId: Annotated[
        StrictStr, Field(description="Made by Blaym's service, never by a browser.")
    ]
    editor: Editor | None = None
    eventId: UUID
    explorationId: Annotated[StrictStr, Field(description="The notebook's history.")]
    links: EventLinks | None = None
    originId: Annotated[
        StrictStr,
        Field(
            description='One recorder instance (for example one browser tab, one kernel listener, one chat reader). Never an editor: that is `editor`.'
        ),
    ]
    payload: OutputsClearedPayload
    schemaVersion: Literal[2]
    tick: Annotated[
        StrictInt,
        Field(
            description='Dense running order for the whole history, from the writer.',
            ge=1,
        ),
    ]
    type: Literal['outputs_cleared']
    userId: Annotated[StrictStr, Field(description='"local" in the first version.')]
    wallTimeMs: Annotated[
        StrictInt,
        Field(
            description='Clock time in milliseconds; a label only, never used for order.',
            ge=0,
        ),
    ]
    workspaceId: Annotated[
        StrictStr, Field(description='"local" in the first version.')
    ]


class PrepareOutputsResponse(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    apiVersion: ApiVersion
    items: list[OutputItem]


class RecorderEvent10(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    authorConfidence: AuthorConfidence | None = None
    authorHint: AuthorHint | None = None
    editor: Editor | None = None
    eventId: UUID
    explorationId: Annotated[StrictStr, Field(description="The notebook's history.")]
    links: EventLinks | None = None
    originId: Annotated[
        StrictStr,
        Field(
            description='One recorder instance (for example one browser tab, one kernel listener, one chat reader). Never an editor: that is `editor`.'
        ),
    ]
    payload: RunStartedPayload
    schemaVersion: Literal[2]
    type: Literal['run_started']
    userId: Annotated[StrictStr, Field(description='"local" in the first version.')]
    wallTimeMs: Annotated[
        StrictInt,
        Field(
            description='Clock time in milliseconds; a label only, never used for order.',
            ge=0,
        ),
    ]
    workspaceId: Annotated[
        StrictStr, Field(description='"local" in the first version.')
    ]


class RecorderEvent11(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    authorConfidence: AuthorConfidence | None = None
    authorHint: AuthorHint | None = None
    editor: Editor | None = None
    eventId: UUID
    explorationId: Annotated[StrictStr, Field(description="The notebook's history.")]
    links: EventLinks | None = None
    originId: Annotated[
        StrictStr,
        Field(
            description='One recorder instance (for example one browser tab, one kernel listener, one chat reader). Never an editor: that is `editor`.'
        ),
    ]
    payload: RunFinishedPayload
    schemaVersion: Literal[2]
    type: Literal['run_finished']
    userId: Annotated[StrictStr, Field(description='"local" in the first version.')]
    wallTimeMs: Annotated[
        StrictInt,
        Field(
            description='Clock time in milliseconds; a label only, never used for order.',
            ge=0,
        ),
    ]
    workspaceId: Annotated[
        StrictStr, Field(description='"local" in the first version.')
    ]


class RecorderEvent13(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    authorConfidence: AuthorConfidence | None = None
    authorHint: AuthorHint | None = None
    editor: Editor | None = None
    eventId: UUID
    explorationId: Annotated[StrictStr, Field(description="The notebook's history.")]
    links: EventLinks | None = None
    originId: Annotated[
        StrictStr,
        Field(
            description='One recorder instance (for example one browser tab, one kernel listener, one chat reader). Never an editor: that is `editor`.'
        ),
    ]
    payload: OutputReplacedPayload
    schemaVersion: Literal[2]
    type: Literal['output_replaced']
    userId: Annotated[StrictStr, Field(description='"local" in the first version.')]
    wallTimeMs: Annotated[
        StrictInt,
        Field(
            description='Clock time in milliseconds; a label only, never used for order.',
            ge=0,
        ),
    ]
    workspaceId: Annotated[
        StrictStr, Field(description='"local" in the first version.')
    ]


class RecorderEvent16(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    authorConfidence: AuthorConfidence | None = None
    authorHint: AuthorHint | None = None
    editor: Editor | None = None
    eventId: UUID
    explorationId: Annotated[StrictStr, Field(description="The notebook's history.")]
    links: EventLinks | None = None
    originId: Annotated[
        StrictStr,
        Field(
            description='One recorder instance (for example one browser tab, one kernel listener, one chat reader). Never an editor: that is `editor`.'
        ),
    ]
    payload: KernelRestartedPayload
    schemaVersion: Literal[2]
    type: Literal['kernel_restarted']
    userId: Annotated[StrictStr, Field(description='"local" in the first version.')]
    wallTimeMs: Annotated[
        StrictInt,
        Field(
            description='Clock time in milliseconds; a label only, never used for order.',
            ge=0,
        ),
    ]
    workspaceId: Annotated[
        StrictStr, Field(description='"local" in the first version.')
    ]


class RecorderEvent20(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    authorConfidence: AuthorConfidence | None = None
    authorHint: AuthorHint | None = None
    editor: Editor | None = None
    eventId: UUID
    explorationId: Annotated[StrictStr, Field(description="The notebook's history.")]
    links: EventLinks | None = None
    originId: Annotated[
        StrictStr,
        Field(
            description='One recorder instance (for example one browser tab, one kernel listener, one chat reader). Never an editor: that is `editor`.'
        ),
    ]
    payload: ChatMessageAddedPayload
    schemaVersion: Literal[2]
    type: Literal['chat_message_added']
    userId: Annotated[StrictStr, Field(description='"local" in the first version.')]
    wallTimeMs: Annotated[
        StrictInt,
        Field(
            description='Clock time in milliseconds; a label only, never used for order.',
            ge=0,
        ),
    ]
    workspaceId: Annotated[
        StrictStr, Field(description='"local" in the first version.')
    ]


class RecorderEvent23(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    authorConfidence: AuthorConfidence | None = None
    authorHint: AuthorHint | None = None
    editor: Editor | None = None
    eventId: UUID
    explorationId: Annotated[StrictStr, Field(description="The notebook's history.")]
    links: EventLinks | None = None
    originId: Annotated[
        StrictStr,
        Field(
            description='One recorder instance (for example one browser tab, one kernel listener, one chat reader). Never an editor: that is `editor`.'
        ),
    ]
    payload: RecordingGapStartedPayload
    schemaVersion: Literal[2]
    type: Literal['recording_gap_started']
    userId: Annotated[StrictStr, Field(description='"local" in the first version.')]
    wallTimeMs: Annotated[
        StrictInt,
        Field(
            description='Clock time in milliseconds; a label only, never used for order.',
            ge=0,
        ),
    ]
    workspaceId: Annotated[
        StrictStr, Field(description='"local" in the first version.')
    ]


class RecorderEvent24(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    authorConfidence: AuthorConfidence | None = None
    authorHint: AuthorHint | None = None
    editor: Editor | None = None
    eventId: UUID
    explorationId: Annotated[StrictStr, Field(description="The notebook's history.")]
    links: EventLinks | None = None
    originId: Annotated[
        StrictStr,
        Field(
            description='One recorder instance (for example one browser tab, one kernel listener, one chat reader). Never an editor: that is `editor`.'
        ),
    ]
    payload: RecordingGapEndedPayload
    schemaVersion: Literal[2]
    type: Literal['recording_gap_ended']
    userId: Annotated[StrictStr, Field(description='"local" in the first version.')]
    wallTimeMs: Annotated[
        StrictInt,
        Field(
            description='Clock time in milliseconds; a label only, never used for order.',
            ge=0,
        ),
    ]
    workspaceId: Annotated[
        StrictStr, Field(description='"local" in the first version.')
    ]


class RecordingGapEnded(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    authorConfidence: AuthorConfidence | None = None
    authorHint: AuthorHint | None = None
    branchId: Annotated[
        StrictStr, Field(description="Made by Blaym's service, never by a browser.")
    ]
    editor: Editor | None = None
    eventId: UUID
    explorationId: Annotated[StrictStr, Field(description="The notebook's history.")]
    links: EventLinks | None = None
    originId: Annotated[
        StrictStr,
        Field(
            description='One recorder instance (for example one browser tab, one kernel listener, one chat reader). Never an editor: that is `editor`.'
        ),
    ]
    payload: RecordingGapEndedPayload
    schemaVersion: Literal[2]
    tick: Annotated[
        StrictInt,
        Field(
            description='Dense running order for the whole history, from the writer.',
            ge=1,
        ),
    ]
    type: Literal['recording_gap_ended']
    userId: Annotated[StrictStr, Field(description='"local" in the first version.')]
    wallTimeMs: Annotated[
        StrictInt,
        Field(
            description='Clock time in milliseconds; a label only, never used for order.',
            ge=0,
        ),
    ]
    workspaceId: Annotated[
        StrictStr, Field(description='"local" in the first version.')
    ]


class RecordingGapStarted(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    authorConfidence: AuthorConfidence | None = None
    authorHint: AuthorHint | None = None
    branchId: Annotated[
        StrictStr, Field(description="Made by Blaym's service, never by a browser.")
    ]
    editor: Editor | None = None
    eventId: UUID
    explorationId: Annotated[StrictStr, Field(description="The notebook's history.")]
    links: EventLinks | None = None
    originId: Annotated[
        StrictStr,
        Field(
            description='One recorder instance (for example one browser tab, one kernel listener, one chat reader). Never an editor: that is `editor`.'
        ),
    ]
    payload: RecordingGapStartedPayload
    schemaVersion: Literal[2]
    tick: Annotated[
        StrictInt,
        Field(
            description='Dense running order for the whole history, from the writer.',
            ge=1,
        ),
    ]
    type: Literal['recording_gap_started']
    userId: Annotated[StrictStr, Field(description='"local" in the first version.')]
    wallTimeMs: Annotated[
        StrictInt,
        Field(
            description='Clock time in milliseconds; a label only, never used for order.',
            ge=0,
        ),
    ]
    workspaceId: Annotated[
        StrictStr, Field(description='"local" in the first version.')
    ]


class ResolveCellRevisionResponse(
    RootModel[
        ResolveCellRevisionOk
        | ResolveCellRevisionUnknownCell
        | ResolveCellRevisionCodeDiffers
        | ResolveCellRevisionUnknownHistory
    ]
):
    root: (
        ResolveCellRevisionOk
        | ResolveCellRevisionUnknownCell
        | ResolveCellRevisionCodeDiffers
        | ResolveCellRevisionUnknownHistory
    )


class RunFinished(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    authorConfidence: AuthorConfidence | None = None
    authorHint: AuthorHint | None = None
    branchId: Annotated[
        StrictStr, Field(description="Made by Blaym's service, never by a browser.")
    ]
    editor: Editor | None = None
    eventId: UUID
    explorationId: Annotated[StrictStr, Field(description="The notebook's history.")]
    links: EventLinks | None = None
    originId: Annotated[
        StrictStr,
        Field(
            description='One recorder instance (for example one browser tab, one kernel listener, one chat reader). Never an editor: that is `editor`.'
        ),
    ]
    payload: RunFinishedPayload
    schemaVersion: Literal[2]
    tick: Annotated[
        StrictInt,
        Field(
            description='Dense running order for the whole history, from the writer.',
            ge=1,
        ),
    ]
    type: Literal['run_finished']
    userId: Annotated[StrictStr, Field(description='"local" in the first version.')]
    wallTimeMs: Annotated[
        StrictInt,
        Field(
            description='Clock time in milliseconds; a label only, never used for order.',
            ge=0,
        ),
    ]
    workspaceId: Annotated[
        StrictStr, Field(description='"local" in the first version.')
    ]


class RunOutputs(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    clearPending: Annotated[
        StrictBool | None,
        Field(
            description='Set by `outputs_cleared` with `wait: true`; the next `output_added` for the run replaces `items` and clears the flag (Jupyter\'s "clear and wait").'
        ),
    ] = None
    items: list[OutputItem]
    runId: Annotated[
        StrictStr,
        Field(
            description="For outputs that arrived with an inserted cell and no run, `pasted:<eventId>` (the `cell_inserted` event's id), made by the rebuilder, never by a recorder. For outputs that arrived in a `notebook_snapshot` (the editor's statement of the whole notebook), `snapshot:<eventId>` (the snapshot event's id), made by the recorder."
        ),
    ]


class RunStarted(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    authorConfidence: AuthorConfidence | None = None
    authorHint: AuthorHint | None = None
    branchId: Annotated[
        StrictStr, Field(description="Made by Blaym's service, never by a browser.")
    ]
    editor: Editor | None = None
    eventId: UUID
    explorationId: Annotated[StrictStr, Field(description="The notebook's history.")]
    links: EventLinks | None = None
    originId: Annotated[
        StrictStr,
        Field(
            description='One recorder instance (for example one browser tab, one kernel listener, one chat reader). Never an editor: that is `editor`.'
        ),
    ]
    payload: RunStartedPayload
    schemaVersion: Literal[2]
    tick: Annotated[
        StrictInt,
        Field(
            description='Dense running order for the whole history, from the writer.',
            ge=1,
        ),
    ]
    type: Literal['run_started']
    userId: Annotated[StrictStr, Field(description='"local" in the first version.')]
    wallTimeMs: Annotated[
        StrictInt,
        Field(
            description='Clock time in milliseconds; a label only, never used for order.',
            ge=0,
        ),
    ]
    workspaceId: Annotated[
        StrictStr, Field(description='"local" in the first version.')
    ]


class RunState(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    cellId: StrictStr
    cellRevision: Annotated[
        StrictInt,
        Field(
            description='The revision that was sent, even if the cell was edited during the run.',
            ge=1,
        ),
    ]
    endedTick: Annotated[
        StrictInt | None,
        Field(
            description='Tick of the finish, or of the restart that left it unfinished.',
            ge=1,
        ),
    ] = None
    runCount: Annotated[StrictInt, Field(ge=1)]
    runId: StrictStr
    startedTick: Annotated[StrictInt, Field(ge=1)]
    status: RunStatus


class SearchHit(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    branchId: StrictStr
    kind: SearchHitKind
    snippet: Annotated[
        StrictStr, Field(description='A short piece of the matching text.')
    ]
    tick: Annotated[StrictInt, Field(ge=1)]


class SearchResponse(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    apiVersion: ApiVersion
    hits: list[SearchHit]


class TimelineIndexResponse(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    apiVersion: ApiVersion
    authors: list[AuthorHint]
    cellIds: list[StrictStr | None]
    confidences: list[AuthorConfidence | None]
    kinds: list[TimelineKind]
    nextTick: Annotated[StrictInt | None, Field(ge=1)] = None
    runIds: list[StrictStr | None]
    ticks: list[Tick]
    timesMs: Annotated[
        list[StrictFloat],
        Field(description='Clock time of each event (a label, not an order).'),
    ]
    truncated: StrictBool


class CellInsertedPayload(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    cellId: StrictStr
    cellType: CellType
    code: StrictStr
    index: Annotated[StrictInt, Field(ge=0)]
    metadata: dict[str, Any] | None = None
    outputs: Annotated[
        list[OutputItem] | None,
        Field(
            description="For cells that arrive with outputs and no run (a paste, or an AI tool inserting a cell with outputs). Shown as the cell's outputs, linked to no run: the rebuilder groups them under `pasted:<eventId>` (see `RunOutputs.runId`)."
        ),
    ] = None
    revision: Annotated[StrictInt, Field(description='Always 1 for a new cell.', ge=1)]


class ChatMessageAdded(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    authorConfidence: AuthorConfidence | None = None
    authorHint: AuthorHint | None = None
    branchId: Annotated[
        StrictStr, Field(description="Made by Blaym's service, never by a browser.")
    ]
    editor: Editor | None = None
    eventId: UUID
    explorationId: Annotated[StrictStr, Field(description="The notebook's history.")]
    links: EventLinks | None = None
    originId: Annotated[
        StrictStr,
        Field(
            description='One recorder instance (for example one browser tab, one kernel listener, one chat reader). Never an editor: that is `editor`.'
        ),
    ]
    payload: ChatMessageAddedPayload
    schemaVersion: Literal[2]
    tick: Annotated[
        StrictInt,
        Field(
            description='Dense running order for the whole history, from the writer.',
            ge=1,
        ),
    ]
    type: Literal['chat_message_added']
    userId: Annotated[StrictStr, Field(description='"local" in the first version.')]
    wallTimeMs: Annotated[
        StrictInt,
        Field(
            description='Clock time in milliseconds; a label only, never used for order.',
            ge=0,
        ),
    ]
    workspaceId: Annotated[
        StrictStr, Field(description='"local" in the first version.')
    ]


class CreateBranchOk(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    branch: OutlineBranch
    status: Literal['ok']


class CreateBranchResponse(RootModel[CreateBranchOk | CreateBranchRefused]):
    root: CreateBranchOk | CreateBranchRefused


class HistoryAdvanced(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    branchId: Annotated[
        StrictStr, Field(description='The branch that received the new event.')
    ]
    explorationId: StrictStr
    newBranch: Annotated[
        OutlineBranch | None,
        Field(
            description='Present when the new event created a branch. Its entry already carries the spans it inherits.'
        ),
    ] = None
    runStarted: Annotated[
        StrictStr | None,
        Field(
            description='Present when the new event started a run: the id of the run whose span starts at this tick on `branchId`.'
        ),
    ] = None
    runsEnded: Annotated[
        list[StrictStr] | None,
        Field(
            description="Present when the new event closed runs: the ids of the runs whose span on `branchId`'s line ends at this tick. A finished run closes one; a kernel restart closes every run still open on that line, so it may list several. Only runs listed in that branch's `runSpans` are meant."
        ),
    ] = None
    tick: Annotated[StrictInt, Field(description='The new highest stored tick.', ge=1)]


class HistoryOutline(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    branches: list[OutlineBranch]
    explorationId: StrictStr
    highestTick: Annotated[
        StrictInt,
        Field(
            description='The highest stored tick that has no missing tick below it.',
            ge=1,
        ),
    ]
    rootBranchId: StrictStr
    schemaVersion: Literal[2]


class KernelRestarted(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    authorConfidence: AuthorConfidence | None = None
    authorHint: AuthorHint | None = None
    branchId: Annotated[
        StrictStr, Field(description="Made by Blaym's service, never by a browser.")
    ]
    editor: Editor | None = None
    eventId: UUID
    explorationId: Annotated[StrictStr, Field(description="The notebook's history.")]
    links: EventLinks | None = None
    originId: Annotated[
        StrictStr,
        Field(
            description='One recorder instance (for example one browser tab, one kernel listener, one chat reader). Never an editor: that is `editor`.'
        ),
    ]
    payload: KernelRestartedPayload
    schemaVersion: Literal[2]
    tick: Annotated[
        StrictInt,
        Field(
            description='Dense running order for the whole history, from the writer.',
            ge=1,
        ),
    ]
    type: Literal['kernel_restarted']
    userId: Annotated[StrictStr, Field(description='"local" in the first version.')]
    wallTimeMs: Annotated[
        StrictInt,
        Field(
            description='Clock time in milliseconds; a label only, never used for order.',
            ge=0,
        ),
    ]
    workspaceId: Annotated[
        StrictStr, Field(description='"local" in the first version.')
    ]


class NotebookCell(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    cellId: StrictStr
    cellType: CellType
    code: StrictStr
    metadata: dict[str, Any]
    outputs: list[RunOutputs]
    revision: Annotated[StrictInt, Field(ge=1)]
    runCount: Annotated[StrictInt | None, Field(ge=1)] = None


class NotebookSnapshotPayload(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    cells: list[NotebookCell]
    kernelName: StrictStr
    language: StrictStr
    notebookMetadata: dict[str, Any]
    path: StrictStr


class NotebookState(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    cells: list[NotebookCell]
    metadata: dict[str, Any]
    path: StrictStr


class OutputAddedPayload(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    cellId: StrictStr
    item: OutputItem
    outputIndex: Annotated[StrictInt, Field(ge=0)]
    runId: StrictStr


class OutputReplaced(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    authorConfidence: AuthorConfidence | None = None
    authorHint: AuthorHint | None = None
    branchId: Annotated[
        StrictStr, Field(description="Made by Blaym's service, never by a browser.")
    ]
    editor: Editor | None = None
    eventId: UUID
    explorationId: Annotated[StrictStr, Field(description="The notebook's history.")]
    links: EventLinks | None = None
    originId: Annotated[
        StrictStr,
        Field(
            description='One recorder instance (for example one browser tab, one kernel listener, one chat reader). Never an editor: that is `editor`.'
        ),
    ]
    payload: OutputReplacedPayload
    schemaVersion: Literal[2]
    tick: Annotated[
        StrictInt,
        Field(
            description='Dense running order for the whole history, from the writer.',
            ge=1,
        ),
    ]
    type: Literal['output_replaced']
    userId: Annotated[StrictStr, Field(description='"local" in the first version.')]
    wallTimeMs: Annotated[
        StrictInt,
        Field(
            description='Clock time in milliseconds; a label only, never used for order.',
            ge=0,
        ),
    ]
    workspaceId: Annotated[
        StrictStr, Field(description='"local" in the first version.')
    ]


class RebuiltState(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    chat: list[ChatMessageState]
    detachedOutputs: Annotated[
        list[RunOutputs],
        Field(
            description='Output groups of runs whose cell no longer exists, shown in review as "output from a deleted cell". A run\'s output events address the run, so output that arrives after its cell was deleted is kept here, not dropped.'
        ),
    ]
    gaps: list[GapState]
    kernel: KernelState
    lastOutsideChange: OutsideChangeMarker | None = None
    notebook: NotebookState
    position: StatePosition
    runs: list[RunState]
    schemaVersion: Literal[2]


class RecorderEvent1(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    authorConfidence: AuthorConfidence | None = None
    authorHint: AuthorHint | None = None
    editor: Editor | None = None
    eventId: UUID
    explorationId: Annotated[StrictStr, Field(description="The notebook's history.")]
    links: EventLinks | None = None
    originId: Annotated[
        StrictStr,
        Field(
            description='One recorder instance (for example one browser tab, one kernel listener, one chat reader). Never an editor: that is `editor`.'
        ),
    ]
    payload: NotebookSnapshotPayload
    schemaVersion: Literal[2]
    type: Literal['notebook_snapshot']
    userId: Annotated[StrictStr, Field(description='"local" in the first version.')]
    wallTimeMs: Annotated[
        StrictInt,
        Field(
            description='Clock time in milliseconds; a label only, never used for order.',
            ge=0,
        ),
    ]
    workspaceId: Annotated[
        StrictStr, Field(description='"local" in the first version.')
    ]


class RecorderEvent2(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    authorConfidence: AuthorConfidence | None = None
    authorHint: AuthorHint | None = None
    editor: Editor | None = None
    eventId: UUID
    explorationId: Annotated[StrictStr, Field(description="The notebook's history.")]
    links: EventLinks | None = None
    originId: Annotated[
        StrictStr,
        Field(
            description='One recorder instance (for example one browser tab, one kernel listener, one chat reader). Never an editor: that is `editor`.'
        ),
    ]
    payload: CellInsertedPayload
    schemaVersion: Literal[2]
    type: Literal['cell_inserted']
    userId: Annotated[StrictStr, Field(description='"local" in the first version.')]
    wallTimeMs: Annotated[
        StrictInt,
        Field(
            description='Clock time in milliseconds; a label only, never used for order.',
            ge=0,
        ),
    ]
    workspaceId: Annotated[
        StrictStr, Field(description='"local" in the first version.')
    ]


class RecorderEvent12(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    authorConfidence: AuthorConfidence | None = None
    authorHint: AuthorHint | None = None
    editor: Editor | None = None
    eventId: UUID
    explorationId: Annotated[StrictStr, Field(description="The notebook's history.")]
    links: EventLinks | None = None
    originId: Annotated[
        StrictStr,
        Field(
            description='One recorder instance (for example one browser tab, one kernel listener, one chat reader). Never an editor: that is `editor`.'
        ),
    ]
    payload: OutputAddedPayload
    schemaVersion: Literal[2]
    type: Literal['output_added']
    userId: Annotated[StrictStr, Field(description='"local" in the first version.')]
    wallTimeMs: Annotated[
        StrictInt,
        Field(
            description='Clock time in milliseconds; a label only, never used for order.',
            ge=0,
        ),
    ]
    workspaceId: Annotated[
        StrictStr, Field(description='"local" in the first version.')
    ]


class RecorderEvent19(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    authorConfidence: AuthorConfidence | None = None
    authorHint: Literal['outside']
    editor: Editor | None = None
    eventId: UUID
    explorationId: Annotated[StrictStr, Field(description="The notebook's history.")]
    links: EventLinks | None = None
    originId: Annotated[
        StrictStr,
        Field(
            description='One recorder instance (for example one browser tab, one kernel listener, one chat reader). Never an editor: that is `editor`.'
        ),
    ]
    payload: NotebookSnapshotPayload
    schemaVersion: Literal[2]
    type: Literal['changed_outside_editor']
    userId: Annotated[StrictStr, Field(description='"local" in the first version.')]
    wallTimeMs: Annotated[
        StrictInt,
        Field(
            description='Clock time in milliseconds; a label only, never used for order.',
            ge=0,
        ),
    ]
    workspaceId: Annotated[
        StrictStr, Field(description='"local" in the first version.')
    ]


class RecorderEvent(
    RootModel[
        RecorderEvent1
        | RecorderEvent2
        | RecorderEvent3
        | RecorderEvent4
        | RecorderEvent5
        | RecorderEvent6
        | RecorderEvent7
        | RecorderEvent8
        | RecorderEvent9
        | RecorderEvent10
        | RecorderEvent11
        | RecorderEvent12
        | RecorderEvent13
        | RecorderEvent14
        | RecorderEvent15
        | RecorderEvent16
        | RecorderEvent17
        | RecorderEvent18
        | RecorderEvent19
        | RecorderEvent20
        | RecorderEvent21
        | RecorderEvent22
        | RecorderEvent23
        | RecorderEvent24
    ]
):
    root: (
        RecorderEvent1
        | RecorderEvent2
        | RecorderEvent3
        | RecorderEvent4
        | RecorderEvent5
        | RecorderEvent6
        | RecorderEvent7
        | RecorderEvent8
        | RecorderEvent9
        | RecorderEvent10
        | RecorderEvent11
        | RecorderEvent12
        | RecorderEvent13
        | RecorderEvent14
        | RecorderEvent15
        | RecorderEvent16
        | RecorderEvent17
        | RecorderEvent18
        | RecorderEvent19
        | RecorderEvent20
        | RecorderEvent21
        | RecorderEvent22
        | RecorderEvent23
        | RecorderEvent24
    )


class CellInserted(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    authorConfidence: AuthorConfidence | None = None
    authorHint: AuthorHint | None = None
    branchId: Annotated[
        StrictStr, Field(description="Made by Blaym's service, never by a browser.")
    ]
    editor: Editor | None = None
    eventId: UUID
    explorationId: Annotated[StrictStr, Field(description="The notebook's history.")]
    links: EventLinks | None = None
    originId: Annotated[
        StrictStr,
        Field(
            description='One recorder instance (for example one browser tab, one kernel listener, one chat reader). Never an editor: that is `editor`.'
        ),
    ]
    payload: CellInsertedPayload
    schemaVersion: Literal[2]
    tick: Annotated[
        StrictInt,
        Field(
            description='Dense running order for the whole history, from the writer.',
            ge=1,
        ),
    ]
    type: Literal['cell_inserted']
    userId: Annotated[StrictStr, Field(description='"local" in the first version.')]
    wallTimeMs: Annotated[
        StrictInt,
        Field(
            description='Clock time in milliseconds; a label only, never used for order.',
            ge=0,
        ),
    ]
    workspaceId: Annotated[
        StrictStr, Field(description='"local" in the first version.')
    ]


class ChangedOutsideEditor(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    authorConfidence: AuthorConfidence | None = None
    authorHint: Literal['outside']
    branchId: Annotated[
        StrictStr, Field(description="Made by Blaym's service, never by a browser.")
    ]
    editor: Editor | None = None
    eventId: UUID
    explorationId: Annotated[StrictStr, Field(description="The notebook's history.")]
    links: EventLinks | None = None
    originId: Annotated[
        StrictStr,
        Field(
            description='One recorder instance (for example one browser tab, one kernel listener, one chat reader). Never an editor: that is `editor`.'
        ),
    ]
    payload: NotebookSnapshotPayload
    schemaVersion: Literal[2]
    tick: Annotated[
        StrictInt,
        Field(
            description='Dense running order for the whole history, from the writer.',
            ge=1,
        ),
    ]
    type: Literal['changed_outside_editor']
    userId: Annotated[StrictStr, Field(description='"local" in the first version.')]
    wallTimeMs: Annotated[
        StrictInt,
        Field(
            description='Clock time in milliseconds; a label only, never used for order.',
            ge=0,
        ),
    ]
    workspaceId: Annotated[
        StrictStr, Field(description='"local" in the first version.')
    ]


class IngestRequest(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    editor: Annotated[
        Editor,
        Field(
            description='The editor sending the events; the claimant of the one-recorder lease.'
        ),
    ]
    events: list[RecorderEvent]
    explorationId: StrictStr
    instanceId: Annotated[
        StrictStr,
        Field(
            description='The recorder instance sending the events (for example one browser tab).'
        ),
    ]
    targetBranchId: StrictStr | None = None


class NotebookSnapshot(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    authorConfidence: AuthorConfidence | None = None
    authorHint: AuthorHint | None = None
    branchId: Annotated[
        StrictStr, Field(description="Made by Blaym's service, never by a browser.")
    ]
    editor: Editor | None = None
    eventId: UUID
    explorationId: Annotated[StrictStr, Field(description="The notebook's history.")]
    links: EventLinks | None = None
    originId: Annotated[
        StrictStr,
        Field(
            description='One recorder instance (for example one browser tab, one kernel listener, one chat reader). Never an editor: that is `editor`.'
        ),
    ]
    payload: NotebookSnapshotPayload
    schemaVersion: Literal[2]
    tick: Annotated[
        StrictInt,
        Field(
            description='Dense running order for the whole history, from the writer.',
            ge=1,
        ),
    ]
    type: Literal['notebook_snapshot']
    userId: Annotated[StrictStr, Field(description='"local" in the first version.')]
    wallTimeMs: Annotated[
        StrictInt,
        Field(
            description='Clock time in milliseconds; a label only, never used for order.',
            ge=0,
        ),
    ]
    workspaceId: Annotated[
        StrictStr, Field(description='"local" in the first version.')
    ]


class OutputAdded(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    authorConfidence: AuthorConfidence | None = None
    authorHint: AuthorHint | None = None
    branchId: Annotated[
        StrictStr, Field(description="Made by Blaym's service, never by a browser.")
    ]
    editor: Editor | None = None
    eventId: UUID
    explorationId: Annotated[StrictStr, Field(description="The notebook's history.")]
    links: EventLinks | None = None
    originId: Annotated[
        StrictStr,
        Field(
            description='One recorder instance (for example one browser tab, one kernel listener, one chat reader). Never an editor: that is `editor`.'
        ),
    ]
    payload: OutputAddedPayload
    schemaVersion: Literal[2]
    tick: Annotated[
        StrictInt,
        Field(
            description='Dense running order for the whole history, from the writer.',
            ge=1,
        ),
    ]
    type: Literal['output_added']
    userId: Annotated[StrictStr, Field(description='"local" in the first version.')]
    wallTimeMs: Annotated[
        StrictInt,
        Field(
            description='Clock time in milliseconds; a label only, never used for order.',
            ge=0,
        ),
    ]
    workspaceId: Annotated[
        StrictStr, Field(description='"local" in the first version.')
    ]


class RebuildOk(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    state: RebuiltState
    status: Literal['ok']


class BlaymEvent(
    RootModel[
        NotebookSnapshot
        | CellInserted
        | CellDeleted
        | CellMoved
        | CellTypeChanged
        | CellOutputsCleared
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
        | RecordingGapEnded
    ]
):
    root: Annotated[
        NotebookSnapshot
        | CellInserted
        | CellDeleted
        | CellMoved
        | CellTypeChanged
        | CellOutputsCleared
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
        | RecordingGapEnded,
        Field(description='Every event Blaym records, told apart by `type`.'),
    ]


class EventsBetweenResponse(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    apiVersion: ApiVersion
    events: list[BlaymEvent]
    nextTick: Annotated[StrictInt | None, Field(ge=1)] = None
    truncated: StrictBool


class EventsSinceResponse(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    apiVersion: ApiVersion
    events: list[BlaymEvent]
    outline: HistoryOutline


class RebuildConflict(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    eventId: StrictStr
    first: Annotated[BlaymEvent, Field(description='The event as first stored.')]
    second: Annotated[
        BlaymEvent,
        Field(description='The event with the same id but different content.'),
    ]
    status: Literal['conflict']


class RebuildResult(
    RootModel[
        RebuildOk
        | RebuildMissingEvents
        | RebuildConflict
        | RebuildInvalidRevision
        | RebuildUnknownCell
        | RebuildUnknownBranch
        | RebuildLineageLoop
        | RebuildInvalidEvent
    ]
):
    root: (
        RebuildOk
        | RebuildMissingEvents
        | RebuildConflict
        | RebuildInvalidRevision
        | RebuildUnknownCell
        | RebuildUnknownBranch
        | RebuildLineageLoop
        | RebuildInvalidEvent
    )


class IngestRefused(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    detail: Annotated[
        StrictStr, Field(description='A short plain-language explanation.')
    ]
    eventId: StrictStr
    reason: IngestRefusalReason
    rebuild: RebuildResult | None = None
    status: Literal['refused']


class IngestOutcome(RootModel[IngestAccepted | IngestRefused]):
    root: IngestAccepted | IngestRefused


class IngestResponse(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
    )
    apiVersion: ApiVersion
    outcomes: list[IngestOutcome]
