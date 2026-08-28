# Potential Ports For fluxer.py

This report lists dropped, deferred, partial, and currently broken areas that could become useful `fluxer.py` features. The goal is Fluxer-native ergonomics with familiar discord.py-style names only where the Fluxer API supports them.

## Highest Priority: Reconcile Current Port Surface

### 1. Continue Broad Client/HTTP Surface Reconciliation

Current status: `fluxer.message` and `fluxer.webhook` import cleanly, and focused regression coverage exists for the restored message/webhook/gateway surface.

Next useful work: reconcile the much broader manual `offline_tests.py` script with current source by either restoring the remaining OpenAPI-backed client wrappers or moving future-only checks into a separate backlog test module.

### 2. Align Tests With Current Source

Current status: `fluxer.py/tests/offline_tests.py` expects many APIs that are not present on current importable classes.

Options:

- Treat the file as a backlog/spec and mark tests expected-failing until implementation catches up.
- Split it into current passing tests and future port tests.
- Restore the missing code to satisfy the existing tests.

Recommendation: split current tests from future-port tests so coverage can become trustworthy again.

### 3. Reconcile Top-Level Exports

Current status: many helper classes exist in modules but are not exported at `fluxer.*`.

Options:

- Export all stable implemented classes from `fluxer.__init__`.
- Keep advanced helpers module-only and document import paths.
- Add a compatibility audit test that imports every documented public symbol.

Recommendation: export only stable implemented models and add an import-surface test to prevent docs drift.

## Message And Channel Parity

Good candidates:

- Message save/unsave helpers, selected-media forwarding helpers, and richer reference parsing from full API responses.
- Channel permission overwrite helpers and richer invite ergonomics.
- Reaction user iterators and full reaction cache hydration.

Why it fits: Fluxer has message/channel REST endpoints and this is high-value bot ergonomics.

Risk: Medium. Avoid promising Discord-specific channel subclasses or payload fields that Fluxer does not provide.

## Command Framework Completion

Good candidates:

- Make `fluxer.ext.commands.Bot` the recommended command bot in examples and docs.
- Finish help-command behavior, command signatures, parser edge cases, converter errors, extension rollback, cog hooks, and cooldown/concurrency edge cases.
- Decide how the older top-level `fluxer.Bot` relates to `fluxer.ext.commands.Bot`.

Why it fits: Mostly local behavior, independent of Fluxer REST changes.

Risk: Low to medium. Parser compatibility has subtle edge cases, so tests matter.

## Fluxer-Native REST Expansion

Good candidates:

- Account APIs: auth sessions, MFA/WebAuthn, settings, guild notification settings, pinned DMs, connections, authorized IPs, data export.
- Messaging APIs: saved/scheduled messages, mentions/read states, message search, favorite media/GIF resolution.
- Guild/admin APIs: discovery, vanity, transfer ownership, bulk emoji/sticker, clone emoji/sticker, audit-log diffs.
- Calls/media APIs: call eligibility, ringing, RTC regions, slowmode, voice debug logging, entrance sounds, packs, themes, gifts.

Why it fits: These are Fluxer-specific strengths and should not be forced into Discord-shaped models.

Risk: Medium to high for user-token-sensitive and payment-adjacent routes. Keep docstrings explicit and live tests opt-in.

## Cache, Gateway, And Events

Good candidates:

- Broader `ConnectionState` caches for channels, members, messages, voice states, reactions, relationships, saved messages, and read states.
- Rich/raw event fallback behavior for message edits/deletes, reactions, and more Fluxer-only gateway events.
- Lazy member-list hydration and cache reconciliation after gateway helper requests.

Why it fits: Fluxer gateway docs include enough protocol shape for typed payloads and raw events.

Risk: Medium. Cache correctness and reconnect behavior need carefully isolated tests.

## Models And Local Utilities

Good candidates:

- `Asset` transformation helpers where Fluxer CDN supports them.
- `SequenceProxy`, hash/equality helpers, richer `Object`, `Colour`/`Color` aliases, permission overwrite tests, and richer `Embed` validation.
- Async iterators for paginated REST routes.

Why it fits: Mostly local ergonomics and type-checker value.

Risk: Low unless CDN transforms are guessed instead of backed by Fluxer behavior.

## Voice And Player Ergonomics

Good candidates:

- Keep LiveKit/ffmpeg as the transport, but add higher-level `play`, `pause`, `resume`, `stop`, `is_playing`, and source lifecycle tests.
- Mock ffmpeg and LiveKit behavior for offline tests; keep live voice manual.

Why it fits: Voice is useful, but Fluxer's implementation should stay Fluxer-native.

Risk: Medium. Do not copy Discord UDP/Opus internals unless Fluxer needs them.

## Keep Unsupported Unless Fluxer Adds Equivalents

- Discord guild templates.
- Discord guild widgets.
- Discord guild integrations.
- Discord developer team/team-member models.
- Discord news publish/crosspost.
- Guild prune helpers.
- Discord-shaped private calls.
- Discord `opus` and `oggparse` internals.
