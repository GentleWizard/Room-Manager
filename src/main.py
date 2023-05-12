import discord
import os
import dotenv
from datetime import datetime
import random
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker


###############################################
#                   SQLITE                    #
###############################################
engine = create_engine('sqlite:///Guilds.db', echo=True)
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()


class Guild(Base):
    __tablename__ = 'guild'
    guild_id = Column(Integer, primary_key=True)
    name = Column(String)
    welcome_enabled = Column(Boolean)
    leave_enabled = Column(Boolean)
    welcome_channel = Column(Integer)
    leave_channel = Column(Integer)
    welcome_message = Column(String)
    leave_message = Column(String)
    welcome_type = Column(String)
    moderation_channel = Column(Integer)
    mod_role = Column(String)
    users = relationship("User", back_populates="guild")


class User(Base):
    __tablename__ = 'user'
    user_id = Column(Integer, primary_key=True)
    name = Column(String)
    discriminator = Column(Integer)
    avatar = Column(String)
    guild_id = Column(Integer, ForeignKey('guild.guild_id', ondelete='CASCADE'),
                      index=True, nullable=False, depends_on='guild.guild_id')
    banned = Column(Boolean)
    banned_reason = Column(String)
    banned_at = Column(DateTime)
    banned_by = Column(String)
    times_banned = Column(Integer)
    guild = relationship("Guild", back_populates="users")


Base.metadata.create_all(engine)
#################################################
dotenv.load_dotenv()                            #
bot = discord.Bot(intents=discord.Intents.all())
now = datetime.now()                            #
formatted_time = now.strftime("%H:%M:%S")
bot_token = os.getenv("BOT_TOKEN")              #
bot_id = os.getenv("BOT_ID")                    #
owner_id = os.getenv("OWNER_ID")               #
#################################################

###############################################
#                   COMMANDS                  #
###############################################


@bot.slash_command(name="hello", description="Says hello to the user")
async def hello(ctx):
    await ctx.respond(f"Hello {ctx.author.name}!")


@bot.slash_command(name="welcome_channel", description="Sets the welcome channel")
async def welcome_channel(ctx, channel: discord.Option(discord.SlashCommandOptionType.channel, required=True, description="The channel to send welcome messages in")):
    user = ctx.author
    if user.guild_permissions.administrator or user.id == owner_id or user.id == bot_id:
        guild = session.query(Guild).filter_by(guild_id=ctx.guild.id).first()
        guild.welcome_channel = channel.id
        session.commit()
        await ctx.respond(f"Welcome channel set to {channel.mention}", ephemeral=True)
    else:
        await ctx.respond("You don't have permission to use this command.", ephemeral=True)


@bot.slash_command(name="welcome_message", description="Sets the welcome message")
async def welcome_message(ctx, message: discord.Option(discord.SlashCommandOptionType.string, required=True, description="The message to send to new members")):
    user = ctx.author
    if user.guild_permissions.administrator or user.id == owner_id or user.id == bot_id:
        guild = session.query(Guild).filter_by(guild_id=ctx.guild.id).first()
        guild.welcome_message = message
        session.commit()
        await ctx.respond(f"Welcome message set to {message}", ephemeral=True)
    else:
        await ctx.respond("You don't have permission to use this command.", ephemeral=True)


@bot.slash_command(name="welcome_type", description="Sets the welcome type")
async def welcome_type(ctx, type: discord.Option(discord.SlashCommandOptionType.string, required=True, description="Where to send the welcome message (dm or channel)")):
    user = ctx.author
    if user.guild_permissions.administrator or user.id == owner_id or user.id == bot_id:
        guild = session.query(Guild).filter_by(guild_id=ctx.guild.id).first()
        guild.welcome_type = type
        session.commit()
        await ctx.respond(f"Welcome type set to {type}", ephemeral=True)
    else:
        await ctx.respond("You don't have permission to use this command.", ephemeral=True)


@bot.slash_command(name="leave_message", description="Sets the leave message")
async def leave_message(ctx, message: discord.Option(discord.SlashCommandOptionType.string, required=True, description="The message to send the member leave channel")):
    user = ctx.author
    if user.guild_permissions.administrator or user.id == owner_id or user.id == bot_id:
        guild = session.query(Guild).filter_by(guild_id=ctx.guild.id).first()
        guild.leave_message = message
        session.commit()
        await ctx.respond(f"Leave message set to {message}", ephemeral=True)
    else:
        await ctx.respond("You don't have permission to use this command.", ephemeral=True)


@bot.slash_command(name="leave_channel", description="Sets the leave channel")
async def leave_channel(ctx, channel: discord.Option(discord.SlashCommandOptionType.channel, required=True, description="The channel to send leave messages in")):
    user = ctx.author
    if user.guild_permissions.administrator or user.id == owner_id or user.id == bot_id:
        guild = session.query(Guild).filter_by(guild_id=ctx.guild.id).first()
        guild.leave_channel = channel.id
        session.commit()
        await ctx.respond(f"Leave channel set to {channel.mention}", ephemeral=True)
    else:
        await ctx.respond("You don't have permission to use this command.", ephemeral=True)


@bot.slash_command(name="welcome_enabled", description="Enables or disables welcome messages")
async def welcome_enabled(ctx, enabled: discord.Option(discord.SlashCommandOptionType.boolean, required=True, description="Whether to enable or disable welcome messages (True or False))")):
    user = ctx.author
    if user.guild_permissions.administrator or user.id == owner_id or user.id == bot_id:
        guild = session.query(Guild).filter_by(guild_id=ctx.guild.id).first()
        guild.welcome_enabled = enabled
        session.commit()
        await ctx.respond(f"Welcome messages set to {enabled}", ephemeral=True)
    else:
        await ctx.respond("You don't have permission to use this command.", ephemeral=True)


@bot.slash_command(name="leave_enabled", description="Enables or disables leave messages")
async def leave_enabled(ctx, enabled: discord.Option(discord.SlashCommandOptionType.boolean, required=True, description="Whether to enable or disable leave messages (True or False))")):
    user = ctx.author
    if user.guild_permissions.administrator or user.id == owner_id or user.id == bot_id:
        guild = session.query(Guild).filter_by(guild_id=ctx.guild.id).first()
        guild.leave_enabled = enabled
        session.commit()
        await ctx.respond(f"Leave messages set to {enabled}", ephemeral=True)
    else:
        await ctx.respond("You don't have permission to use this command.", ephemeral=True)


@bot.slash_command(name="roll", description="Rolls a dice")
async def roll(ctx, sides: discord.Option(discord.SlashCommandOptionType.integer, required=True, description="how many sides the dice has"), dice: discord.Option(discord.SlashCommandOptionType.integer, required=False, description="how many dice to roll")):

    if dice is None or dice == 0:
        await ctx.respond(f"You rolled a {random.randint(1, sides)}")
    elif dice > 0:
        dice_list = []
        for _ in range(dice):
            random_number = random.randint(1, sides)
            dice_list.append(random_number)
        await ctx.respond(f"You rolled a {dice}d{sides} and got {sum(dice_list)}")


@bot.slash_command(name="ping", description="Pings the bot.")
async def ping(ctx):
    await ctx.respond(f"Pong! {int(bot.latency * 1000)}ms", ephemeral=True)


@bot.slash_command(name="help", description="Shows the help menu")
async def help(ctx):
    embed = discord.Embed(
        title="Help", description="This is the help menu for the bot.", color=0x00ff00)
    embed.add_field(
        name="Commands", value="This is the commands section of the help menu. Here you can find all the commands for the bot.", inline=False)
    embed.add_field(name="Moderation",
                    value="This is the moderation section of the help menu. Here you can find all the moderation commands for the bot.", inline=False)
    embed.add_field(
        name="Config", value="This is the config section of the help menu. Here you can find all the config commands for the bot.", inline=False)
    embed.set_footer(
        text="If you need more help, join the support server: https://discord.gg/")
    view = HelpMenu()
    message = await ctx.respond(embed=embed, view=view, ephemeral=True)
    view.message = message


@bot.slash_command(name="clean", description="Gets rid of all bots messages in specified range")
async def clean_messages(ctx, amount: discord.Option(discord.SlashCommandOptionType.integer, required=True, description="how many messages to delete")):
    delete_amount = int(amount)
    if delete_amount > 100:
        await ctx.respond("You can only delete 100 messages at a time.", ephemeral=True)
        return
    if delete_amount < 1:
        await ctx.respond("You must delete at least 1 message.", ephemeral=True)
        return
    messages_to_delete = []
    async for message in ctx.channel.history(limit=delete_amount):
        messages_to_delete.append(message)
        await ctx.channel.delete_messages(messages_to_delete)

    await ctx.respond(f"{delete_amount} messages deleted.", ephemeral=True)


@bot.slash_command(name="embed_message", description="Creates an embeded message")
async def embed_message(ctx, title: discord.Option(discord.SlashCommandOptionType.string, required=True, description="Title of the embed"),
                        description: discord.Option(discord.SlashCommandOptionType.string, required=False, description="Description of the embed"),
                        field_one: discord.Option(discord.SlashCommandOptionType.string, required=False, description="The first field of the embed"),
                        field_one_context: discord.Option(discord.SlashCommandOptionType.string, required=False, description="The context of the first field of the embed"),
                        field_two: discord.Option(discord.SlashCommandOptionType.string, required=False, description="The second field of the embed"),
                        field_two_context: discord.Option(discord.SlashCommandOptionType.string, required=False, description="The context of the second field of the embed"),
                        field_three: discord.Option(discord.SlashCommandOptionType.string, required=False, description="The third field of the embed"),
                        field_three_context: discord.Option(discord.SlashCommandOptionType.string, required=False, description="The context of the third field of the embed"),
                        field_four: discord.Option(discord.SlashCommandOptionType.string, required=False, description="The fourth field of the embed"),
                        field_four_context: discord.Option(discord.SlashCommandOptionType.string, required=False, description="The context of the fourth field of the embed"),
                        field_five: discord.Option(discord.SlashCommandOptionType.string, required=False, description="The fifth field of the embed"),
                        field_five_context: discord.Option(discord.SlashCommandOptionType.string, required=False, description="The context of the fifth field of the embed"),
                        time_stamp: discord.Option(discord.SlashCommandOptionType.string, required=False, description="Y or N question (defult is N)"),
                        footer: discord.Option(discord.SlashCommandOptionType.string, required=False, description="Footer of the embed"),
                        color: discord.Option(discord.SlashCommandOptionType.integer, required=False, description="Color of the embed (number)"),
                        ):

    embed = discord.Embed()

    embed.set_author(name=ctx.author, icon_url=ctx.author.avatar.url)

    embed.set_footer("Powered by Room Manager")

    if title is not None:
        embed.title = title

    if description is not None:
        embed.description = description

    if time_stamp and time_stamp.lower() in ["y", "yes"]:
        embed.timestamp = datetime.now()
    elif time_stamp and time_stamp.lower() in ["n", "no"] or None:
        embed.timestamp = None

    if field_one is not None:
        embed.add_field(name=field_one, value="")
    if field_one_context is not None:
        embed.set_field_at(0, name=field_one, value=field_one_context)

    if field_two is not None:
        embed.add_field(name=field_two, value="")
    if field_two_context is not None:
        embed.set_field_at(1, name=field_two, value=field_two_context)

    if field_three is not None:
        embed.add_field(name=field_three, value="")
    if field_three_context is not None:
        embed.set_field_at(2, name=field_three, value=field_three_context)

    if field_four is not None:
        embed.add_field(name=field_four, value="")
    if field_four_context is not None:
        embed.set_field_at(3, name=field_four, value=field_four_context)

    if field_five is not None:
        embed.add_field(name=field_five, value="")
    if field_five_context is not None:
        embed.set_field_at(4, name=field_five, value=field_five_context)

    if color is not None:
        embed.color = int(color, 16)

    await ctx.respond(embed=embed)


###############################################
#                   GUIs                      #
###############################################


class HelpMenu(discord.ui.View):
    def __init__(self, message=None):
        super().__init__()
        self.message = message

    @discord.ui.button(label="Moderation", style=discord.ButtonStyle.blurple)
    async def modderation_tab(self, button, interaction):
        user = interaction.user
        mod_role = discord.utils.get(user.guild.roles, name=config["mod_role"])
        if user.guild_permissions.administrator or mod_role in user.roles or user.id == server_owner_id:
            embed = discord.Embed(title="Moderation Settings")
            embed.add_field(name="Ban Settings", value="test")
            view = ModerationHelpMenu()

            await interaction.response.edit_message(embed=embed, view=view)
        else:
            await interaction.response.send_message("You do not have permission to open this menu.", ephemeral=True)
        await interaction.response.edit_message(embed=embed, view=view)

    @discord.ui.button(label="Commands", style=discord.ButtonStyle.blurple)
    async def commands_tab(self, button, interaction):
        embed = discord.Embed(title="Commands")
        embed.add_field(name="Ban", value="test")
        view = CommandsHelpMenu()

        await interaction.response.edit_message(embed=embed, view=view)

    @discord.ui.button(label="Config", style=discord.ButtonStyle.blurple)
    async def config_tab(self, button, interaction):
        user = interaction.user
        mod_role = discord.utils.get(user.guild.roles, name=config["mod_role"])
        if user.guild_permissions.administrator or mod_role in user.roles or user.id == bot_mod_id:
            embed = discord.Embed(title="Commands")
            embed.add_field(name="Ban", value="test")
            view = ConfigHelpMenu()

            await interaction.response.edit_message(embed=embed, view=view)
        else:
            await interaction.response.send_message("You do not have permission to open this menu.", ephemeral=True)
        await interaction.response.edit_message(embed=embed, view=view)

    @discord.ui.button(label="Exit", style=discord.ButtonStyle.red)
    async def exit_button(self, button, interaction):
        await interaction.message.delete()
        await interaction.response.edit_message("Closed", ephemeral=True)
        self.stop()


class ModerationHelpMenu(discord.ui.View):
    def __init__(self, message=None):
        super().__init__()
        self.message = message

    @discord.ui.button(label="Ban", style=discord.ButtonStyle.blurple)
    async def ban_button(self, button, interaction):
        embed = discord.Embed()
        embed.add_field(name="Ban", value="test")
        view = ModerationHelpMenu()

        await interaction.response.edit_message(embed=embed, view=view)

    @discord.ui.button(label="Kick", style=discord.ButtonStyle.blurple)
    async def kick_button(self, button, interaction):
        embed = discord.Embed()
        embed.add_field(name="Kick", value="test")
        view = ModerationHelpMenu()

        await interaction.response.edit_message(embed=embed, view=view)

    @discord.ui.button(label="Mute", style=discord.ButtonStyle.blurple)
    async def mute_button(self, button, interaction):
        embed = discord.Embed()
        embed.add_field(name="Mute", value="test")
        view = ModerationHelpMenu()

        await interaction.response.edit_message(embed=embed, view=view)

    @discord.ui.button(label="Unmute", style=discord.ButtonStyle.blurple)
    async def unmute_button(self, button, interaction):
        embed = discord.Embed()
        embed.add_field(name="Unmute", value="test")
        view = ModerationHelpMenu()

        await interaction.response.edit_message(embed=embed, view=view)

    @discord.ui.button(label="back", style=discord.ButtonStyle.red)
    async def exit_button(self, button, interaction):
        embed = discord.Embed(
            title="Help", description="This is the help menu for the bot.", color=0x00ff00)
        embed.add_field(
            name="Commands", value="This is the commands section of the help menu. Here you can find all the commands for the bot.", inline=False)
        embed.add_field(name="Moderation",
                        value="This is the moderation section of the help menu. Here you can find all the moderation commands for the bot.", inline=False)
        embed.add_field(
            name="Config", value="This is the config section of the help menu. Here you can find all the config commands for the bot.", inline=False)
        embed.set_footer(
            text="If you need more help, join the support server: https://discord.gg/")
        view = HelpMenu()

        await interaction.response.edit_message(embed=embed, view=view)
        self.stop()


class CommandsHelpMenu(discord.ui.View):
    def __init__(self, message=None):
        super().__init__()
        self.message = message

    @discord.ui.button(label="Ping", style=discord.ButtonStyle.blurple)
    async def ping_button(self, button, interaction):
        embed = discord.Embed()
        embed.add_field(name="Ping", value="test")
        view = CommandsHelpMenu()

        await interaction.response.edit_message(embed=embed, view=view)

    @discord.ui.button(label="Help", style=discord.ButtonStyle.blurple)
    async def help_button(self, button, interaction):
        embed = discord.Embed()
        embed.add_field(name="Help", value="Shows this menu")
        view = CommandsHelpMenu()

        await interaction.response.edit_message(embed=embed, view=view)

    @discord.ui.button(label="clean", style=discord.ButtonStyle.blurple)
    async def clean_button(self, button, interaction):
        embed = discord.Embed()
        embed.add_field(name="Clean", value="test")
        view = CommandsHelpMenu()

        await interaction.response.edit_message(embed=embed, view=view)

    @discord.ui.button(label="back", style=discord.ButtonStyle.red)
    async def back_button(self, button, interaction):
        embed = discord.Embed(
            title="Help", description="This is the help menu for the bot.", color=0x00ff00)
        embed.add_field(
            name="Commands", value="This is the commands section of the help menu. Here you can find all the commands for the bot.", inline=False)
        embed.add_field(name="Moderation",
                        value="This is the moderation section of the help menu. Here you can find all the moderation commands for the bot.", inline=False)
        embed.add_field(
            name="Config", value="This is the config section of the help menu. Here you can find all the config commands for the bot.", inline=False)
        embed.set_footer(
            text="If you need more help, join the support server: https://discord.gg/")
        view = HelpMenu()

        await interaction.response.edit_message(embed=embed, view=view)
        self.stop()


class ConfigHelpMenu(discord.ui.View):
    def __init__(self, message=None):
        super().__init__()
        self.message = message

    @discord.ui.button(label="Prefix", style=discord.ButtonStyle.blurple)
    async def prefix_button(self, button, interaction):
        embed = discord.Embed()
        embed.add_field(name="Prefix", value="test")
        view = ConfigHelpMenu()

        await interaction.response.edit_message(embed=embed, view=view)

    @discord.ui.button(label="Welcome", style=discord.ButtonStyle.blurple)
    async def welcome_button(self, button, interaction):
        embed = discord.Embed()
        embed.add_field(name="Welcome", value="test")
        view = ConfigHelpMenu()

        await interaction.response.edit_message(embed=embed, view=view)

    @discord.ui.button(label="back", style=discord.ButtonStyle.red)
    async def back_button(self, button, interaction):
        embed = discord.Embed(
            title="Help", description="This is the help menu for the bot.", color=0x00ff00)
        embed.add_field(
            name="Commands", value="This is the commands section of the help menu. Here you can find all the commands for the bot.", inline=False)
        embed.add_field(name="Moderation",
                        value="This is the moderation section of the help menu. Here you can find all the moderation commands for the bot.", inline=False)
        embed.add_field(
            name="Config", value="This is the config section of the help menu. Here you can find all the config commands for the bot.", inline=False)
        embed.set_footer(
            text="If you need more help, join the support server: https://discord.gg/")
        view = HelpMenu()

        await interaction.response.edit_message(embed=embed, view=view)
        self.stop()


class WelcomeSettingsModal(discord.ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.add_item(discord.ui.InputText(
            label="message", style=discord.InputTextStyle.long))

    async def callback(self, interaction: discord.Interaction):
        embed = discord.Embed(title="test")
        embed.add_field(name="Message:", value=self.children[0].value)
        await interaction.response.send_message(embed=[embed])

    @discord.ui.button(label="back", custom_id="back", style=discord.ButtonStyle.primary)
    async def back_button(self, button, interaction):
        embed = discord.Embed(
            title="Other Settings")

        view = OtherSettings()
        await interaction.response.edit_message(embed=embed, view=view)
###############################################
#                   EVENTS                    #
###############################################


@bot.event
async def on_member_join(member):
    if member.bot:
        return
    else:
        new_user = User(user_id=member.id, name=member.name, discriminator=member.discriminator,
                        avatar=member.avatar.url, guild_id=member.guild.id)
        session.merge(new_user)
        session.commit()

    guild = session.query(Guild).filter_by(guild_id=member.guild.id).first()

    if guild.welcome_type == "channel":
        channel = bot.get_channel(guild.welcome_channel)
        message = guild.welcome_message
        user = member.mention
        server = member.guild
        await channel.send(f"{message.format(user=user, server='**' + member.guild.name + '**')}")

    elif guild.welcome_type == "dm":
        message = guild.welcome_message
        user = member.mention
        server = member.guild
        await member.send(f"{message.format(user=user, server='**' + member.guild.name + '**')}")

    elif guild.welcome_type == "both":
        channel = bot.get_channel(guild.welcome_channel)
        message = guild.welcome_message
        user = member.mention
        server = member.guild
        await channel.send(f"{message.format(user=user, server='**' + member.guild.name + '**')}")
        await member.send(f"{message.format(user=user, server='**' + member.guild.name + '**')}")
    elif guild.welcome_type == None:
        channel = bot.get_channel(guild.moderation_channel)
        message = guild.welcome_message
        user = member.mention
        server = member.guild
        await member.send(f"{message.format(user=user, server='**' + member.guild.name + '**')}")
        await channel.send(f"Please set a welcome type. (channel, dm, both)")
    elif guild.welcome_channel is None:
        channel = bot.get_channel(guild.welcome_channel)
        message = guild.welcome_message
        user = member.mention
        server = member.guild
        await member.guild.owner.send(f"{member.mention} has joined. Make sure to set a welcome channel, or set welcome type to 'dm'.")
        await member.send(f"{message.format(user=user, server='**' + member.guild.name + '**')}")
    else:
        channel = bot.get_channel(guild.moderation_channel)
        await channel.send(f"Error: Something went wrong displaying join message. Please contact the bot owner.")
        return


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")

    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="Mr.Wizard#5853"))


@bot.event
async def on_member_ban(guild):
    logs = await guild.audit_logs(limit=1, action=discord.AuditLogAction.ban).flatten()
    logs = logs[0]

    async def on_member_ban(guild, member):
        logs = await guild.audit_logs(limit=1, action=discord.AuditLogAction.ban).flatten()
        logs = logs[0]
        if logs.target == member:
            user = session.query(member).filter_by(
                user_id=member.id, guild_id=member.guild.id).first()
            if user is not None:
                user.banned = True
                user.banned_by = logs.user.name
                user.banded_at = logs.created_at.strftime('%Y-%m-%d %H:%M:%S')
                user.ban_reason = logs.reason
                user.times_banned += 1
                session.commit()
                print(
                    f'Member {member.name} was banned by {logs.user.name} at {logs.created_at} with reason: {logs.reason}')
            else:
                print(f'Member {member.name} was not banned')


@bot.event
async def on_member_unban(guild, user):
    user = session.query(User).filter_by(user_id=user.id).first()
    user.banned = False
    user.banned_by = None
    user.banded_at = None
    user.ban_reason = None
    session.commit()
    print(f'Member {user.name} was unbanned')


# @bot.event
# async def on_member_remove(member):
#     try:
#         await member.guild.fetch_ban(member)
#         # The user has been banned
#     except discord.NotFound:
#         # The user has left


@bot.event
async def on_guild_join(guild):
    new_guild = Guild(guild_id=guild.id, name=guild.name, welcome_enabled=False, welcome_channel=None,
                      welcome_message=None, welcome_type="dm", leave_enabled=False, leave_channel=None, leave_message=None)
    session.merge(new_guild)
    session.commit()
    print(f'Guild {guild.name} has been joined.')


print(f"database: {sqlalchemy.__version__}")
print(f"Using: Pycord {discord.__version__}")
bot.run(bot_token)
