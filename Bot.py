# Pycord v2.4
import discord
import os
from dotenv import load_dotenv
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("discord")

owner_ids = [os.getenv("OWNER_ID")]
command_prefix = os.getenv("PREFIX")
activity = discord.Activity(type=discord.ActivityType.watching, name="you")
intents = discord.Intents.all()

load_dotenv("./Config/.env")

bot = discord.Bot(intents=intents, logging=logging.INFO, owner_ids=owner_ids, command_prefix=command_prefix,
                  activity=activity)


@bot.event
async def on_ready():
    logger.info(f"Logged in as {bot.user.name}#{bot.user.discriminator}")
    logger.info(f"Guilds: {len(bot.guilds)}")
    logger.info(f"Cogs: {len(bot.cogs)}")
    logger.info(f"Commands: {len(bot.commands)}")
    logger.info(f"Version: {discord.__version__}")
    logger.info(f"Invite: https://discord.com/oauth2/authorize?client_id={bot.user.id}&scope=bot&permissions=8")
    logger.info(f"Support: https://github.com/GentleWizard/Room-Manager/issues")
    logger.info(f"Github: https://github.com/GentleWizard/Room-Manager")
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="you"))
    await bot.change_presence(status=discord.Status.online)



for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        bot.load_extension(f"cogs.{filename[:-3]}")
        logger.info(f"Loaded {filename[:-3]}")

if __name__ == "__main__":
    bot.run(os.getenv("TOKEN"))
