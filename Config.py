# This code is importing necessary modules and setting up a Discord bot using the Discord API. It also
# loads environment variables using the `dotenv` module and sets up a configuration dictionary with
# various settings for the bot, such as the server ID, bot token, and moderation channel. Finally, it
# sets variables for the server ID, bot ID, and bot token for later use.
import discord
import os
import dotenv
from datetime import datetime
import random


# `bot = discord.Bot(intents=discord.Intents.all())` is creating a new instance of the `discord.Bot`
# class with all intents enabled. This will allow the bot to receive and handle all events from the
# Discord API.
bot = discord.Bot(intents=discord.Intents.all())
    
# `dotenv.load_dotenv()` is loading environment variables from a `.env` file into the current
# environment.
dotenv.load_dotenv()

# `now = datetime.now()` creates a datetime object representing the current date and time.
# `formatted_time = now.strftime("%H:%M:%S")` formats the datetime object into a string with the
# format "hour:minute:second" and assigns it to the variable `formatted_time`.
now = datetime.now()
formatted_time = now.strftime("%H:%M:%S")

config = {
    "bot_token": os.getenv("BOT_TOKEN"),
    "server_id": os.getenv("SERVER_ID"),
    "bot_id": os.getenv("BOT_ID"),
    "moderation_channel": 1065772341554053162,
    "mod_role": None,
    "trafic": {
        "enabled": True,
        "channel": None,
        "welcome_message": None,
        "Leave_message": None,
        "welcome_type": "dm",
    },
}
guild_id = config["server_id"]
bot_id = config["bot_id"]
bot_token = config["bot_token"]
