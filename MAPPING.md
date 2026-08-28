# fluxer.py Mapping

`fluxer.py/` is the active Fluxer library in this repository. It uses the `fluxer` namespace and maps familiar discord.py ideas onto Fluxer entities only where the Fluxer API has a real equivalent.

## Repository Structure

| Folder/file | Purpose |
| --- | --- |
| `fluxer.py/` | Active rewritten library and examples/tests. |
| `discord.py/` | Ignored upstream discord.py reference checkout. |
| `fluxer.py-old/` | Ignored pinned old Fluxer wrapper checkout. |
| `api.canary.fluxer.app-openapi.json` | REST contract reference; unchanged by docs updates. |
| `Fluxer Gateway Protocol Reference.md` | Gateway reference; unchanged by docs updates. |

## Core Concept Mapping

| discord.py concept | Current fluxer.py concept | Status |
| --- | --- | --- |
| `discord.Client` | `fluxer.Client` | Current core client. |
| `discord.ext.commands.Bot` | `fluxer.ext.commands.Bot` | Importable richer command bot, separate from top-level `fluxer.Bot`. |
| Older command bot | `fluxer.Bot` | Current top-level legacy/simple command bot. |
| `discord.ext.commands.Context` | `fluxer.ext.commands.Context` | Importable under `fluxer.ext.commands`. |
| `discord.Cog` / `commands.Cog` | `fluxer.Cog` and `fluxer.ext.commands.Cog` | Two command surfaces currently coexist. |
| `discord.Guild` | `fluxer.Guild` | Core model exists. |
| `discord.Member` | `fluxer.GuildMember`; `fluxer.member.Member` alias | Core model exists; compatibility module imports. |
| `discord.User` / `ClientUser` | `fluxer.User`; `fluxer.user.ClientUser` alias | Core model exists; current-user edit parity deferred. |
| `TextChannel`, `VoiceChannel`, `DMChannel`, `GroupChannel`, `CategoryChannel` | Unified `fluxer.Channel` with `ChannelType`; aliases in `fluxer.channel` | Unified model. `StageChannel` and `StoreChannel` are not exported because Fluxer has no matching channel types. |
| `discord.Message` | `fluxer.Message`, `fluxer.PartialMessage`, `fluxer.MessageReference` | Core model plus partial/reference helpers exist. |
| `discord.Role` | `fluxer.Role` | Core model exists; RoleTags partial. |
| `discord.Emoji` / `PartialEmoji` | `fluxer.Emoji` / `fluxer.models.reaction.PartialEmoji` | Core models exist. |
| `discord.Reaction` | `fluxer.Reaction` | Core model exists; user iterator deferred. |
| `discord.Embed` | `fluxer.Embed` | Basic builder/model exists. |
| `discord.File` | `fluxer.File` | Basic file payload helper exists. |
| `discord.AllowedMentions` | `fluxer.AllowedMentions` / `fluxer.mentions.AllowedMentions` | Exported and wired into message/webhook send/edit payloads. |
| `discord.Object` | `fluxer.Object` / `fluxer.object.Object` | Exported lightweight Fluxer snowflake object. |
| `discord.Colour` / `Color` | `fluxer.Colour` / `fluxer.Color` | Exported RGB helper aliases. |
| `discord.Asset` | `fluxer.asset.Asset` | Basic URL read/save helper exists. |
| `discord.Invite` | `fluxer.Invite` | Module/model exists; richer partial invite wrappers deferred. |
| `discord.Sticker` | `fluxer.Sticker` / `fluxer.sticker.Sticker` | Model exists; bulk/admin helpers deferred. |
| `discord.Webhook` | `fluxer.Webhook` / `fluxer.webhook.Webhook` | Core model imports cleanly and supports token URL handles. |
| `discord.WebhookMessage` | `fluxer.WebhookMessage` / `fluxer.webhook.WebhookMessage` | Implemented for waited webhook sends and webhook message edit/delete. |
| Raw message/reaction events | `fluxer.raw_models`, `fluxer.models.reaction` raw classes | Importable, partial coverage. |
| Discord private calls | `fluxer.calls` for Fluxer-native call/RTC models | Model module exists; route wrappers deferred. |

## Command Framework Mapping

| discord.py import/behavior | fluxer.py equivalent | Status |
| --- | --- | --- |
| `from discord.ext import commands` | `from fluxer.ext import commands` | Importable. |
| `commands.Bot` | `fluxer.ext.commands.Bot` | Importable richer command framework. |
| `@bot.command`, `@commands.command`, `@commands.group` | Same names under `fluxer.ext.commands` | Implemented, needs broader parity tests. |
| Cogs/listeners/extensions | `fluxer.ext.commands.Cog`, load/unload/reload helpers | Partial parity. |
| Checks/cooldowns/max concurrency | Same names under `fluxer.ext.commands` | Implemented, more edge-case coverage needed. |
| Help command | `HelpCommand`, `DefaultHelpCommand`, `MinimalHelpCommand`, `Paginator` | Importable, parity still partial. |
| `discord.ext.tasks.loop` | `fluxer.ext.tasks.loop` | Importable loop helper, advanced scheduling deferred. |

## Gateway And REST Mapping

| discord.py behavior | fluxer.py behavior |
| --- | --- |
| Discord gateway opcodes | Fluxer gateway opcodes from the Gateway Protocol Reference. Documented Fluxer opcodes 5, 12, 14, 15, and 16 are included. |
| Discord identify payload | Fluxer identify payload with token, properties, intents/flags, presence, and shard data where supported. |
| Discord REST base | Fluxer REST base defaults to `https://api.fluxer.app/v1` in current source. |
| Discord rate-limit strategy | Fluxer response headers and `HTTPClient` bucket locks. |
| Discord sharding | Thin `fluxer.shard` placeholders and `/gateway/bot` metadata; full orchestration deferred. |
| Discord connection state | Smaller Fluxer cache for user/guild/message/voice-state and partial event state. |

## Broken Or Deferred Compatibility Mapping

- `fluxer.message` and `fluxer.webhook` now import cleanly.
- `StageChannel` and `StoreChannel` are intentionally not exported from `fluxer.channel`; Fluxer does not expose matching channel types in the current API/spec.
- Fluxer-only account, saved/scheduled message, calls/RTC, discovery/admin, pack/media, and billing surfaces have model classes in places, but public route/client wrappers are not consistently present in current source.
- No `discord` namespace should be created.
