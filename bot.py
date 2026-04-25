import discord
from discord import app_commands
from discord.ext import commands
import os

# TWOJE IMPORTY
from welcome import handle_welcome
from roles import RoleView
from giveaway import GiveawayView, parse_time, run_giveaway  # DODANE

# --- KONFIGURACJA ---
WELCOME_CHANNEL_ID = 1457756805173084309
MAKS_BLUE = 0x3498db
# ... reszta Twoich ID ról ...

intents = discord.Intents.all()

class MaksBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        self.add_view(RoleView(1469838172916551775, 1457769670060019767))
        # Dodajemy widok giveaway do setup_hook, żeby przyciski działały po restarcie
        self.add_view(GiveawayView()) 
        await self.tree.sync()

bot = MaksBot()

# --- KOMENDA GIVEAWAY ---
@bot.tree.command(name="givcreate", description="Tworzy nowy giveaway")
@app_commands.describe(
    tytul="Tytuł konkursu",
    opis="Opis wymagań i nagrody",
    czas="Czas (np. 10m, 1h, 1d)",
    zwyciezcy="Liczba wygranych",
    kolor="Kolor paska w HEX"
)
async def givcreate(
    interaction: discord.Interaction, 
    tytul: str, 
    opis: str, 
    czas: str, 
    zwyciezcy: int, 
    kolor: str = "#3498db"
):
    # Sprawdzanie uprawnień (opcjonalnie)
    if not interaction.user.guild_permissions.administrator:
        return await interaction.response.send_message("Nie masz uprawnień!", ephemeral=True)

    sekundy = parse_time(czas)
    if not sekundy:
        return await interaction.response.send_message("Zły format czasu (np. 10m, 1h)!", ephemeral=True)

    await run_giveaway(interaction, tytul, opis, sekundy, zwyciezcy, kolor)

@bot.event
async def on_member_join(member):
    await handle_welcome(member, WELCOME_CHANNEL_ID, MAKS_BLUE)

# Twój stary kod komendy panel i bot.run...
token = os.getenv('DISCORD_TOKEN')
bot.run(token)
