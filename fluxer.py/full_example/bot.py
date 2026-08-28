from __future__ import annotations

import logging
import os
from pathlib import Path
from typing import Any

import fluxer as fluxer
from fluxer.ext import commands
from fluxer.ext.commands.errors import (
    BadArgument,
    CheckFailure,
    CommandError,
    CommandInvokeError,
    CommandNotFound,
    CommandOnCooldown,
    MaxConcurrencyReached,
    MissingRequiredArgument,
)

logger = logging.getLogger(__name__)


def _env_flag(name: str, default: bool = False) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


class FullFeatureBot(commands.Bot):
    def __init__(self, command_prefix: str, *args: Any, **kwargs: Any):
        super().__init__(
            command_prefix=commands.when_mentioned_or(command_prefix),
            intents=fluxer.Intents.default(),
            case_insensitive=True,
            description="Comprehensive Fluxfork full-feature example bot",
            *args,
            **kwargs,
        )
        self.intents = fluxer.Intents.default()
        self.enable_mutations = _env_flag("ENABLE_MUTATIONS", default=False)
        self.enable_account_routes = _env_flag("ENABLE_ACCOUNT_ROUTES", default=False)
        self.enable_voice = _env_flag("ENABLE_VOICE", default=False)
        logging.basicConfig(level=self.get_log_level())

        @self.command(name="ping", aliases=["pong"])
        async def ping(ctx: commands.Context):
            """Check that the bot can receive commands and reply."""
            await ctx.reply("Pong!")

        @self.command(name="about")
        async def about(ctx: commands.Context):
            """Show a short overview of the full Fluxer example bot."""
            await ctx.reply(
                "Full example loaded. Use `help` to explore feature groups and commands."
            )

        @self.command(name="framework")
        async def framework(ctx: commands.Context):
            """Show gateway readiness, guild count, and message cache size."""
            ready = self.is_ready()
            await ctx.reply(
                f"ready={ready} guilds={len(self.guilds)} cached_messages={len(self.cached_messages)}"
            )

        @self.command(name="helpme")
        async def helpme(ctx: commands.Context, *, command_name: str = ""):
            """Show the help page, or detailed help for a named command."""
            if command_name:
                await ctx.send_help(command_name)
            else:
                await ctx.send_help()

        @self.before_invoke
        async def _before_invoke(ctx: commands.Context):
            logger.info(
                "Invoking command=%s by user=%s",
                getattr(ctx.command, "qualified_name", "<unknown>"),
                getattr(ctx.author, "id", "unknown"),
            )

        @self.after_invoke
        async def _after_invoke(ctx: commands.Context):
            logger.info(
                "Completed command=%s by user=%s",
                getattr(ctx.command, "qualified_name", "<unknown>"),
                getattr(ctx.author, "id", "unknown"),
            )

        @self.event
        async def on_ready():
            if self.user is not None:
                logger.info("Logged in as %s (%s)", self.user.display_name, self.user.id)
            else:
                logger.warning("READY received but user is None")

        @self.on("fluxer_event")
        async def _on_fluxer_event(raw_event: Any):
            logger.debug(
                "Raw Fluxer event received: %s",
                getattr(raw_event, "event_name", type(raw_event).__name__),
            )

    def get_log_level(self) -> int:
        log_level = os.getenv("LOG_LEVEL", "INFO").strip().upper()
        return getattr(logging, log_level, logging.INFO)

    async def setup_hook(self) -> None:
        await self.load_extensions()

    async def load_extensions(self) -> None:
        cogs_path = Path(__file__).resolve().parent / "cogs"
        for file in cogs_path.glob("*.py"):
            if file.name.startswith("_") or file.stem == "shared":
                continue
            await self.load_extension(f"cogs.{file.stem}")

    async def on_command_error(
        self, context: commands.Context, exception: Exception
    ) -> None:
        if isinstance(exception, CommandNotFound):
            return
        if isinstance(exception, MissingRequiredArgument):
            await context.reply(str(exception))
            return
        if isinstance(exception, BadArgument):
            await context.reply(f"Invalid argument: {exception}")
            return
        if isinstance(exception, CommandOnCooldown):
            await context.reply(f"Cooldown active. Retry in {exception.retry_after:.2f}s")
            return
        if isinstance(exception, MaxConcurrencyReached):
            await context.reply("This command is already running. Try again shortly.")
            return
        if isinstance(exception, CheckFailure):
            await context.reply(f"Command check failed: {exception}")
            return
        if isinstance(exception, CommandInvokeError):
            original = exception.original
            if isinstance(original, fluxer.HTTPException):
                await context.reply(
                    f"HTTP error ({original.status}) {original.code}: {original.message}"
                )
            else:
                await context.reply(f"Command failed: {original}")
            logger.exception("Command invoke error", exc_info=original)
            return
        if isinstance(exception, CommandError):
            await context.reply(f"Command error: {exception}")
            return
        logger.exception("Unhandled command error", exc_info=exception)
        await context.reply(f"Unhandled error: {exception}")
