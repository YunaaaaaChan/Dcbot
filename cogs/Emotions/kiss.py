import requests
from discord.ext import commands
from discord.commands import slash_command
from discord import Embed
import json


class Kiss(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(description="Send a hug to a user")
    async def kiss(self, ctx, user: commands.UserConverter):
        # Fetch a random hug image from the nekos.best API
        url = "https://nekos.best/api/v2/kiss"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            hug_image_url = data['results'][0]['url']

            # Create an embed for the hug
            embed = Embed(
                title="Kuss!",
                description=f"{ctx.author.mention} Küsst! {user.mention}! 🤗",
                color=0xFF69B4
            )
            embed.set_image(url=hug_image_url)

            await ctx.respond(embed=embed)
        else:
            await ctx.respond("Konnte keine verbindung zur nekos API aufbauen!, versuche es später erneut!.")


def setup(bot):
    bot.add_cog(Kiss(bot))