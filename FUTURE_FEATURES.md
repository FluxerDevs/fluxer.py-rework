# fluxer.py Future Features

This file tracks Fluxer-backed features that are not fully exposed by the current importable `fluxer.py/` library. The OpenAPI document and Gateway Protocol Reference remain the source of truth for whether a feature is viable.

## Near-Term Restoration Work

- Reconcile the broader manual `tests/offline_tests.py` script with current source. The focused refactor surface is covered by `tests/test_refactor_surface.py`, while the older script still contains future-port expectations.
- Re-export additional implemented helper types intentionally from `fluxer.__init__`, or document them as module-only.
- Continue moving future-port expectations into focused pytest modules as each surface is restored.

## Message And Channel Features

- Saved/unsaved message helpers, selected-media forwarding helpers, and richer message-reference hydration from full API responses.
- Presigned attachment upload orchestration above the existing `File` helper and lower-level message routes.
- Reaction user iterators and fuller reaction cache hydration.

## Account And User Features

- Saved messages, scheduled messages, mentions/read states, relationships, favorite media/GIF resolution, auth sessions, MFA/WebAuthn summaries, user settings, guild notification settings, pinned DMs, user connections, authorized IPs, and data harvest/export wrappers.
- These should be clearly marked user-token-sensitive and remain Fluxer-native rather than Discord-shaped.

## Guild, Discovery, And Admin Features

- Discovery categories/search/application lifecycle, discovery join, vanity URLs, ownership transfer, bulk emoji/sticker creation, emoji/sticker clone endpoints, role hoist-position helpers, and richer audit-log diffs.
- Keep the existing core guild/channel/member/role helpers as the base and add only routes backed by OpenAPI.

## Calls, RTC, Voice, And Media

- Fluxer-native call eligibility, ringing, stop ringing, end call, RTC regions, call region update, voice debug logging, slowmode state, voice presence heartbeat, and group-DM recipient permission wrappers.
- Higher-level LiveKit-backed voice player ergonomics may be added, but Discord UDP/Opus/Ogg internals should remain unsupported unless Fluxer requires them.

## Packs, Premium, Gifts, And Billing

- Pack dashboard/install/invite/media helpers, entrance sound library/selection/playback, custom themes, gift-code management, and favorite meme/media management.
- Broader premium, subscription, donation, Stripe checkout, and billing management should stay low-level and opt-in because they are account/payment sensitive.

## Gateway And Cache Depth

- Typed Fluxer-only raw events for relationship, favorite meme, saved message, auth session, WebAuthn credential, user guild settings, pinned DMs, user connections, entrance sound, recent mention delete, and guild member list updates.
- Lazy member-list hydration, member/count request helpers, relationship/read-state caches, and richer message/reaction raw fallback behavior.

## Discord-Only Features To Keep Unsupported

- Discord guild templates, widgets, guild integrations, developer teams/team members, news publish/crosspost, guild prune, Discord-shaped private calls, `opus`, and `oggparse`.
