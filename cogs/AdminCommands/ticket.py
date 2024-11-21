from datetime import datetime

import discord
from discord.ext import commands
from discord.commands import slash_command
import asyncio

class Ticket(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ticket_channel_count = 0

    @slash_command()
    async def support(self, ctx):
        modal = TicketModal(self.bot)
        await ctx.send_modal(modal)

    @slash_command()
    @commands.has_permissions(administrator=True)
    async def create_ticket(self, ctx):
        embed = discord.Embed(
            title="Ticket Support",
            description="",
            colour=0x00f55e,
            timestamp=datetime.now()
        )
        embed.add_field(
            name="🕛 Support zeiten 🕛",
            value="Unsere Support Zeiten sind 24/7\nWir Antworten innerhalb von 24 Stunden",
            inline=True
        )
        embed.add_field(
            name="❌ Passwörter teilen ❌",
            value="Bitte Teile uns niemals dein Passwort mit, kein Teammitglied würde nach dein passwort fragen.",
            inline=False
        )
        embed.add_field(
            name="✅ Fragen und Hilfe ✅",
            value="Unser Support steht dir bei fragen, Partnerschaften und Problemen Zur seite.",
            inline=True
        )
        embed.add_field(
            name="👍 Benutzer Melden 👍",
            value="Bitte meldet Spam bots, Benutzer die gegen regel verstoßen, und Teammitglieder die gegen regeln Verstoßen!\nDas würde das Benutzer umfeld, von anderen Benutzern Sehr fördern!",
            inline=False
        )
        embed.set_image(
            url="https://cdn.discordapp.com/attachments/1302724998510936145/1307701618485100635/photo-output.png?ex=673b4389&is=6739f209&hm=5bb089c5203d57d53b93e84d7c47fac04d59dcd3f37a57abcfbd5f9a481d3710&"
        )
        embed.set_thumbnail(
            url="https://media.discordapp.net/attachments/1302724998510936145/1302725204035895369/logosimple.png?ex=673af524&is=6739a3a4&hm=400de174d144e306884912fc66240b93a7cce9eb7963b67a182bd86a4aca993a&=&format=webp&quality=lossless&width=235&height=240"
        )
        embed.set_footer(
            text="Spectra-Studio.cc",
            icon_url="https://media.discordapp.net/attachments/1302724998510936145/1302725204035895369/logosimple.png?ex=673af524&is=6739a3a4&hm=400de174d144e306884912fc66240b93a7cce9eb7963b67a182bd86a4aca993a&=&format=webp&quality=lossless&width=235&height=240"
        )
        await ctx.respond(embed=embed, view=ButtonView(self.bot))

def setup(bot):
    bot.add_cog(Ticket(bot))

class TicketModal(discord.ui.Modal):
    def __init__(self, bot, **kwargs):
        super().__init__(title="Ticket System", **kwargs)
        self.bot = bot
        self.add_item(discord.ui.InputText(
            label="Ticket Grund",
            placeholder="Beschreibe Hier dein Problem"
        ))
        self.add_item(discord.ui.InputText(
            label="Beschreibung",
            placeholder="Beschreibe hier dein Problem",
            style=discord.InputTextStyle.long
        ))

    async def callback(self, interaction):
        guild = interaction.guild

        category_id = 1307536258716930110
        category = guild.get_channel(category_id)

        if category is None or not isinstance(category, discord.CategoryChannel):
            await interaction.response.send_message("Die angegebene Kategorie existiert nicht.", ephemeral=True)
            return

        for channel in category.channels:
            if isinstance(channel, discord.TextChannel) and channel.name.startswith("ticket-"):
                if interaction.user in channel.members:
                    await interaction.response.send_message(ephemeral=True,
                                                            embed = discord.Embed (
                                                                    title="Ticket System",
                                                                    description=f"Error: Du hast Bereits ein ticket geöffnet.",
                                                                    colour=0xf50000,
                                                                    timestamp=datetime.now()
                                                                )
                                                            )
                    return

        ticket_number = self.bot.get_cog('Ticket').ticket_channel_count + 1
        ticket_name = f"ticket-{ticket_number}"

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            interaction.user: discord.PermissionOverwrite(read_messages=True)
        }

        team_role_id = 1307539911221575781
        team_role = guild.get_role(team_role_id)
        if team_role:
            overwrites[team_role] = discord.PermissionOverwrite(read_messages=True)
        channel = await guild.create_text_channel(ticket_name, category=category, overwrites=overwrites)

        embed = discord.Embed(
            title="Ticket System",
            description=f"Herzlich Willkommen {interaction.user.mention} in unseren Ticket System.\nWir sind gleich für sie da.\nUnser Support arbeitet 24/7 wir Antworten meist innerhalb von 24 Stunden.",
            colour=0x00f55e,
            timestamp=datetime.now()
        )
        embed.add_field(
            name="Ticket Grund:",
            value=self.children[0].value,
            inline=True
        )
        embed.add_field(
            name="Ticket Beschreibung:",
            value=self.children[1].value,
            inline=True
        )
        embed.set_image(
            url="https://cdn.discordapp.com/attachments/1302724998510936145/1307701618485100635/photo-output.png?ex=673b4389&is=6739f209&hm=5bb089c5203d57d53b93e84d7c47fac04d59dcd3f37a57abcfbd5f9a481d3710&"
        )

        embed.set_thumbnail(
            url="https://media.discordapp.net/attachments/1302724998510936145/1302725204035895369/logosimple.png?ex=673af524&is=6739a3a4&hm=400de174d144e306884912fc66240b93a7cce9eb7963b67a182bd86a4aca993a&=&format=webp&quality=lossless&width=235&height=240"
        )

        embed.set_footer(
            text="Spectra-Studio.cc",
            icon_url="https://media.discordapp.net/attachments/1302724998510936145/1302725204035895369/logosimple.png?ex=673af524&is=6739a3a4&hm=400de174d144e306884912fc66240b93a7cce9eb7963b67a182bd86a4aca993a&=&format=webp&quality=lossless&width=235&height=240"
        )
        await channel.send(embed=embed)

        await channel.send(view=SupporterButtons(self.bot, channel))

        self.bot.get_cog('Ticket').ticket_channel_count = ticket_number

        await interaction.response.send_message(ephemeral=True,
            embed = discord.Embed (
                title="Ticket System",
                description=f"{interaction.user.mention} Du hast ein ticket geöffnet!",
                colour=0x00f53d,
                timestamp=datetime.now())
        )

class SupporterButtons(discord.ui.View):
    def __init__(self, bot, channel):
        super().__init__()
        self.bot = bot
        self.channel = channel

    @discord.ui.button(label="Ticket übernehmen", style=discord.ButtonStyle.success)
    async def take_ticket(self, button: discord.ui.Button, interaction: discord.Interaction):
        team_role_id = 1307539911221575781
        team_role = interaction.guild.get_role(team_role_id)
        if team_role in interaction.user.roles:
            embed = discord.Embed (
                title="Ticket System",
                description=f"Hey {interaction.user.mention}, hat das Ticket übernommen",
                colour = 0x00f55e,
                timestamp=datetime.now()
            )
            embed.set_image(url="https://cdn.discordapp.com/attachments/1302724998510936145/1307701618485100635/photo-output.png?ex=673b4389&is=6739f209&hm=5bb089c5203d57d53b93e84d7c47fac04d59dcd3f37a57abcfbd5f9a481d3710&")

            embed.set_thumbnail(url="https://media.discordapp.net/attachments/1302724998510936145/1302725204035895369/logosimple.png?ex=673af524&is=6739a3a4&hm=400de174d144e306884912fc66240b93a7cce9eb7963b67a182bd86a4aca993a&=&format=webp&quality=lossless&width=235&height=240")

            embed.set_footer(text="Spectra-Studio.cc",
                             icon_url="https://media.discordapp.net/attachments/1302724998510936145/1302725204035895369/logosimple.png?ex=673af524&is=6739a3a4&hm=400de174d144e306884912fc66240b93a7cce9eb7963b67a182bd86a4aca993a&=&format=webp&quality=lossless&width=235&height=240"
                             )

            await  interaction.response.send_message(embed=embed)
        else:
            embed = discord.Embed (
                title="Ticket System",
                description=f"Error: Du hast nicht die Berechtigung, dieses Ticket zu übernehmen.",
                colour=0xf50000,
                timestamp=datetime.now()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)

    @discord.ui.button(label="Ticket schließen", style=discord.ButtonStyle.danger)
    async def close_ticket(self, button: discord.ui.Button, interaction: discord.Interaction):
        modal = CloseTicketModal(self.bot, self.channel)
        await interaction.response.send_modal(modal)


class CloseTicketModal(discord.ui.Modal):
    def __init__(self, bot, channel, **kwargs):
        super().__init__(title="Ticket schließen", **kwargs)
        self.bot = bot
        self.channel = channel
        self.add_item(discord.ui.InputText(
            label="Grund der Schließung",
            placeholder="Gib den Grund für die Schließung des Tickets an."
        ))

    async def callback(self, interaction):
        reason = self.children[0].value
        log_channel_id = 1307541524783038534
        log_channel = interaction.guild.get_channel(log_channel_id)

        if log_channel is None:
            print("Log-Kanal nicht gefunden.")
            await interaction.response.send_message("Der Log-Kanal konnte nicht gefunden werden.", ephemeral=True)
            return

        embed = discord.Embed(
            title="Ticket geschlossen",
            description=f"Das Ticket wurde geschlossen.",
            color=discord.Color.red()
        )
        embed.add_field(name="Grund", value=reason, inline=False)
        embed.add_field(name="Geschlossen von", value=interaction.user.mention, inline=False)
        embed.add_field(name="Ticket Name", value=self.channel.name, inline=False)
        embed.add_field(name="Ticket Geschlossen am ", value=datetime.now(), inline=False)

        await interaction.response.send_message(
            ephemeral=True,
            embed=discord.Embed(
                title="Ticket geschlossen",
                description=f"Du hast das Ticket geschlossen.\n\n Das ticket schließt in 5 sekunden.",
                color=discord.Color.red()
                )
        )

        if self.channel:
            try:
                await self.channel.send(
                    embed = discord.Embed(
                        title="Ticket geschlossen",
                        description=f"Das Ticket wurde geschlossen.\n\n Das ticket schließt in 5 sekunden.\n\nGeschlossen von {interaction.user.mention}.",
                        color=discord.Color.red()
                    )
                )
                await log_channel.send(embed=embed)

                await asyncio.sleep(5)

                await self.channel.delete()
                print(f"Ticket-Kanal {self.channel.name} wurde erfolgreich geschlossen.")
            except discord.Forbidden:
                print("Der Bot hat keine Berechtigung, den Kanal zu löschen.")
            except discord.NotFound:
                print("Der Kanal wurde nicht gefunden.")
            except Exception as e:
                print(f"Ein Fehler ist aufgetreten beim Löschen des Kanals: {e}")

class ButtonView(discord.ui.View):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot

    @discord.ui.button(label="Öffne ein Ticket")
    async def button_callback(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.response.send_modal(TicketModal(self.bot))