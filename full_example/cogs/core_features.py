from __future__ import annotations

import asyncio
import logging
from typing import Any

import fluxer as fluxer
from fluxer.ext import commands, tasks
from fluxer.ext.commands.errors import (
    ExtensionAlreadyLoaded,
    ExtensionFailed,
    ExtensionNotFound,
    ExtensionNotLoaded,
)

from bot import FullFeatureBot
from cogs.shared import parse_csv_ids

logger = logging.getLogger(__name__)


class CoreFeatures(commands.Cog):
    def __init__(self, bot: FullFeatureBot):
        super().__init__(bot)

    @commands.Cog.listener(name="on_message")
    async def on_message_log(self, message: fluxer.Message):
        if message.author.bot:
            return
        logger.info("Message event from %s in %s: %s", message.author.display_name, message.channel.name, message.content)

    @commands.Cog.listener(name="on_reaction_add")
    async def on_reaction_add_log(self, reaction: fluxer.Reaction, user: Any):
        logger.info("Reaction add event: %s by %s", reaction.emoji, getattr(user, "id", user))

    @tasks.loop(minutes=5.0)
    async def status_heartbeat(self):
        logger.info(
            "Heartbeat loop: ready=%s guilds=%s",
            self.bot.is_ready(),
            len(self.bot.guilds),
        )

    @status_heartbeat.before_loop
    async def before_status_heartbeat(self):
        await self.bot.wait_until_ready()

    @status_heartbeat.error
    async def status_heartbeat_error(self, error: Exception):
        logger.exception("status_heartbeat failed: %s", error)

    async def cog_load(self) -> None:
        self.status_heartbeat.start()

    async def cog_unload(self) -> None:
        self.status_heartbeat.stop()

    @commands.command(name="waitnext")
    async def waitnext(self, ctx: commands.Context, timeout: float = 15.0):
        """Wait for the invoking user's next message in the current channel."""
        await ctx.reply("Send your next message in this channel.")

        def _check(message: fluxer.Message) -> bool:
            return (
                message.channel_id == ctx.channel.id
                and message.author.id == ctx.author.id
                and not message.author.bot
            )

        try:
            event_message = await self.bot.wait_for(
                "message", check=_check, timeout=timeout
            )
        except TimeoutError:
            await ctx.reply("Timed out waiting for message.")
            return

        await ctx.reply(f"Captured message: {event_message.content}")

    @commands.command(name="presence")
    async def presence(
        self, ctx: commands.Context, status: str = "online", *, activity: str = "Fluxfork demo"
    ):
        """Send a Fluxer presence update with a status and activity text."""
        await self.bot.change_presence(status=status, activity=activity)
        await ctx.reply("Presence update dispatched.")

    @commands.command(name="gateway_members")
    async def gateway_members(self, ctx: commands.Context, guild_id: int, limit: int = 25):
        """Request guild members over the gateway for a guild."""
        await self.bot.request_guild_members(guild_id=guild_id, limit=limit)
        await ctx.reply("Gateway member request sent.")

    @commands.command(name="gateway_lazy")
    async def gateway_lazy(self, ctx: commands.Context, guild_id: int):
        """Request a lazy member-list update for a guild over the gateway."""
        await self.bot.request_lazy_members(guild_id=guild_id)
        await ctx.reply("Gateway lazy member request sent.")

    @commands.command(name="gateway_counts")
    async def gateway_counts(self, ctx: commands.Context, *, guild_ids: str):
        """Request member counts for comma-separated guild IDs over the gateway."""
        await self.bot.request_guild_counts(parse_csv_ids(guild_ids))
        await ctx.reply("Gateway guild count request sent.")

    @commands.command(name="gateway_channel_counts")
    async def gateway_channel_counts(self, ctx: commands.Context, *, channel_ids: str):
        """Request member counts for comma-separated channel IDs over the gateway."""
        await self.bot.request_channel_member_counts(parse_csv_ids(channel_ids))
        await ctx.reply("Gateway channel member count request sent.")

    @commands.command(name="convert_demo", aliases=["convert"])
    async def convert_demo(
        self,
        ctx: commands.Context,
        user: fluxer.User,
        channel: fluxer.Channel,
        member: fluxer.GuildMember,
        colour: fluxer.Colour,
        enabled: bool,
    ):
        """Demonstrate Fluxer converters for users, channels, members, colours, and booleans."""
        await ctx.reply(
            "Converted values: "
            f"user={user.display_name} channel={channel.id} member={member.display_name} "
            f"colour={colour.value} enabled={enabled}"
        )

    @commands.command(name="cooldown_demo")
    @commands.cooldown(2, 20.0, commands.BucketType.user)
    async def cooldown_demo(self, ctx: commands.Context):
        """Demonstrate a per-user command cooldown."""
        await ctx.reply("Cooldown demo executed.")

    @commands.command(name="concurrency_demo")
    @commands.max_concurrency(1, per=commands.BucketType.channel, wait=False)
    async def concurrency_demo(self, ctx: commands.Context, hold_seconds: int = 8):
        """Demonstrate max-concurrency locking for commands in a channel."""
        await ctx.reply(f"Holding slot for {hold_seconds}s.")
        await asyncio.sleep(hold_seconds)
        await ctx.reply("Concurrency slot released.")

    @commands.command(name="permission_demo")
    @commands.has_permissions(kick_members=True)
    async def permission_demo(self, ctx: commands.Context):
        """Check whether the caller has the kick-members permission."""
        await ctx.reply("You passed has_permissions(kick_members=True).")

    @commands.command(name="owner_demo")
    @commands.is_owner()
    async def owner_demo(self, ctx: commands.Context):
        """Check whether the caller is configured as the bot owner."""
        await ctx.reply("You passed is_owner().")

    @commands.group(name="math", invoke_without_command=True)
    async def math_group(self, ctx: commands.Context):
        """Show available math subcommands."""
        await ctx.reply("Use subcommands: math add <left> <right> or math mul <left> <right>.")

    @math_group.command(name="add")
    async def math_add(self, ctx: commands.Context, left: int, right: int):
        """Add two integers and return the result."""
        await ctx.reply(str(left + right))

    @math_group.command(name="mul", aliases=["multiply"])
    async def math_mul(self, ctx: commands.Context, left: int, right: int):
        """Multiply two integers and return the result."""
        await ctx.reply(str(left * right))

    @commands.group(name="extension", invoke_without_command=True)
    async def extension_group(self, ctx: commands.Context):
        """Show loaded extensions or use subcommands to manage them."""
        loaded = sorted(self.bot.extensions.keys())
        await ctx.reply(f"Loaded extensions: {', '.join(loaded) if loaded else 'none'}")

    @extension_group.command(name="load")
    async def extension_load(self, ctx: commands.Context, extension: str):
        """Load an extension module by import path."""
        try:
            await self.bot.load_extension(extension)
        except (ExtensionAlreadyLoaded, ExtensionNotFound, ExtensionFailed) as exc:
            await ctx.reply(f"Extension load failed: {exc}")
            return
        await ctx.reply(f"Loaded extension {extension}.")

    @extension_group.command(name="unload")
    async def extension_unload(self, ctx: commands.Context, extension: str):
        """Unload an extension module by import path."""
        try:
            await self.bot.unload_extension(extension)
        except (ExtensionNotLoaded, ExtensionNotFound) as exc:
            await ctx.reply(f"Extension unload failed: {exc}")
            return
        await ctx.reply(f"Unloaded extension {extension}.")

    @extension_group.command(name="reload")
    async def extension_reload(self, ctx: commands.Context, extension: str):
        """Reload an extension module by import path."""
        try:
            await self.bot.reload_extension(extension)
        except (ExtensionNotFound, ExtensionNotLoaded, ExtensionFailed) as exc:
            await ctx.reply(f"Extension reload failed: {exc}")
            return
        await ctx.reply(f"Reloaded extension {extension}.")


async def setup(bot: FullFeatureBot):
    await bot.add_cog(CoreFeatures(bot))
