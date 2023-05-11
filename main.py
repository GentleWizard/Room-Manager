from Config import *
            


###############################################
#                   COMMANDS                  #
###############################################

@bot.slash_command(name="hello", description="Says hello to the user", guild_ids=[guild_id])
async def hello(ctx):
    await ctx.respond(f"Hello {ctx.author.name}!", ephemeral=True)
    
@bot.slash_command(name="roll", description="Rolls a dice", guild_ids=[guild_id])
async def roll(ctx, sides: discord.Option(discord.SlashCommandOptionType.integer, required=True, description="how many sides the dice has"), dice: discord.Option(discord.SlashCommandOptionType.integer, required=False, description="how many dice to roll")):
    
    if dice is None or dice == 0:
        await ctx.respond(f"You rolled a {random.randint(1, sides)}")
    elif dice > 0:
        dice_list = []
        for _ in range(dice):
            random_number = random.randint(1, sides)
            dice_list.append(random_number)
        await ctx.respond(f"You rolled a {dice}d{sides} and got {sum(dice_list)}")
            
        
@bot.slash_command(name="spoiler", description="Sends a spoiler message", guild_ids=[guild_id])
async def spoiler(ctx, message: discord.Option(discord.SlashCommandOptionType.string, required=True, description="the message to send")):
    await ctx.respond(f"||{message}||")

@bot.slash_command(name="ping", description="Pings the bot.", guild_ids=[guild_id])
async def ping(ctx):
    await ctx.respond(f"Pong! {int(bot.latency * 1000)}ms", ephemeral=True)

@bot.slash_command(name="help", description="Shows the help menu", guild_ids=[guild_id])
async def help(ctx):
    embed = discord.Embed(title="Help", description="This is the help menu for the bot.", color=0x00ff00)
    embed.add_field(name="Commands", value="This is the commands section of the help menu. Here you can find all the commands for the bot.", inline=False)
    embed.add_field(name="Moderation", value="This is the moderation section of the help menu. Here you can find all the moderation commands for the bot.", inline=False)
    embed.add_field(name="Config", value="This is the config section of the help menu. Here you can find all the config commands for the bot.", inline=False)
    embed.set_footer(text="If you need more help, join the support server: https://discord.gg/")
    view = HelpMenu()
    message = await ctx.respond(embed=embed, view=view)
    view.message = message

@bot.slash_command(name="config_help", description="Change the bot settings", guild_ids=[guild_id])
async def settings(ctx):
    user_perms = ctx.author.guild_permissions
    if not user_perms.manage_guild:
        await ctx.respond("You do not have the required permissions to use this command.", ephemeral=True)
        return
    else:
        embed = discord.Embed(
            title="Config Helper", description="This helper has everything you need to change the bot settings.", color=0x00ff00)
        embed.add_field(
            name="Moderation", value="Inside of Moderation, you can find out how to edit these settings:\n    - Ban Settings\n    - Kick Settings\n    - Mute Settings", inline=False)
        embed.add_field(name="Other Settings",
                        value="Inside of Other Settings, you can find out how to edit these settings:\n    - Welcome Settings", inline=False)
        embed.set_footer(
            text="If you need more help, join the support server: https://discord.gg/")
        view = BotSettingHelp()
        message = await ctx.respond(embed=embed, view=view)
        view.message = message


@bot.slash_command(name="clean", description="Gets rid of all bots messages in specified range", guild_ids=[guild_id])
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


@bot.slash_command(name="embed_message", description="Creates an embeded message", guild_ids=[guild_id])
async def embed_message(ctx, title: discord.Option(discord.SlashCommandOptionType.string, required=True, description="Title of the embed"),
                        author_name: discord.Option(discord.SlashCommandOptionType.string, required=False, description="Author of the embed"),
                        author_icon: discord.Option(discord.SlashCommandOptionType.string, required=False, description="Icon url for the author"),
                        description: discord.Option(discord.SlashCommandOptionType.string, required=False, description="Description of the embed"),
                        field_amount: discord.Option(discord.SlashCommandOptionType.integer, required=False, description="Amount of fields to send"),
                        time_stamp: discord.Option(discord.SlashCommandOptionType.string, required=False, description="Yes or no question"),
                        footer: discord.Option(discord.SlashCommandOptionType.string, required=False, description="Footer of the embed"),
                        color: discord.Option(
                            discord.SlashCommandOptionType.string, required=False, description="Color of the embed")
                        ):

    fields = None
    if field_amount is not None:
        for i in range(field_amount):
            fields = 1 + i

    if field_amount is None:
        embed = discord.Embed()

        if author_name is not None or author_icon is not None:
            embed.set_author(name=author_name or "", icon_url=author_icon)
        else:
            embed.set_author(name=ctx.author.name,
                             icon_url=ctx.author.avatar.url)

        if author_name is not None or author_icon is not None:
            embed.set_author(name=author_name or "", icon_url=author_icon)
        else:
            embed.set_author(name=ctx.author.name,
                             icon_url=ctx.author.avatar.url)

        if author_name == None:
            embed.set_author(name=ctx.author, icon_url=ctx.author.avatar.url)
        elif author_name != None:
            embed.set_author(name=author_name)

        embed.set_footer(text=footer or "Powered by Room Manager")

        if title is not None:
            embed.title = title

        if description is not None:
            embed.description = description

        if time_stamp and time_stamp.lower() in ["y", "yes"]:
            embed.timestamp = datetime.now()
        elif time_stamp and time_stamp.lower() in ["n", "no"] or None:
            embed.timestamp = None

    if field_amount == 0:
        await ctx.respond(embed=embed)
    elif field_amount and field_amount >= 1:
        modal = EmbedModal(field_amount=field_amount)
        message = await ctx.send_modal(modal)
        fields = await modal.run()


###############################################
#                   GUIs                      #
###############################################

# class EmbedModal(discord.ui.modal):


class HelpMenu(discord.ui.View):
    def __init__(self, message=None):
        super().__init__()
        self.message = message
    @discord.ui.button(label="Moderation", style=discord.ButtonStyle.blurple)
    async def modderation_tab(self, button, interaction):
        embed = discord.Embed(title="Moderation Settings")
        embed.add_field(name="Ban Settings", value="test")
        view = HelpMenu()
        
        
        
        await interaction.response.send_message(embed=embed, view=vie)
    @discord.ui.button(label="Commands", style=discord.ButtonStyle.blurple)
    async def commands_tab(self, button, interaction):
        embed = discord.Embed(title="Commands")
        embed.add_field(name="Ban", value="test")
        view = HelpMenu()
        
        
        await interaction.response.send_message(embed=embed, view=view)
    @discord.ui.button(label="Config", style=discord.ButtonStyle.blurple)
    async def config_tab(self, button, interaction):
        embed.add_field(name="Ban", value="test")        
        view = HelpMenu()


        await interaction.response.send_message(embed=embed, view=view)
    


class WelcomeSettingsModal(discord.ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.add_item(discord.ui.InputText(
            label="message", style=discord.InputTextStyle.long))

    async def callback(self, interaction: discord.Interaction):
        embed = discord.Embed(title="test")
        embed.add_field(name="Message:", value=self.children[0].value)
        await interaction.response.send_message(embed=[embed])


class BotSettingHelp(discord.ui.View):
    def __init__(self, message=None):
        super().__init__()
        self.message = message

    @discord.ui.button(label="Moderation", custom_id="moderation_settings", style=discord.ButtonStyle.primary)
    async def moderation_button(self, button, interaction):
        embed = discord.Embed(title="Moderation Settings")
        moderation_view = ModerationSettingsView()
        await interaction.response.edit_message(embed=embed, view=moderation_view)

    @discord.ui.button(label="Other Settings", custom_id="other_settings", style=discord.ButtonStyle.primary)
    async def other_button(self, button, interaction):
        embed = discord.Embed(title="Other Settings")
        settings_view = OtherSettings()
        await interaction.response.edit_message(embed=embed, view=settings_view)

    @discord.ui.button(label="Exit", custom_id="exit", style=discord.ButtonStyle.primary)
    async def exit_button(self, button, interaction):
        await interaction.message.delete()
        await interaction.response.edit_message(embeds=[])


class ModerationSettingsView(discord.ui.View):
    def __init__(self, message=None):
        super().__init__()
        self.message = message

    @discord.ui.button(label="Ban Settings", custom_id="ban_settings", style=discord.ButtonStyle.primary)
    async def ban_button(self, button, interaction):
        # Handle the ban button click here
        embed = discord.Embed(title="Ban Settings")
        await interaction.response.edit_message(embed=embed)

    @discord.ui.button(label="Kick Settings", custom_id="kick_settings", style=discord.ButtonStyle.primary)
    async def kick_button(self, button, interaction):
        # Handle the kick button click here
        embed = discord.Embed(title="Kick Settings")
        await interaction.response.edit_message(embed=embed)

    @discord.ui.button(label="Profanity Filter Settings", custom_id="profanty_settings", style=discord.ButtonStyle.primary)
    async def profanity_button(self, button, interaction):
        # Handle the kick button click here
        embed = discord.Embed(title="Profanity Filter Settings")
        await interaction.response.edit_message(embed=embed)

    @discord.ui.button(label="back", custom_id="back", style=discord.ButtonStyle.primary)
    async def back_button(self, button, interaction):
        embed = discord.Embed(
            title="Config Helper", description="This helper has everything you need to change the bot settings.", color=0x00ff00)
        embed.add_field(
            name="Moderation", value="Inside of Moderation, you can find out how to edit these settings:\n    - Ban Settings\n    - Kick Settings\n    - Mute Settings", inline=False)
        embed.add_field(name="Other Settings",
                        value="Inside of Other Settings, you can find out how to edit these settings:\n    - Welcome Settings", inline=False)
        embed.set_footer(
            text="If you need more help, join the support server: https://discord.gg/")
        view = BotSettingHelp()
        await interaction.response.edit_message(embed=embed, view=view)


class OtherSettings(discord.ui.View):
    def __init__(self, message=None):
        super().__init__()
        self.message = message

    @discord.ui.button(label="Language", custom_id="Language_settings", style=discord.ButtonStyle.primary)
    async def language_button(self, button, interaction):
        # Handle the welcome button click here
        embed = discord.Embed(title="Language Settings", )
        view = LanguageSettings()
        await interaction.response.edit_message(embed=embed, view=view)

    @discord.ui.button(label="Welcome Settings", custom_id="welcome_settings", style=discord.ButtonStyle.primary)
    async def welcome_button(self, button, interaction):
        # Handle the welcome button click here
        embed = discord.Embed(title="Welcome Settings")
        view = WelcomeSettings()
        await interaction.response.edit_message(embed=embed, view=view)

    @discord.ui.button(label="back", custom_id="back", style=discord.ButtonStyle.primary)
    async def back_button(self, button, interaction):
        embed = discord.Embed(
            title="Config Helper", description="This helper has everything you need to change the bot settings.", color=0x00ff00)
        embed.add_field(
            name="Moderation", value="Inside of Moderation, you can find out how to edit these settings:\n    - Ban Settings\n    - Kick Settings\n    - Mute Settings", inline=False)
        embed.add_field(name="Other Settings",
                        value="Inside of Other Settings, you can find out how to edit these settings:\n    - Welcome Settings", inline=False)
        embed.set_footer(
            text="If you need more help, join the support server: https://discord.gg/")

        view = BotSettingHelp()
        await interaction.response.edit_message(embed=embed, view=view)


class WelcomeSettings(discord.ui.View):
    def __init__(self, message=None):
        super().__init__()
        self.message = message

    @discord.ui.button(label="Welcome Message", custom_id="welcome_message", style=discord.ButtonStyle.primary)
    async def welcome_button(self, button, interaction):
        await interaction.response.send_modal(WelcomeSettingsModal(title="Modal via Button"))
        await interaction.response.send_modal(modal=WelcomeSettingsModal())


class LanguageSettings(discord.ui.View):
    def __init__(self, message=None):
        super().__init__()
        self.message = message

        # create the dropdown menu
        self.language_select = discord.ui.Select(
            placeholder="Select a language",
            options=[
                discord.SelectOption(label="English", value="en"),
                discord.SelectOption(label="Spanish", value="es"),
                discord.SelectOption(label="French", value="fr")
            ],
            custom_id="language_select"
        )

        # add the dropdown menu to the view
        self.add_item(self.language_select)

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
    if config["trafic"]["enabled"] == True:
        if config["trafic"]["welcome_type"] == "channel":
            if config["trafic"]["channel"] == None:
                if config["moderation_channel"] == None:
                    await member.guild.owner.send("You have not set a Mod Channel for the server!")
                    return
                await bot.get_channel(config["moderation_channel"]).send("You have not set a user trafic Channel for the server! (join/leave notifs)")
                return
            else:
                await member.guild.get_channel(config["trafic"]["channel"]).send(config["trafic"]["welcome_message"].replace("{member}", member.mention))
        elif config["trafic"]["welcome_type"] == "dm":
            await member.send(f"Welcome to the server, {member.mention}! Please read the rules and enjoy your stay!")



    print("Starting bot...")
    open("Logs/session_logs.txt", "w").close()
    open("Logs/session_logs.txt",
         "a").write(f"[{formatted_time}] Starting bot...\n")



@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="Mr.Wizard#5853"))


@bot.event
async def on_member_ban(guild, user):

    if config["moderation_channel"] == None:
        await guild.owner.send("You have not set a Mod Channel for the server!")
        return
    await bot.get_channel(config["moderation_channel"]).send(f"{user} has been banned from the server.")


@bot.event
async def on_member_unban(guild, user):
    if config["moderation_channel"] == None:
        await guild.owner.send("You have not set a Mod Channel for the server!")
        return
    await bot.get_channel(config["moderation_channel"]).send(f"{user} has been unbanned from the server.")


print(f"Using: Pycord {discord.__version__}")
bot.run(bot_token)
