import discord
from discord.ext import commands
from discord.commands import slash_command
from discord import Embed

class Announce(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.channel_id = 1307560129440518224
        self.role_id = 1307432290007122001

    @slash_command()
    @commands.has_permissions(administrator=True)
    async def announce(self, ctx):
        modal = discord.ui.Modal(title="Nachricht Ankündigen")

        embed_description_input = discord.ui.InputText(label="Embed Beschreibung", placeholder="Gib die Beschreibung des Embeds ein", style=discord.InputTextStyle.paragraph)
        modal.add_item(embed_description_input)

        image_url_input = discord.ui.InputText(label="Bild URL", placeholder="Gib die URL des Bildes ein")
        modal.add_item(image_url_input)

        async def modal_callback(interaction: discord.Interaction):
            embed_description = embed_description_input.value
            image_url = image_url_input.value

            embed = Embed(title="Neuigkeiten", description=embed_description)
            if image_url:
                embed.set_image(url=image_url)

            channel = self.bot.get_channel(self.channel_id)

            if channel is None:
                await interaction.response.send_message("Channel nicht gefunden!", ephemeral=True)
                return

            await channel.send(f"Hey Es gibt News <@&{self.role_id}>", embed=embed)

            await interaction.response.send_message("Nachricht erfolgreich gesendet!", ephemeral=True)

        modal.callback = modal_callback
        await ctx.send_modal(modal)

def setup(bot):
    bot.add_cog(Announce(bot))