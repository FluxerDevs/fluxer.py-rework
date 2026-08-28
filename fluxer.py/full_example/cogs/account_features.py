from __future__ import annotations

import datetime as dt

import fluxer as fluxer
from fluxer.ext import commands

from bot import FullFeatureBot
from cogs.shared import require_account_routes, require_mutations


class AccountFeatures(commands.Cog):
    def __init__(self, bot: FullFeatureBot):
        super().__init__(bot)

    @commands.command(name="user_fetch")
    async def user_fetch(self, ctx: commands.Context, user_id: int):
        """Fetch a public Fluxer user by ID and show display-name details."""
        user = await self.bot.fetch_user(str(user_id))
        await ctx.reply(f"user={user.display_name} created_at={user.created_at.isoformat()}")

    @commands.command(name="user_profile")
    async def user_profile(self, ctx: commands.Context, user_id: int):
        """Fetch a user's Fluxer profile and show basic profile fields."""
        profile = await self.bot.fetch_user_profile(str(user_id))
        await ctx.reply(f"profile user={profile.user.display_name} bio={profile.bio!r}")

    @commands.command(name="user_dm")
    async def user_dm(self, ctx: commands.Context, user: fluxer.User, *, content: str):
        """Send a direct message to a user. Requires mutations to be enabled."""
        require_mutations(self.bot)
        message = await user.send(content)
        await ctx.reply(f"DM sent in channel={message.channel_id} message_id={message.id}")

    @commands.command(name="apps")
    async def apps(self, ctx: commands.Context):
        """Fetch the current token's default application and application list."""
        require_account_routes(self.bot)
        app = await self.bot.application_info()
        all_apps = await self.bot.fetch_applications()
        await ctx.reply(f"default_app={app.id} total_apps={len(all_apps)}")

    @commands.command(name="app_fetch")
    async def app_fetch(self, ctx: commands.Context, app_id: int):
        """Fetch one OAuth application record by ID."""
        require_account_routes(self.bot)
        app = await self.bot.fetch_application(app_id)
        await ctx.reply(f"app id={app.id} name={app.name!r}")

    @commands.command(name="saved_messages")
    async def saved_messages(self, ctx: commands.Context, limit: int = 20):
        """List saved messages for the current user."""
        require_account_routes(self.bot)
        saved = await self.bot.fetch_saved_messages(limit=limit)
        await ctx.reply(f"saved_messages={len(saved)}")

    @commands.command(name="scheduled_list")
    async def scheduled_list(self, ctx: commands.Context):
        """List scheduled messages for the current user."""
        require_account_routes(self.bot)
        messages = await self.bot.fetch_scheduled_messages()
        await ctx.reply(f"scheduled_messages={len(messages)}")

    @commands.command(name="scheduled_create")
    async def scheduled_create(
        self,
        ctx: commands.Context,
        channel: fluxer.Channel,
        minutes_from_now: int,
        *,
        content: str,
    ):
        """Schedule a message in a channel for a future UTC time."""
        require_account_routes(self.bot)
        scheduled_at = (dt.datetime.now() + dt.timedelta(minutes=minutes_from_now)).replace(
            second=0, microsecond=0
        )
        scheduled = await self.bot.schedule_message(
            channel.id,
            scheduled_local_at=scheduled_at.isoformat(),
            timezone="UTC",
            content=content,
        )
        await ctx.reply(f"scheduled_message_id={scheduled.id}")

    @commands.command(name="scheduled_cancel")
    async def scheduled_cancel(self, ctx: commands.Context, scheduled_message_id: str):
        """Cancel a scheduled message by ID."""
        require_account_routes(self.bot)
        await self.bot.cancel_scheduled_message(scheduled_message_id)
        await ctx.reply("Scheduled message canceled.")

    @commands.command(name="mentions")
    async def mentions(self, ctx: commands.Context, limit: int = 20):
        """List recent mentions for the current user."""
        require_account_routes(self.bot)
        mentions = await self.bot.fetch_mentions(limit=limit)
        await ctx.reply(f"mentions={len(mentions)}")

    @commands.command(name="mentions_read")
    async def mentions_read(self, ctx: commands.Context, *, message_ids: str):
        """Mark comma-separated mention message IDs as read."""
        require_account_routes(self.bot)
        ids = [int(item.strip()) for item in message_ids.split(",") if item.strip()]
        await self.bot.mark_mentions_read(ids)
        await ctx.reply("Mentions marked as read.")

    @commands.command(name="read_states_ack")
    async def read_states_ack(
        self, ctx: commands.Context, channel_id: int, last_message_id: int
    ):
        """Acknowledge a channel read state up to a message ID."""
        require_account_routes(self.bot)
        result = await self.bot.ack_read_states(
            [{"channel_id": str(channel_id), "last_message_id": str(last_message_id)}]
        )
        await ctx.reply(f"ack_read_states response keys={list(result.keys())}")

    @commands.command(name="relationships")
    async def relationships(self, ctx: commands.Context):
        """List relationships for the current user."""
        require_account_routes(self.bot)
        relationships = await self.bot.fetch_relationships()
        await ctx.reply(f"relationships={len(relationships)}")

    @commands.command(name="relationship_nick")
    async def relationship_nick(
        self, ctx: commands.Context, user_id: int, *, nickname: str
    ):
        """Update the nickname stored for a relationship."""
        require_account_routes(self.bot)
        rel = await self.bot.update_relationship_nickname(user_id, nickname)
        await ctx.reply(f"relationship={rel.user_id} nickname={rel.nickname!r}")

    @commands.command(name="gifts")
    async def gifts(self, ctx: commands.Context):
        """List gift codes available to the current user."""
        require_account_routes(self.bot)
        gifts = await self.bot.fetch_gifts()
        await ctx.reply(f"gifts={len(gifts)}")

    @commands.command(name="gift_lookup")
    async def gift_lookup(self, ctx: commands.Context, code: str):
        """Fetch metadata for a gift code."""
        require_account_routes(self.bot)
        gift = await self.bot.fetch_gift_code(code)
        await ctx.reply(f"gift code={gift.code} redeemed={gift.redeemed}")

    @commands.command(name="gift_redeem")
    async def gift_redeem(self, ctx: commands.Context, code: str):
        """Redeem a gift code. Requires mutations to be enabled."""
        require_account_routes(self.bot)
        require_mutations(self.bot)
        await self.bot.redeem_gift_code(code)
        await ctx.reply("Gift redemption request sent.")

    @commands.command(name="settings")
    async def settings(self, ctx: commands.Context):
        """Fetch current-user settings."""
        require_account_routes(self.bot)
        settings = await self.bot.fetch_user_settings()
        await ctx.reply(f"theme={settings.theme} locale={settings.locale!r}")

    @commands.command(name="settings_update")
    async def settings_update(self, ctx: commands.Context, *, locale: str):
        """Update the current user's locale setting."""
        require_account_routes(self.bot)
        require_mutations(self.bot)
        updated = await self.bot.update_user_settings(locale=locale)
        await ctx.reply(f"updated locale={updated.locale!r}")

    @commands.command(name="connections")
    async def connections(self, ctx: commands.Context):
        """List external connections linked to the current user."""
        require_account_routes(self.bot)
        connections = await self.bot.fetch_user_connections()
        await ctx.reply(f"connections={len(connections)}")

    @commands.command(name="auth_sessions")
    async def auth_sessions(self, ctx: commands.Context):
        """List authentication sessions for the current user."""
        require_account_routes(self.bot)
        sessions = await self.bot.fetch_auth_sessions()
        await ctx.reply(f"auth_sessions={len(sessions)}")

    @commands.command(name="mfa_state")
    async def mfa_state(self, ctx: commands.Context):
        """Fetch the current user's MFA summary."""
        require_account_routes(self.bot)
        mfa_state = await self.bot.fetch_mfa_state()
        await ctx.reply(f"mfa_enabled={mfa_state.enabled}")

    @commands.command(name="webauthn")
    async def webauthn(self, ctx: commands.Context):
        """List WebAuthn credentials for the current user."""
        require_account_routes(self.bot)
        credentials = await self.bot.fetch_webauthn_credentials()
        await ctx.reply(f"webauthn_credentials={len(credentials)}")

    @commands.command(name="authorized_ips")
    async def authorized_ips(self, ctx: commands.Context):
        """List authorized IP records for the current user."""
        require_account_routes(self.bot)
        ips = await self.bot.fetch_authorized_ips()
        await ctx.reply(f"authorized_ips={len(ips)}")

    @commands.command(name="data_harvest")
    async def data_harvest(self, ctx: commands.Context):
        """Request a current-user data export or harvest."""
        require_account_routes(self.bot)
        harvest = await self.bot.request_data_harvest()
        await ctx.reply(f"harvest id={harvest.id} status={harvest.status!r}")

    @commands.command(name="theme_create")
    async def theme_create(self, ctx: commands.Context, *, css: str):
        """Create a custom theme from raw CSS. Requires mutations to be enabled."""
        require_account_routes(self.bot)
        require_mutations(self.bot)
        theme = await self.bot.create_theme(css)
        await ctx.reply(f"theme id={theme.id}")


async def setup(bot: FullFeatureBot):
    await bot.add_cog(AccountFeatures(bot))
