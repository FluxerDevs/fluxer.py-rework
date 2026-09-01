from __future__ import annotations

from typing import Any

import fluxer as fluxer
from fluxer.ext import commands


def parse_csv_ids(value: str) -> list[int]:
    ids = []
    for chunk in value.split(","):
        cleaned = chunk.strip()
        if cleaned:
            ids.append(int(cleaned))
    return ids


def require_mutations(bot: Any) -> None:
    if not getattr(bot, "enable_mutations", False):
        raise RuntimeError(
            "Mutating commands are disabled. Set ENABLE_MUTATIONS=true to enable."
        )


def require_account_routes(bot: Any) -> None:
    if not getattr(bot, "enable_account_routes", False):
        raise RuntimeError(
            "Account commands are disabled. Set ENABLE_ACCOUNT_ROUTES=true to enable."
        )


def require_voice(bot: Any) -> None:
    if not getattr(bot, "enable_voice", False):
        raise RuntimeError("Voice commands are disabled. Set ENABLE_VOICE=true to enable.")


async def resolve_guild(
    ctx: commands.Context, guild_id: int | None = None
) -> fluxer.Guild:
    resolved_id = guild_id or ctx.message.guild_id
    if resolved_id is None:
        raise RuntimeError("This command requires a guild context or guild_id.")
    return await ctx.bot.fetch_guild(str(resolved_id))
