from __future__ import annotations

from typing import Any

import fluxer as fluxer
from fluxer.ext import commands

from bot import FullFeatureBot
from cogs.shared import require_account_routes, require_mutations, require_voice


class WebhookVoiceFeatures(commands.Cog):
    def __init__(self, bot: FullFeatureBot):
        super().__init__(bot)
        self.voice_clients: dict[int, fluxer.VoiceClient] = {}

    @commands.command(name="webhooks_channel")
    async def webhooks_channel(self, ctx: commands.Context, channel: fluxer.Channel):
        """List webhooks for a channel."""
        hooks = await self.bot.fetch_channel_webhooks(str(channel.id))
        await ctx.reply(f"Channel webhooks={len(hooks)}")

    @commands.command(name="webhooks_guild")
    async def webhooks_guild(self, ctx: commands.Context, guild_id: int):
        """List webhooks for a guild."""
        hooks = await self.bot.fetch_guild_webhooks(str(guild_id))
        await ctx.reply(f"Guild webhooks={len(hooks)}")

    @commands.command(name="webhook_create")
    async def webhook_create(
        self, ctx: commands.Context, channel: fluxer.Channel, *, name: str
    ):
        """Create a webhook in a channel. Requires mutations to be enabled."""
        require_mutations(self.bot)
        webhook = await self.bot.create_webhook(str(channel.id), name=name)
        await ctx.reply(f"Webhook created id={webhook.id}")

    @commands.command(name="webhook_fetch")
    async def webhook_fetch(self, ctx: commands.Context, webhook_id: int):
        """Fetch a webhook by ID."""
        webhook = await self.bot.fetch_webhook(str(webhook_id))
        await ctx.reply(f"Webhook id={webhook.id} name={webhook.name!r}")

    @commands.command(name="webhook_send")
    async def webhook_send(self, ctx: commands.Context, webhook_url: str, *, content: str):
        """Send a message through a webhook URL."""
        webhook = fluxer.Webhook.from_url(webhook_url, http=self.bot._http)
        message = await webhook.send(content=content, wait=True)
        await ctx.reply(f"Webhook message id={message.id if message is not None else 'none'}")

    @commands.command(name="webhook_edit")
    async def webhook_edit(
        self,
        ctx: commands.Context,
        webhook_url: str,
        *,
        name: str,
    ):
        """Edit a webhook's name. Requires mutations to be enabled."""
        require_mutations(self.bot)
        webhook = fluxer.Webhook.from_url(webhook_url, http=self.bot._http)
        updated = await webhook.edit(name=name)
        await ctx.reply(f"Webhook updated name={updated.name!r}")

    @commands.command(name="webhook_delete")
    async def webhook_delete(self, ctx: commands.Context, webhook_url: str):
        """Delete a webhook by URL. Requires mutations to be enabled."""
        require_mutations(self.bot)
        webhook = fluxer.Webhook.from_url(webhook_url, http=self.bot._http)
        await webhook.delete()
        await ctx.reply("Webhook deleted.")

    @commands.command(name="webhook_provider")
    async def webhook_provider(self, ctx: commands.Context, webhook_url: str, provider: str):
        """Execute a provider-specific webhook payload. Requires mutations to be enabled."""
        require_mutations(self.bot)
        webhook = fluxer.Webhook.from_url(webhook_url, http=self.bot._http)
        payload: dict[str, Any] = {"event": "example", "source": "full_example"}
        if provider == "github":
            await webhook.execute_github(payload)
        elif provider == "instatus":
            await webhook.execute_instatus(payload)
        elif provider == "slack":
            response = await webhook.execute_slack(payload)
            await ctx.reply(f"Slack endpoint response={response!r}")
            return
        else:
            raise RuntimeError("provider must be one of: github, instatus, slack")
        await ctx.reply(f"Executed {provider} webhook payload.")

    @commands.command(name="packs")
    async def packs(self, ctx: commands.Context):
        """Fetch the current user's pack dashboard."""
        require_account_routes(self.bot)
        dashboard = await self.bot.fetch_packs()
        await ctx.reply(
            f"packs sections={len(dashboard.sections)} total={dashboard.total_count}"
        )

    @commands.command(name="pack_invites")
    async def pack_invites(self, ctx: commands.Context, pack_id: int):
        """List invites for a pack."""
        require_account_routes(self.bot)
        invites = await self.bot.fetch_pack_invites(pack_id)
        await ctx.reply(f"pack_invites={len(invites)}")

    @commands.command(name="pack_emojis")
    async def pack_emojis(self, ctx: commands.Context, pack_id: int):
        """List emojis in a pack."""
        require_account_routes(self.bot)
        emojis = await self.bot.fetch_pack_emojis(pack_id)
        await ctx.reply(f"pack_emojis={len(emojis)}")

    @commands.command(name="pack_stickers")
    async def pack_stickers(self, ctx: commands.Context, pack_id: int):
        """List stickers in a pack."""
        require_account_routes(self.bot)
        stickers = await self.bot.fetch_pack_stickers(pack_id)
        await ctx.reply(f"pack_stickers={len(stickers)}")

    @commands.command(name="entrance_sounds")
    async def entrance_sounds(self, ctx: commands.Context):
        """List entrance sounds and selections for the current user."""
        require_account_routes(self.bot)
        library = await self.bot.fetch_entrance_sound_library()
        await ctx.reply(
            f"entrance_sounds={len(library.sounds)} selections={len(library.selections)}"
        )

    @commands.command(name="call_eligibility")
    async def call_eligibility(self, ctx: commands.Context, channel_id: int):
        """Check whether a channel can start or ring a call."""
        require_account_routes(self.bot)
        eligibility = await self.bot.fetch_call_eligibility(channel_id)
        await ctx.reply(f"call eligible={eligibility.can_call} ringable={eligibility.ringable}")

    @commands.command(name="rtc_regions")
    async def rtc_regions(self, ctx: commands.Context, channel_id: int):
        """List RTC regions available to a call channel."""
        require_account_routes(self.bot)
        regions = await self.bot.fetch_rtc_regions(channel_id)
        await ctx.reply(f"rtc_regions={len(regions)}")

    @commands.command(name="slowmode_state")
    async def slowmode_state(self, ctx: commands.Context, channel_id: int):
        """Fetch slowmode state for a channel."""
        require_account_routes(self.bot)
        state = await self.bot.fetch_channel_slowmode_state(channel_id)
        await ctx.reply(
            f"slowmode_seconds={state.slowmode_seconds} retry_after={state.retry_after}"
        )

    @commands.command(name="voice_debug_status")
    async def voice_debug_status(self, ctx: commands.Context, channel_id: int):
        """Fetch voice debug logging status for a channel."""
        require_account_routes(self.bot)
        status = await self.bot.fetch_voice_debug_logging_status(channel_id)
        await ctx.reply(f"voice_debug enabled={status.enabled}")

    @commands.command(name="voice_debug_toggle")
    async def voice_debug_toggle(
        self, ctx: commands.Context, channel_id: int, enabled: bool
    ):
        """Toggle voice debug logging for a channel. Requires mutations to be enabled."""
        require_account_routes(self.bot)
        require_mutations(self.bot)
        status = await self.bot.set_voice_debug_logging_status(channel_id, enabled)
        await ctx.reply(f"voice_debug enabled={status.enabled}")

    @commands.command(name="voice_hb")
    async def voice_hb(self, ctx: commands.Context, channel_id: int):
        """Send a voice presence heartbeat for a channel."""
        require_account_routes(self.bot)
        state = await self.bot.voice_presence_heartbeat(channel_id)
        await ctx.reply(f"voice_state channel_id={state.channel_id} active={state.active}")

    @commands.command(name="ring_call")
    async def ring_call(self, ctx: commands.Context, channel_id: int, *, user_ids: str = ""):
        """Ring call recipients for a channel. Requires mutations to be enabled."""
        require_account_routes(self.bot)
        require_mutations(self.bot)
        parsed = [int(x.strip()) for x in user_ids.split(",") if x.strip()]
        await self.bot.ring_call(channel_id, parsed or None)
        await ctx.reply("Ring call request sent.")

    @commands.command(name="stop_ringing")
    async def stop_ringing(self, ctx: commands.Context, channel_id: int, *, user_ids: str = ""):
        """Stop ringing call recipients for a channel. Requires mutations to be enabled."""
        require_account_routes(self.bot)
        require_mutations(self.bot)
        parsed = [int(x.strip()) for x in user_ids.split(",") if x.strip()]
        await self.bot.stop_ringing_call(channel_id, parsed or None)
        await ctx.reply("Stop ringing request sent.")

    @commands.command(name="end_call")
    async def end_call(self, ctx: commands.Context, channel_id: int):
        """End the active call in a channel. Requires mutations to be enabled."""
        require_account_routes(self.bot)
        require_mutations(self.bot)
        await self.bot.end_call(channel_id)
        await ctx.reply("Call end request sent.")

    @commands.command(name="group_dm_perms")
    async def group_dm_perms(self, ctx: commands.Context, channel_id: int, user_id: int):
        """Fetch group DM recipient permissions."""
        require_account_routes(self.bot)
        perms = await self.bot.fetch_group_dm_recipient_permissions(channel_id, user_id)
        await ctx.reply(f"group_dm_permissions keys={list(perms.keys())}")

    @commands.command(name="group_dm_add")
    async def group_dm_add(self, ctx: commands.Context, channel_id: int, user_id: int):
        """Add a recipient to a group DM. Requires mutations to be enabled."""
        require_account_routes(self.bot)
        require_mutations(self.bot)
        await self.bot.add_group_dm_recipient(channel_id, user_id)
        await ctx.reply("Group DM recipient added.")

    @commands.command(name="group_dm_remove")
    async def group_dm_remove(self, ctx: commands.Context, channel_id: int, user_id: int):
        """Remove a recipient from a group DM. Requires mutations to be enabled."""
        require_account_routes(self.bot)
        require_mutations(self.bot)
        await self.bot.remove_group_dm_recipient(channel_id, user_id)
        await ctx.reply("Group DM recipient removed.")

    @commands.command(name="voice_join")
    async def voice_join(self, ctx: commands.Context, channel: fluxer.Channel):
        """Join a Fluxer voice channel. Requires voice support to be enabled."""
        require_voice(self.bot)
        voice_client = await channel.connect(self.bot)
        if channel.guild_id is not None:
            self.voice_clients[channel.guild_id] = voice_client
        await ctx.reply(f"Joined voice channel {channel.id}")

    @commands.command(name="voice_disconnect")
    async def voice_disconnect(self, ctx: commands.Context, guild_id: int | None = None):
        """Disconnect a cached voice client."""
        require_voice(self.bot)
        target_guild_id = guild_id or ctx.message.guild_id
        if target_guild_id is None:
            raise RuntimeError("guild_id is required outside guild channels.")
        voice_client = self.voice_clients.get(target_guild_id)
        if voice_client is None:
            raise RuntimeError("No cached voice client for this guild.")
        await voice_client.disconnect()
        self.voice_clients.pop(target_guild_id, None)
        await ctx.reply("Disconnected voice client.")

    @commands.command(name="voice_pause")
    async def voice_pause(self, ctx: commands.Context, guild_id: int | None = None):
        """Pause playback on a cached voice client."""
        require_voice(self.bot)
        target_guild_id = guild_id or ctx.message.guild_id
        if target_guild_id is None:
            raise RuntimeError("guild_id is required outside guild channels.")
        voice_client = self.voice_clients.get(target_guild_id)
        if voice_client is None:
            raise RuntimeError("No cached voice client for this guild.")
        voice_client.pause()
        await ctx.reply("Voice playback paused.")

    @commands.command(name="voice_resume")
    async def voice_resume(self, ctx: commands.Context, guild_id: int | None = None):
        """Resume playback on a cached voice client."""
        require_voice(self.bot)
        target_guild_id = guild_id or ctx.message.guild_id
        if target_guild_id is None:
            raise RuntimeError("guild_id is required outside guild channels.")
        voice_client = self.voice_clients.get(target_guild_id)
        if voice_client is None:
            raise RuntimeError("No cached voice client for this guild.")
        voice_client.resume()
        await ctx.reply("Voice playback resumed.")

    @commands.command(name="voice_play_file")
    async def voice_play_file(self, ctx: commands.Context, file_path: str):
        """Play a local audio file through the cached voice client."""
        require_voice(self.bot)
        guild_id = ctx.message.guild_id
        if guild_id is None:
            raise RuntimeError("This command requires a guild context.")
        voice_client = self.voice_clients.get(guild_id)
        if voice_client is None:
            raise RuntimeError("Join a voice channel first with voice_join.")
        source = fluxer.FFmpegPCMAudio(file_path)
        await voice_client.play(source)
        await ctx.reply("Playback started.")


async def setup(bot: FullFeatureBot):
    await bot.add_cog(WebhookVoiceFeatures(bot))
