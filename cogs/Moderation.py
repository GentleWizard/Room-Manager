import discord
from discord.ext import commands
import typing
import asyncio


class Ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(name="ping", description="Ping the bot")
    async def ping(self, ctx):
        """Ping the bot"""
        await ctx.send(f"Pong! {round(self.bot.latency * 1000)}ms")


class Mute(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.muted_role = None

    async def set_channel_permissions(self):
        for channel in self.guild.channels:
            if channel.type == discord.ChannelType.text:
                if channel.permissions_for(self.muted_role).send_messages is None:
                    await channel.set_permissions(self.muted_role, send_messages=False)

        for channel in self.guild.voice_channels:
            if channel.type == discord.ChannelType.voice:
                if channel.permissions_for(self.muted_role).speak is None:
                    await channel.set_permissions(self.muted_role, speak=False)

    async def create_muted_role(self, guild):
        self.muted_role = await guild.create_role(name="Muted", reason="Created muted role.",
                                                  colour=discord.Colour(0xFf0000), hoist=True, mentionable=False)
        await self.set_channel_permissions()

    async def add_member_to_muted_role(self, member, reason):
        await member.add_roles(self.muted_role, reason=reason)

    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
        await self.set_channel_permissions()

    @discord.slash_command(name="mute", description="Mute a user")
    @commands.has_permissions(manage_roles=True)
    async def mute(self, ctx, member: discord.Member, seconds: typing.Optional[int] = 0,
                   minutes: typing.Optional[int] = 0, hours: typing.Optional[int] = 0,
                   reason: typing.Optional[str] = "No reason provided."):
        """Mute a user"""
        if discord.utils.get(ctx.guild.roles, name="Muted") is None:
            await self.create_muted_role(ctx.guild)

        if seconds == 0 and minutes == 0 and hours == 0:
            await ctx.respond("Please specify a time to mute the user for.", ephemeral=True)
            return

        if member == ctx.author:
            await ctx.respond("You cannot mute yourself.", ephemeral=True)
            return

        if member == ctx.guild.owner:
            await ctx.respond("You cannot mute the server owner.", ephemeral=True)
            return

        if member == ctx.guild.me:
            await ctx.respond("You cannot mute me.", ephemeral=True)
            return

        if member.top_role > ctx.author.top_role:
            await ctx.respond("You cannot mute someone with a higher role than you.", ephemeral=True)
            return
        else:
            if discord.utils.get(ctx.guild.roles, name="Muted") in member.roles:
                await ctx.respond(f"{member.mention} is already muted.", ephemeral=True)
            else:
                await self.add_member_to_muted_role(member, reason)

                if seconds >= 60:
                    minutes += seconds // 60
                    seconds = seconds % 60
                if minutes >= 60:
                    hours += minutes // 60
                    minutes = minutes % 60

                await member.send(
                    f"**You have been muted in {ctx.guild.name}** for {hours} hours, {minutes} minutes, {seconds} seconds.\nReason: {reason}")
                await ctx.respond(
                    f"Muted {member.mention} for {hours} hours, {minutes} minutes, {seconds} seconds.\n{reason}",
                    ephemeral=True)

                await asyncio.sleep(seconds + (minutes * 60) + (hours * 3600))
                await member.remove_roles(discord.utils.get(ctx.guild.roles, name="Muted"), reason="Mute expired.")

    @mute.error
    async def mute_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.respond(error, ephemeral=True)


class Unmute(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(name="unmute", description="Unmute a user")
    @commands.has_permissions(manage_roles=True)
    async def unmute(self, ctx, member: discord.Member, reason: typing.Optional[str] = "No reason provided."):
        """Unmute a user"""
        if member == ctx.author:
            await ctx.respond("You cannot unmute yourself.", ephemeral=True)
            return

        if member == ctx.guild.me:
            await ctx.respond("Thanks for trying but, you cannot unmute me. :cry:", ephemeral=True)
            return

        if member.top_role > ctx.author.top_role:
            await ctx.respond("You cannot unmute someone with a higher role than you.", ephemeral=True)
            return
        else:
            if discord.utils.get(ctx.guild.roles, name="Muted") in member.roles:
                await member.remove_roles(discord.utils.get(ctx.guild.roles, name="Muted"), reason=reason)
                await member.send(f"**You have been unmuted in {ctx.guild.name}**.\nReason: {reason}")
                await ctx.respond(f"Unmuted {member.mention}.\n{reason}", ephemeral=True)
            else:
                await ctx.respond(f"{member.mention} is not muted.", ephemeral=True)

    @unmute.error
    async def unmute_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.respond(error, ephemeral=True)


def setup(bot):
    bot.add_cog(Ping(bot))
    bot.add_cog(Mute(bot))
    bot.add_cog(Unmute(bot))
