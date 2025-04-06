import discord
from discord.ext import commands
from discord.utils import escape_markdown
from dotenv import load_dotenv
import datetime
import os

load_dotenv()
LOG_CHANNEL_ID = int(os.getenv("LOG_CHANNEL_ID"))

class LogEvents(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def get_log_channel(self, guild):
        return self.bot.get_channel(LOG_CHANNEL_ID)

    def create_log_embed(self, title, description, user, emoji, color):
        embed = discord.Embed(
            title=f"{emoji} {title}",
            description=description,
            color=color,
            timestamp=datetime.datetime.utcnow()
        )
        embed.set_author(name=str(user), icon_url=user.display_avatar.url)
        return embed

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if before.author.bot or before.content == after.content:
            return
        channel = self.get_log_channel(before.guild)
        if channel:
            embed = self.create_log_embed(
                "Message Edited",
                f"**User:** {before.author.mention}\n**Channel:** {before.channel.name}\n**Before:** {escape_markdown(before.content)}\n**After:** {escape_markdown(after.content)}",
                before.author,
                "✏️",
                discord.Color.gold()
            )
            await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.author.bot:
            return
        channel = self.get_log_channel(message.guild)
        if channel:
            deleter = "Unknown"
            async for entry in message.guild.audit_logs(limit=1, action=discord.AuditLogAction.message_delete):
                if entry.target.id == message.author.id:
                    deleter = entry.user.mention
            embed = self.create_log_embed(
                "Message Deleted",
                f"**Author:** {message.author.mention}\n**Deleted by:** {deleter}\n**Channel:** {message.channel.name}\n**Content:** {escape_markdown(message.content)}",
                message.author,
                "🗑️",
                discord.Color.red()
            )
            await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = self.get_log_channel(member.guild)
        if channel:
            embed = self.create_log_embed("Member Joined", f"{member.mention} joined the server!", member, "📥", discord.Color.green())
            await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        channel = self.get_log_channel(member.guild)
        if not channel:
            return

        async for entry in member.guild.audit_logs(limit=1, action=discord.AuditLogAction.kick):
            if entry.target.id == member.id:
                embed = self.create_log_embed("Member Kicked", f"{member.mention} was kicked by {entry.user.mention}", entry.user, "🥾", discord.Color.red())
                await channel.send(embed=embed)
                return

        embed = self.create_log_embed("Member Left", f"{member.mention} left the server!", member, "📤", discord.Color.orange())
        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        channel = self.get_log_channel(after.guild)
        if not channel:
            return

        if before.nick != after.nick:
            embed = self.create_log_embed(
                "Nickname Changed",
                f"**User:** {after.mention}\n**Before:** {before.nick or before.name}\n**After:** {after.nick or after.name}",
                after,
                "📝",
                discord.Color.blue()
            )
            await channel.send(embed=embed)

        added_roles = [role for role in after.roles if role not in before.roles]
        removed_roles = [role for role in before.roles if role not in after.roles]

        async for entry in after.guild.audit_logs(limit=5):
            for role in added_roles:
                if entry.target.id == after.id and entry.action == discord.AuditLogAction.member_role_update and role in entry.changes.after:
                    embed = self.create_log_embed("Role Added", f"{entry.user.mention} added **{role.name}** to {after.mention}.", entry.user, "➕", discord.Color.green())
                    await channel.send(embed=embed)
            for role in removed_roles:
                if entry.target.id == after.id and entry.action == discord.AuditLogAction.member_role_update and role in entry.changes.before:
                    embed = self.create_log_embed("Role Removed", f"{entry.user.mention} removed **{role.name}** from {after.mention}.", entry.user, "➖", discord.Color.red())
                    await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        channel = self.get_log_channel(member.guild)
        if not channel:
            return

        if not before.channel and after.channel:
            embed = self.create_log_embed("Joined Voice Channel", f"{member.mention} joined **{after.channel.name}**", member, "🎙️", discord.Color.green())
            await channel.send(embed=embed)
        elif before.channel and not after.channel:
            embed = self.create_log_embed("Left Voice Channel", f"{member.mention} left **{before.channel.name}**", member, "🔇", discord.Color.red())
            await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
        log_channel = self.get_log_channel(channel.guild)
        if log_channel:
            async for entry in channel.guild.audit_logs(limit=1, action=discord.AuditLogAction.channel_create):
                embed = self.create_log_embed("Channel Created", f"{entry.user.mention} created **#{channel.name}**.", entry.user, "📁", discord.Color.green())
                await log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
        log_channel = self.get_log_channel(channel.guild)
        if log_channel:
            async for entry in channel.guild.audit_logs(limit=1, action=discord.AuditLogAction.channel_delete):
                embed = self.create_log_embed("Channel Deleted", f"{entry.user.mention} deleted **#{channel.name}**.", entry.user, "🗂️", discord.Color.red())
                await log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_ban(self, guild, user):
        channel = self.get_log_channel(guild)
        if channel:
            async for entry in guild.audit_logs(limit=1, action=discord.AuditLogAction.ban):
                if entry.target.id == user.id:
                    embed = self.create_log_embed("Member Banned", f"{entry.user.mention} banned {user.mention}.", entry.user, "🔨", discord.Color.red())
                    await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_unban(self, guild, user):
        channel = self.get_log_channel(guild)
        if channel:
            async for entry in guild.audit_logs(limit=1, action=discord.AuditLogAction.unban):
                if entry.target.id == user.id:
                    embed = self.create_log_embed("Member Unbanned", f"{entry.user.mention} unbanned {user.mention}.", entry.user, "🛡️", discord.Color.green())
                    await channel.send(embed=embed)

async def setup(bot):
    await bot.add_cog(LogEvents(bot))