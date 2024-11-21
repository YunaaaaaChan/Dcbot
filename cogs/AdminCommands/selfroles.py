import discord
from discord.ext import commands
from discord.commands import slash_command
import os

class GeschlechtView(discord.ui.View):
    @discord.ui.select(
        placeholder="Wähle dein Geschlecht",
        options=[
            discord.SelectOption(label="Männlich", value="male"),
            discord.SelectOption(label="Weiblich", value="female"),
            discord.SelectOption(label="Divers", value="diverse"),
        ]
    )
    async def select_callback(self, select, interaction: discord.Interaction):
        await interaction.response.send_message(f"Du hast {select.values[0]} gewählt!", ephemeral=True)

class ZweitesSelectMenu(discord.ui.View):
    @discord.ui.select(
        placeholder="Wähle eine weitere Option",
        options=[
            discord.SelectOption(label="Option 1", value="option1"),
            discord.SelectOption(label="Option 2", value="option2"),
            discord.SelectOption(label="Option 3", value="option3"),
        ]
    )
    async def select_callback(self, select, interaction: discord.Interaction):
        await interaction.response.send_message(f"Du hast {select.values[0]} gewählt!", ephemeral=True)

class SelfRoles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("SelfRoles Cog ist bereit.")

    @slash_command()
    @commands.has_permissions(administrator=True)  # Nur Administratoren können diesen Befehl ausführen
    async def send_roles(self, ctx):
        channel_id = os.environ.get('selfroles')  # Ersetze dies mit der tatsächlichen Kanal-ID
        channel = self.bot.get_channel(int(channel_id))

        if channel is None:
            await ctx.respond("Kanal nicht gefunden. Stelle sicher, dass die Kanal-ID korrekt ist.", ephemeral=True)
            return

        # Sende die GeschlechtView
        embed = discord.Embed(
            title="Wähle dein Geschlecht aus:",
            description="Bitte wähle eine der folgenden Optionen aus:",
            color=discord.Color.blue()
        )
        embed.set_image(url="https://cdn.discordapp.com/attachments/1302724998510936145/1307498115116568646/test.png?ex=673a8602&is=67393482&hm=264b856cf0389575858ac92993bdfbd744a0ca5c0daa41fba0070f2c811f453c&")  # Füge hier die URL deines Bildes ein
        embed.set_footer(text="Reagiere mit der Auswahl unten.")
        try:
            await channel.send(embed=embed, view=GeschlechtView())
        except Exception as e:
            print(f"Fehler beim Senden der GeschlechtView: {e}")

        # Sende die zweite Auswahl
        embed_zweite_auswahl = discord.Embed(
            title="Wähle eine weitere Option:",
            description="Bitte wähle eine der folgenden Optionen aus:",
            color=discord.Color.green()
        )
        embed_zweite_auswahl.set_image(url="https://cdn.discordapp.com/attachments/1302724998510936145/1307498115116568646/test.png?ex=673a8602&is=67393482&hm=264b856cf0389575858ac92993bdfbd744a0ca5c0daa41fba0070f2c811f453c&")  # Füge hier die URL deines zweiten Bildes ein
        embed_zweite_auswahl.set_footer(text="Reagiere mit der Auswahl unten.")
        try:
            await channel.send(embed=embed_zweite_auswahl, view=ZweitesSelectMenu())
        except Exception as e:
            print(f"Fehler beim Senden der zweiten SelectView: {e}")

class GeschlechtView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    options = [
        discord.SelectOption(label="Männlich", description="Männlich"),
        discord.SelectOption(label="Weiblich", description="Weiblich"),
        discord.SelectOption(label="Divers", description="Divers"),
    ]

    @discord.ui.select(
        min_values=1,
        max_values=1,
        placeholder="Triff eine Auswahl!",
        options=options,
        custom_id="geschlecht_select"
    )
    async def select_callback(self, select, interaction):
        roles = {
            "Männlich": int(os.environ.get('Maennlich')),
            "Weiblich": int(os.environ.get('Weiblich')),
            "Divers": int(os.environ.get('Divers')),
        }

        member = interaction.user
        for role in member.roles:
            if role.id in roles.values():
                await member.remove_roles(role)

        selected_role_id = roles.get(select.values[0])
        if selected_role_id:
            role_to_add = discord.utils.get(member.guild.roles, id=selected_role_id)
            if role_to_add:
                await member.add_roles(role_to_add)
                await interaction.response.send_message(f"Du hast die Rolle '{role_to_add.name}' zugewiesen bekommen.")
            else:
                await interaction.response.send_message("Die Rolle konnte nicht gefunden werden.")
        else:
            await interaction.response.send_message("Keine gültige Rolle ausgewählt.")

class ZweitesSelectMenu(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    second_options = [
        discord.SelectOption(label="Option 1", description="Beschreibung für Option 1"),
        discord.SelectOption(label="Option 2", description="Beschreibung für Option 2"),
        discord.SelectOption(label="Option 3", description="Beschreibung für Option 3"),
    ]

    @discord.ui.select(
        min_values=1,
        max_values=1,
        placeholder="Wähle eine weitere Option!",
        options=second_options,
        custom_id="zweites_select"
    )
    async def second_select_callback(self, select, interaction):
        second_roles = {
            "Option 1": 456789012345678901,  # Ersetze dies mit der tatsächlichen Rollen-ID für Option 1
            "Option 2": 567890123456789012,  # Ersetze dies mit der tatsächlichen Rollen-ID für Option 2
            "Option 3": 678901234567890123,  # Ersetze dies mit der tatsächlichen Rollen-ID für Option 3
        }

        member = interaction.user
        for role in member.roles:
            if role.id in second_roles.values():
                await member.remove_roles(role)

        selected_role_id = second_roles.get(select.values[0])
        if selected_role_id:
            role_to_add = discord.utils.get(member.guild.roles, id=selected_role_id)
            if role_to_add:
                await member.add_roles(role_to_add)
                await interaction.response.send_message(f"Du hast die Rolle '{role_to_add.name}' zugewiesen bekommen.")
            else:
                await interaction.response.send_message("Die Rolle konnte nicht gefunden werden.")
        else:
            await interaction.response.send_message("Keine gültige Rolle ausgewählt.")

# Setup-Funktion zum Hinzufügen des Cogs
def setup(bot):
    bot.add_cog(SelfRoles(bot))