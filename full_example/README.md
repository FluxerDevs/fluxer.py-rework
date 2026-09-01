# Full Feature Fluxfork Example

This example is the canonical live/manual Fluxfork bot and demonstrates the currently implemented feature surface (including `done` and `partial` items from `COVERAGE.md`).

## Features covered

- Subclassed bot setup with dynamic cog loading
- Event handlers (`on_message`, reaction events, raw Fluxer events)
- Command framework features: groups, aliases, converters, checks, cooldowns, max concurrency, help/context helpers
- Gateway helpers: presence updates, waiters, member/count requests
- Message and channel APIs: send/fetch/history/reply/edit/delete/purge/pins/typing/reactions/search
- Guild/admin APIs: channel/role/member/moderation/invite/discovery/vanity/audit
- Account APIs (optional): applications, saved/scheduled messages, mentions/read states, relationships, settings, gifts
- Webhooks and provider-specific execute endpoints
- Media/calls/RTC and optional voice controls
- Fluxer-native pack and entrance sound commands

## Setup

1. From the repository root, change into `fluxfork/full_example`.
2. Create and activate a virtual environment, or use the repository `.venv`.
3. Install dependencies:
   - `pip install -r requirements.txt`
4. Ensure `.env` defines `DEV_TOKEN`.
5. Optionally set env vars from `.env.example`.
6. Run:
   - `python main.py`
   - Or from `fluxfork`: `python -m full_example.main`

## Guarded command behavior

- Commands that mutate state require `ENABLE_MUTATIONS=true`.
- Account-user routes require `ENABLE_ACCOUNT_ROUTES=true`.
- Voice commands require `ENABLE_VOICE=true` and optional voice dependencies (`livekit` + ffmpeg environment).

## Command families

- Core/framework: `framework`, `waitnext`, `presence`, `gateway_*`, `convert_demo`, `cooldown_demo`, `concurrency_demo`, `permission_demo`, `owner_demo`, `math *`, `extension *`
- Messaging/channels: `send_text`, `send_embed`, `fetch_message`, `reply_message`, `edit_message`, `delete_message`, `message_*`, `history`, `purge_contains`, `bulk_delete`, `react_*`, `trigger_typing`, `typing_block`, `attachment_*`, `search_messages`, `partial_fetch`
- Guild/admin: `guilds`, `guild_fetch`, `guild_channels`, `channel_*`, `guild_roles`, `guild_members`, `guild_member`, `member_*`, `guild_kick`, `guild_ban`, `guild_unban`, `guild_bans`, `guild_audit`, `guild_vanity`, `guild_set_vanity`, `guild_discovery_status`, `discovery_search`, `guild_emojis`, `guild_stickers`, `guild_bulk_*`
- Account: `user_*`, `apps`, `app_fetch`, `saved_messages`, `scheduled_*`, `mentions*`, `read_states_ack`, `relationships`, `relationship_nick`, `gifts`, `gift_*`, `settings*`, `connections`, `auth_sessions`, `mfa_state`, `webauthn`, `authorized_ips`, `data_harvest`, `theme_create`
- Webhooks/voice/calls/packs: `webhooks_*`, `webhook_*`, `packs`, `pack_*`, `entrance_sounds`, `call_*`, `rtc_regions`, `slowmode_state`, `voice_debug_*`, `voice_hb`, `ring_call`, `stop_ringing`, `end_call`, `group_dm_*`, `voice_*`
