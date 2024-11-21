import random

import discord
from discord.ext import tasks
import os
from dotenv import load_dotenv

import ezcord

intents = discord.Intents.default()

bot = ezcord.Bot(
    intents=intents,
    debug_guilds=[1302663367827263510],
    ready_event=ezcord.ReadyEvent.logs
)


members = 0
for guild in bot.guilds:
    members += guild.member_count

statusmessages = [
    "Made with ❤ by Yuikaaa, Yunaaa",
    "Website: https://spectra-studio.cc/",
    "discord: https://dc.spectra-studio.cc/",
    "Twitter: Spectra-Studio",
    "Instagram: Spectra-Studio",
    "Pinterest: Spectra-Studio",
    "TikTok: Spectra-Studio",
    "YouTube: Spectra-Studio",
    "Support mail: Change@Change.cc",
    f"Mitglieder Online: {members}"
]

@tasks.loop(seconds=10)
async def randomstatus():
    status = random.choice(statusmessages)
    await bot.change_presence(status=discord.Status.do_not_disturb, activity=discord.Game(name=status))

@bot.event
async def on_ready():
    print("Logged in as a bot {0.user}".format(bot))
    randomstatus.start()

if __name__ == "__main__":
    bot.load_cogs(subdirectories=True)


load_dotenv()
bot.run(os.environ.get('TOKEN'))