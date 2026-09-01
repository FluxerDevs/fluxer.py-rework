from __future__ import annotations

import fluxer as fluxer
from fluxer.ext import commands

from bot import FullFeatureBot
from cogs.shared import require_mutations, resolve_guild


class GuildFeatures(commands.Cog):
    def __init__(self, bot: FullFeatureBot):
        super().__init__(bot)

    @commands.command(name="guilds")
    async def guilds(self, ctx: commands.Context, limit: int = 50):
        """List guilds visible to the current token."""
        iterator = self.bot.fetch_guilds(limit=limit)
        guilds = await iterator.flatten()
        names = ", ".join(g.name or str(g.id) for g in guilds[:10])
        await ctx.reply(f"Fetched {len(guilds)} guild(s): {names}")

    @commands.command(name="guild_fetch")
    async def guild_fetch(self, ctx: commands.Context, guild_id: int):
        """Fetch one guild by ID and show basic details."""
        guild = await self.bot.fetch_guild(str(guild_id))
        await ctx.reply(f"Guild {guild.id}: name={guild.name!r} members={guild.member_count}")

    @commands.command(name="guild_channels")
    async def guild_channels(self, ctx: commands.Context, guild_id: int | None = None):
        """List channels for a guild or the current guild."""
        guild = await resolve_guild(ctx, guild_id)
        channels = await guild.fetch_channels()
        await ctx.reply(f"Guild {guild.id} has {len(channels)} channel(s).")

    @commands.command(name="channel_fetch")
    async def channel_fetch(self, ctx: commands.Context, channel_id: int):
        """Fetch one channel by ID and show basic metadata."""
        channel = await self.bot.fetch_channel(str(channel_id))
        await ctx.reply(f"Channel {channel.id}: name={channel.name!r} type={channel.type}")

    @commands.command(name="channel_edit_name")
    async def channel_edit_name(
        self, ctx: commands.Context, channel: fluxer.Channel, *, name: str
    ):
        """Rename a channel. Requires mutations to be enabled."""
        require_mutations(self.bot)
        updated = await channel.edit(name=name)
        await ctx.reply(f"Channel renamed to {updated.name!r}.")

    @commands.command(name="channel_delete")
    async def channel_delete(self, ctx: commands.Context, channel: fluxer.Channel):
        """Delete a channel. Requires mutations to be enabled."""
        require_mutations(self.bot)
        await channel.delete()
        await ctx.reply("Channel deleted.")

    @commands.command(name="channel_set_perms")
    async def channel_set_perms(
        self, ctx: commands.Context, channel: fluxer.Channel, target_id: int
    ):
        """Set channel permission overwrites for a target ID."""
        require_mutations(self.bot)
        await channel.set_permissions(target_id, send_messages=True, view_channel=True)
        await ctx.reply("Permission overwrite set.")

    @commands.command(name="channel_clear_perms")
    async def channel_clear_perms(
        self, ctx: commands.Context, channel: fluxer.Channel, target_id: int
    ):
        """Clear channel permission overwrites for a target ID."""
        require_mutations(self.bot)
        await channel.set_permissions(target_id, overwrite=None)
        await ctx.reply("Permission overwrite removed.")

    @commands.command(name="channel_invites")
    async def channel_invites(self, ctx: commands.Context, channel: fluxer.Channel):
        """List invites for a channel."""
        invites = await channel.invites()
        await ctx.reply(f"Channel invites: {len(invites)}")

    @commands.command(name="channel_invite_create")
    async def channel_invite_create(self, ctx: commands.Context, channel: fluxer.Channel):
        """Create a one-use invite for a channel. Requires mutations to be enabled."""
        require_mutations(self.bot)
        invite = await channel.create_invite(max_age=3600, max_uses=1)
        await ctx.reply(f"Invite created: {invite.code}")

    @commands.command(name="guild_roles")
    async def guild_roles(self, ctx: commands.Context, guild_id: int | None = None):
        """List roles for a guild or the current guild."""
        guild = await resolve_guild(ctx, guild_id)
        roles = await guild.fetch_roles()
        await ctx.reply(f"Guild {guild.id} roles: {len(roles)}")

    @commands.command(name="guild_role_create")
    async def guild_role_create(
        self, ctx: commands.Context, guild_id: int | None = None, *, name: str
    ):
        """Create a role in a guild. Requires mutations to be enabled."""
        require_mutations(self.bot)
        guild = await resolve_guild(ctx, guild_id)
        role = await guild.create_role(name=name, mentionable=True)
        await ctx.reply(f"Created role id={role.id} name={role.name}")

    @commands.command(name="role_edit")
    async def role_edit(self, ctx: commands.Context, role: fluxer.Role, *, name: str):
        """Rename a role. Requires mutations to be enabled."""
        require_mutations(self.bot)
        updated = await role.edit(name=name)
        await ctx.reply(f"Role updated: {updated.id} -> {updated.name}")

    @commands.command(name="role_delete")
    async def role_delete(self, ctx: commands.Context, role: fluxer.Role):
        """Delete a role. Requires mutations to be enabled."""
        require_mutations(self.bot)
        await role.delete()
        await ctx.reply("Role deleted.")

    @commands.command(name="guild_members")
    async def guild_members(
        self, ctx: commands.Context, guild_id: int | None = None, limit: int = 25
    ):
        """Fetch members for a guild."""
        guild = await resolve_guild(ctx, guild_id)
        members = await guild.fetch_members(limit=limit)
        await ctx.reply(f"Fetched {len(members)} members.")

    @commands.command(name="guild_member")
    async def guild_member(self, ctx: commands.Context, guild_id: int, user_id: int):
        """Fetch one guild member by guild ID and user ID."""
        member = await self.bot.fetch_member(guild_id, user_id)
        await ctx.reply(f"Member fetched: {member.display_name} roles={len(member.roles)}")

    @commands.command(name="member_edit_nick")
    async def member_edit_nick(
        self,
        ctx: commands.Context,
        guild_id: int,
        user_id: int,
        *,
        nick: str,
    ):
        """Edit a member nickname. Requires mutations to be enabled."""
        require_mutations(self.bot)
        member = await self.bot.fetch_member(guild_id, user_id)
        await member.edit(nick=nick)
        await ctx.reply("Member nickname updated.")

    @commands.command(name="member_add_role")
    async def member_add_role(
        self, ctx: commands.Context, guild_id: int, user_id: int, role_id: int
    ):
        """Add a role to a member. Requires mutations to be enabled."""
        require_mutations(self.bot)
        member = await self.bot.fetch_member(guild_id, user_id)
        await member.add_role(role_id)
        await ctx.reply("Role added to member.")

    @commands.command(name="member_remove_role")
    async def member_remove_role(
        self, ctx: commands.Context, guild_id: int, user_id: int, role_id: int
    ):
        """Remove a role from a member. Requires mutations to be enabled."""
        require_mutations(self.bot)
        member = await self.bot.fetch_member(guild_id, user_id)
        await member.remove_role(role_id)
        await ctx.reply("Role removed from member.")

    @commands.command(name="guild_search_members")
    async def guild_search_members(self, ctx: commands.Context, guild_id: int, *, query: str):
        """Search guild members by query text."""
        members = await self.bot.search_members(guild_id, query=query, limit=10)
        await ctx.reply(f"Search returned {len(members)} member(s).")

    @commands.command(name="guild_kick")
    @commands.has_permissions(kick_members=True)
    async def guild_kick(self, ctx: commands.Context, user_id: int):
        """Kick a user from the current guild. Requires mutations to be enabled."""
        require_mutations(self.bot)
        guild = await resolve_guild(ctx, None)
        await guild.kick(user_id, reason=f"Requested by {ctx.author.id}")
        await ctx.reply(f"Kicked user {user_id}.")

    @commands.command(name="guild_ban")
    @commands.has_permissions(ban_members=True)
    async def guild_ban(self, ctx: commands.Context, user_id: int):
        """Ban a user from the current guild. Requires mutations to be enabled."""
        require_mutations(self.bot)
        guild = await resolve_guild(ctx, None)
        await guild.ban(user_id, reason=f"Requested by {ctx.author.id}")
        await ctx.reply(f"Banned user {user_id}.")

    @commands.command(name="guild_unban")
    @commands.has_permissions(ban_members=True)
    async def guild_unban(self, ctx: commands.Context, user_id: int):
        """Unban a user from the current guild. Requires mutations to be enabled."""
        require_mutations(self.bot)
        guild = await resolve_guild(ctx, None)
        await guild.unban(user_id, reason=f"Requested by {ctx.author.id}")
        await ctx.reply(f"Unbanned user {user_id}.")

    @commands.command(name="guild_bans")
    async def guild_bans(self, ctx: commands.Context, guild_id: int | None = None):
        """List bans for a guild or the current guild."""
        guild = await resolve_guild(ctx, guild_id)
        bans = await guild.bans()
        await ctx.reply(f"Fetched {len(bans)} ban entries.")

    @commands.command(name="guild_audit")
    async def guild_audit(self, ctx: commands.Context, guild_id: int | None = None, limit: int = 10):
        """Fetch recent guild audit log entries."""
        guild = await resolve_guild(ctx, guild_id)
        audit_log = await guild.audit_logs(limit=limit)
        await ctx.reply(f"Audit entries returned: {len(audit_log.entries)}")

    @commands.command(name="guild_vanity")
    async def guild_vanity(self, ctx: commands.Context, guild_id: int | None = None):
        """Fetch the vanity URL for a guild or the current guild."""
        guild = await resolve_guild(ctx, guild_id)
        vanity = await guild.get_vanity_url()
        await ctx.reply(f"Vanity URL code={vanity.code!r}")

    @commands.command(name="guild_set_vanity")
    async def guild_set_vanity(self, ctx: commands.Context, code: str):
        """Update the current guild's vanity code. Requires mutations to be enabled."""
        require_mutations(self.bot)
        guild = await resolve_guild(ctx, None)
        vanity = await guild.update_vanity_url(code)
        await ctx.reply(f"Updated vanity code={vanity.code!r}")

    @commands.command(name="guild_discovery_status")
    async def guild_discovery_status(self, ctx: commands.Context, guild_id: int | None = None):
        """Fetch discovery status for a guild or the current guild."""
        guild = await resolve_guild(ctx, guild_id)
        status = await guild.discovery_status()
        await ctx.reply(f"Discovery status: {status.status}")

    @commands.command(name="discovery_search")
    async def discovery_search(self, ctx: commands.Context, *, query: str):
        """Search Fluxer discovery for public guilds."""
        guilds = await self.bot.search_discovery_guilds(query=query, limit=10)
        await ctx.reply(f"Discovery search returned {len(guilds)} guild(s).")

    @commands.command(name="guild_emojis")
    async def guild_emojis(self, ctx: commands.Context, guild_id: int | None = None):
        """List guild emojis."""
        guild = await resolve_guild(ctx, guild_id)
        emojis = await guild.fetch_emojis()
        await ctx.reply(f"Guild emojis: {len(emojis)}")

    @commands.command(name="guild_stickers")
    async def guild_stickers(self, ctx: commands.Context, guild_id: int | None = None):
        """List guild stickers."""
        guild = await resolve_guild(ctx, guild_id)
        stickers = await guild.fetch_stickers()
        await ctx.reply(f"Guild stickers: {len(stickers)}")

    @commands.command(name="guild_bulk_emojis")
    async def guild_bulk_emojis(self, ctx: commands.Context, guild_id: int):
        """Demonstrate the bulk emoji route with an empty payload."""
        require_mutations(self.bot)
        result = await self.bot.bulk_create_guild_emojis(guild_id, emojis=[])
        await ctx.reply(f"Bulk emoji operation status={result.status!r}")

    @commands.command(name="guild_bulk_stickers")
    async def guild_bulk_stickers(self, ctx: commands.Context, guild_id: int):
        """Demonstrate the bulk sticker route with an empty payload."""
        require_mutations(self.bot)
        result = await self.bot.bulk_create_guild_stickers(guild_id, stickers=[])
        await ctx.reply(f"Bulk sticker operation status={result.status!r}")


async def setup(bot: FullFeatureBot):
    await bot.add_cog(GuildFeatures(bot))
