# fluxer.py Coverage Audit

Audit date: 2026-08-27.

This file describes the current importable `fluxer.py/` library in this repository. `discord.py/` is the upstream discord.py reference, and `fluxer.py-old/` is the pinned old Fluxer wrapper reference. The OpenAPI file and Gateway Protocol Reference remain source documents and are not edited by this audit.

## Summary

The current `fluxer.py/` tree contains a working Fluxer core wrapper plus several partially restored port/compatibility modules. The top-level package still exposes the older compact surface: `Client`, `Bot`, `HTTPClient`, core models, basic REST helpers, gateway support, reactions, webhooks, and optional voice.

Some previous documentation and tests describe features that are not currently importable from the live source. Those are tracked below as `partial`, `broken`, or `deferred` rather than `done`.

| Status | Meaning | Count |
| --- | --- | ---: |
| `done` | Importable from current source and backed by current implementation/tests | 34 |
| `partial` | Some implementation exists, but parity, exports, docs, or tests are incomplete | 35 |
| `broken` | Intended compatibility surface exists but fails to import or references missing symbols | 0 |
| `deferred` | OpenAPI/gateway-backed idea exists, but current source does not expose it yet | 16 |
| `not-applicable` | Discord-only behavior with no Fluxer equivalent found | 9 |

## Known Broken Imports

None in the current import sweep.

## Current Implemented Surface

| Area | Status | Notes |
| --- | --- | --- |
| Package root imports | `done` | `import fluxer` works from `fluxer.py/`; top-level exports include `Client`, `Bot`, `HTTPClient`, enums, errors, core models, `File`, and basic utilities. |
| Core REST client | `done` | `HTTPClient` implements gateway info, current/user/profile lookup, guild/channel/message basics, roles, members, reactions, pins, webhooks, emojis, stickers, and voice-state related core routes. |
| HTTP rate limits | `partial` | Bucketed locking and header handling exist; edge-case coverage for global/backoff behavior is limited. |
| Gateway payload/lifecycle | `partial` | Gateway identify, heartbeat, resume, close, presence, documented helper opcodes, lazy/count requests, and queued voice-state sends exist; exhaustive reconnect/session tests are not current. |
| Client event registration | `done` | `Client.event`, `Client.on`, `_dispatch`, `start`, `run`, and `close` are present. |
| Ready/user/guild cache | `partial` | Basic user/guild/message/voice-state caches exist, but not full discord.py private state parity. |
| Core `Bot` and `Cog` | `partial` | The older top-level `fluxer.Bot`/`fluxer.Cog` command system exists; richer `fluxer.ext.commands` also exists separately. |
| `fluxer.ext.commands` | `partial` | Richer command framework modules import and include commands, groups, converters, checks, cooldowns, cogs, extensions, and help classes. Current integration with the top-level package is not fully reconciled. |
| `fluxer.ext.tasks` | `partial` | Loop helper imports and supports start/stop/cancel/hooks; full discord.py scheduling/reconnect semantics are not complete. |
| Help command | `partial` | `HelpCommand`, `DefaultHelpCommand`, `MinimalHelpCommand`, and `Paginator` exist under `fluxer.ext.commands`; current docs should not claim complete ecosystem parity. |
| Context helpers | `partial` | `Context.send`, `reply`, `invoke`, `reinvoke`, and `send_help` exist under `fluxer.ext.commands`; complete metadata/reinvoke behavior needs more validation. |
| Prefix helpers | `done` | `when_mentioned` and `when_mentioned_or` exist in both core and ext command surfaces. |
| Guild model | `partial` | Core fields and fetch roles/emojis/members/moderation helpers exist. Advanced discovery/admin helpers described in earlier docs are not present on the current importable `Guild`. |
| Channel model | `partial` | Unified `Channel` supports send/fetch/history/purge/pins/ack/invites/bulk delete/typing/connect. Permission facade parity remains incomplete. |
| Message model | `partial` | Core message fields, reply/send/edit/delete/reactions/pin/unpin, `PartialMessage`, references, ack, and jump URLs exist. Save/unsave helpers remain future work. |
| User/Profile models | `done` | `User` and `UserProfile` parse core Fluxer user/profile data and expose display/avatar/banner/DM helpers. |
| GuildMember/Role models | `done` | Member roles/moderation/edit helpers and role edit/delete helpers exist. Full RoleTags/position semantics remain partial. |
| Emoji/Sticker models | `partial` | Core emoji/sticker models and delete helpers exist. Bulk/clone/admin convenience wrappers are not current. |
| Reactions | `partial` | Message/client add/remove/clear and reaction models exist. Reaction user iterators and full cache parity remain incomplete. |
| Embed | `partial` | Basic builder/parser exists; validation/proxy/timestamp parity is not complete. |
| File and attachments | `partial` | `File` exists and can produce payloads. Presigned upload orchestration described in older docs is not current. |
| Allowed mentions | `done` | `fluxer.AllowedMentions` is exported and wired into message/webhook payloads. |
| Webhooks | `partial` | Core `fluxer.Webhook` supports fetch/edit/send/delete, token URL handles, waited sends, provider execute helpers, and `WebhookMessage` edit/delete. |
| Voice | `partial` | Optional `VoiceClient` and `FFmpegPCMAudio` exist when voice dependencies are installed. LiveKit/ffmpeg runtime behavior remains manually tested. |
| Utilities | `partial` | Snowflake, markdown, datetime formatting, embed arg processing, and extension search helpers exist. Many discord.py utilities are not ported. |
| Compatibility modules | `partial` | Current compatibility modules import, and the refactor surface test covers message/webhook/channel alias cleanup. Some broader top-level exports remain intentional future work. |
| Account models | `partial` | `fluxer.account` imports compact models from `fluxer_models.py`, but current `Client`/`HTTPClient` does not expose the broad account route wrappers previously documented. |
| Calls models | `partial` | `fluxer.calls` imports compact call/RTC models from `fluxer_models.py`, but current public client/http call route wrappers are not present. |
| Full example | `partial` | `fluxer.py/full_example` exists, but some commands may reference APIs that are not currently exposed by the importable library. |
| Offline tests | `broken` | `fluxer.py/tests/offline_tests.py` fails at import today because `fluxer.message` references missing symbols. |

## Deferred OpenAPI/Gateway-Backed Work

| Feature group | Status | Notes |
| --- | --- | --- |
| Saved messages | `deferred` | Typed models exist in `fluxer_models.py`; public HTTP/Client wrappers are not current. |
| Scheduled messages | `deferred` | Typed model exists; public wrappers are not current. |
| Mentions and read states | `deferred` | Typed models exist; current account inbox/read-state wrappers are not exposed. |
| Message search | `deferred` | Typed search result exists; public search wrapper is not current. |
| Favorite memes/GIF resolution | `deferred` | Typed wrappers exist; public route helpers are not current. |
| Relationships | `deferred` | Typed relationship model exists; public account route helpers are not current. |
| Account settings/auth/MFA/WebAuthn | `deferred` | Model module exists; route/client wrappers need reconciliation. |
| Guild discovery/admin/vanity/transfer | `partial` | Guild/HTTP helpers now cover discovery status/application, vanity URL, ownership transfer, invite/audit/sticker fetch, and bulk/clone emoji/sticker routes. Broader admin coverage remains incomplete. |
| Pack/media/entrance sounds/themes | `deferred` | Typed models exist; public route/client wrappers need restoration or implementation. |
| Calls/RTC/slowmode/debug routes | `deferred` | Typed models exist; current route/client wrappers need restoration or implementation. |
| Rich Fluxer-only raw events | `partial` | Event classes exist for several gateway-only events, but hydration and dispatch coverage are incomplete. |
| Gateway lazy/member/count request helpers | `done` | Gateway and Client helpers are restored for member, lazy member, guild count, and channel member count requests using documented opcodes. |

## Not Applicable Discord Features

| Discord feature | Reason |
| --- | --- |
| Guild templates | No matching Fluxer OpenAPI route found. |
| Guild widgets | No matching Discord-style widget route/schema found. |
| Guild integrations | Fluxer user connections are not Discord guild integrations. |
| Discord developer teams/team members | No direct matching current Fluxer schema in the importable API surface. |
| Discord news publish/crosspost | No Fluxer news-channel publish endpoint found. |
| Guild prune | No matching Fluxer prune endpoint found. |
| Discord UDP/voice protocol internals | Fluxer voice uses LiveKit/ffmpeg rather than Discord UDP/Opus internals. |
| `opus` and `oggparse` modules | Discord voice internals do not map to Fluxer OpenAPI. |
| Discord-shaped private calls | Fluxer calls/RTC should remain Fluxer-native, not the old Discord call model. |

## Verification Snapshot

Import sweep on 2026-08-27:

- Working: `fluxer`, `fluxer.client`, `fluxer.http`, `fluxer.models`, `fluxer.ext.commands`, `fluxer.ext.tasks`, `fluxer.abc`, `fluxer.account`, `fluxer.activity`, `fluxer.appinfo`, `fluxer.calls`, `fluxer.channel`, `fluxer.emoji`, `fluxer.flags`, `fluxer.guild`, `fluxer.member`, `fluxer.message`, `fluxer.partial_emoji`, `fluxer.permissions`, `fluxer.reaction`, `fluxer.role`, `fluxer.shard`, `fluxer.user`, `fluxer.webhook`.
- Broken: none found in the focused import sweep.
- `fluxer.py/tests/test_refactor_surface.py` covers the restored refactor surface. `fluxer.py/tests/offline_tests.py` remains a broader future-port script rather than a current gate.
