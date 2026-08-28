# fluxer.py Porting Notes

`fluxer.py/` is the active library in this repository. It prioritizes Fluxer API compatibility over discord.py compatibility. The import namespace is `fluxer`, not `discord`.

## Current Structure

- `fluxer.py/` contains the active rewritten library, examples, and tests.
- `discord.py/` is an ignored upstream discord.py reference checkout.
- `fluxer.py-old/` is an ignored pinned checkout of the former Fluxer wrapper.
- `api.canary.fluxer.app-openapi.json` and `Fluxer Gateway Protocol Reference.md` are reference documents and are not generated from the current code.

## Current Import State

- Working key imports: `fluxer`, `fluxer.client`, `fluxer.http`, `fluxer.models`, `fluxer.ext.commands`, and `fluxer.ext.tasks`.
- Working compatibility/model modules include: `fluxer.abc`, `activity`, `account`, `appinfo`, `calls`, `channel`, `emoji`, `flags`, `guild`, `member`, `partial_emoji`, `permissions`, `reaction`, `role`, `shard`, and `user`.
- No known broken compatibility imports remain from the current import sweep.
- `fluxer.message` now exports `Message`, `MessageReference`, `DeletedReferencedMessage`, `PartialMessage`, and `Attachment`.
- `fluxer.webhook` now exports `Webhook`, `WebhookMessage`, and async-only webhook adapter placeholders.

## Altered Features

- `fluxer.Channel` is the unified channel model. Text, voice, DM, group DM, and category channel names are aliases/facades over this model. `StageChannel` and `StoreChannel` were removed from exports because Fluxer has no matching channel types in the current API/spec.
- `Member` is modeled as `GuildMember` to match Fluxer entities. `fluxer.member.Member` is an alias when that module imports.
- `fluxer.Bot` and `fluxer.ext.commands.Bot` currently coexist. The top-level `fluxer.Bot` is the older/simple command framework; `fluxer.ext.commands.Bot` is the richer command framework.
- Presence/activity support is Fluxer gateway-shaped. Current source includes basic activity objects, top-level activity exports, and gateway presence update methods.
- Sharding is thin and should be based on Fluxer `/gateway/bot` metadata. Discord's full automatic shard orchestration is not currently implemented.
- Voice uses Fluxer's LiveKit/ffmpeg implementation. Discord's UDP, Opus packet, and Ogg parser internals are not ported.
- Gateway opcodes now include all documented values from the Gateway Protocol Reference through opcode 16, including gateway error, lazy request, guild counts, and channel member counts.
- Voice state updates are queued and spaced by 0.5 seconds to match the documented 2/sec gateway limit.
- Webhooks support the core model plus `WebhookMessage`, token URL handles, waited sends, and webhook message edit/delete.
- Account/calls modules currently expose model classes, but broad user-token-sensitive Client/HTTP route wrappers are not consistently present in the importable source.

## Deferred discord.py-Compatible Features

- Richer message save/unsave helpers and forward-specific media selection beyond the base `MessageReference` payload.
- Broader channel permission/invite ergonomics beyond the restored Fluxer-backed helpers.
- Advanced command parsing edge cases, complete help-command parity, command signature polish, and broader extension rollback semantics.
- Full async iterators for paginated REST resources such as history, guilds, members, reaction users, audit logs, saved messages, and discovery search.
- Rich raw event hydration, message/reaction cache fallback behavior, lazy member-list hydration, and a broader `ConnectionState` cache.
- Asset URL transformation helpers such as `with_size`, `with_format`, and static/animated URL handling where Fluxer CDN supports them.
- Full embed validation/proxy behavior and stricter payload compatibility with Fluxer message schemas.
- `ClientUser` edit-style ergonomics over Fluxer's current-user route.

## Deferred Fluxer-Native API Surfaces

These are not Discord parity, but they are useful Fluxer APIs to restore or implement from OpenAPI:

- Saved messages, scheduled messages, message search, mentions, read states, favorite memes/media, and GIF URL resolution.
- Relationships, auth sessions, MFA/WebAuthn, user settings, guild notification settings, pinned DMs, user connections, authorized IPs, and data export/harvest.
- Discovery categories/search/application lifecycle, vanity URLs, ownership transfer, bulk emoji/sticker routes, clone emoji/sticker routes, and richer audit logs.
- Packs, pack invites, pack emoji/sticker management, entrance sounds, entrance sound selections/playback, custom themes, gifts, premium, and billing-adjacent routes.
- Call eligibility, ringing, stop ringing, end call, RTC regions, call region updates, slowmode state, voice debug logging, voice presence heartbeat, and group DM recipient permissions.

## Dropped Or Not Applicable Discord Features

- Discord guild templates, guild widgets, guild integrations, developer teams/team members, news-channel publish/crosspost, and guild prune have no current matching Fluxer implementation in the importable library.
- Discord-shaped private calls should stay unsupported; Fluxer calls belong in `fluxer.calls` with Fluxer-native models.
- Discord `opus`, `oggparse`, and low-level voice protocol modules should remain unsupported unless Fluxer/LiveKit requires equivalent local media internals.

## Testing Notes

- `fluxer.py/tests/test_refactor_surface.py` is the current focused offline regression file for the restored import/message/webhook/gateway surface.
- `fluxer.py/tests/offline_tests.py` now gets past the old import blocker but still describes a broader future port surface; do not treat the whole script as a current coverage gate.
- Live gateway and voice behavior remain manual/smoke-test surfaces unless a Fluxer sandbox is provided.
