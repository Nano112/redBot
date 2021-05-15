
from discord.ext import commands
import os
from dotenv import load_dotenv
import json

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

with open('config.json') as file:
      config = json.load(file)


red_bot = commands.Bot(command_prefix=config["command_prefix"])

red_bot.load_extension("cogs.maincog")

red_bot.run(token)