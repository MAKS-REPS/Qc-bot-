import discord
from discord import app_commands
from discord.ext import commands
import os

# Importy Twoich plików:
from welcome import handle_welcome
from roles import RoleView
# NOWE: Importujemy giveaway
from giveaway import GiveawayView, parse_time, start_giveaway 

# --- KONFIGURACJA ---
WELCOME_CHANNEL_ID = 1457756805173084309
REQUIRED_ROLE_ID = 1457769309735485450 
ROLE_TIKTOK_ID = 1469838172916551775
ROLE_PROMOCJE_ID = 1457769670060019767
MAKS_BLUE = 0x3498db

intents = discord.Intents.all()

class MaksBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        # Rejestrujemy widoki ról
        self.add_view(RoleView(ROLE_TIKTOK_ID, ROLE_PROMOCJE_ID))
        # NOWE: Rejestrujemy widok giveaway, żeby przycisk działał po restarcie
        self.add_view(GiveawayView())
        await self.tree.sync()

bot = MaksBot()

@bot.event
async def on_member_join(member):
    await handle_welcome(member, WELCOME_CHANNEL_ID, MAKS_BLUE)

@bot.tree.command(name="panel", description="Wysyła wybrany panel")
async def panel(interaction: discord.Interaction, typ: str):
    # Logika sprawdzania uprawnień i wysyłania widoków...
    pass

# --- NOWA KOMENDA GIVEAWAY ---
@bot.tree.command(name="givcreate", description="Tworzy nowy giveaway")
@app_commands.describe(
    tytul="Tytuł konkursu",
    opis="Nagroda i opis",
    czas="Czas trwania (np. 10m, 1h, 1d)",
    zwyciezcy="Ilu zwycięzców",
    kolor="Kolor paska HEX (np. #ff0000)"
)
async def givcreate(interaction: discord.Interaction, tytul: str, opis: str, czas: str, zwyciezcy: int, kolor: str = "#3498db"):
    if not interaction.user.guild_permissions.administrator:
        return await interaction.response.send_message("Brak uprawnień!", ephemeral=True)

    sekundy = parse_time(czas)
    if not sekundy:
        return await interaction.response.send_message("Błędny format czasu!", ephemeral=True)

    await start_giveaway(interaction, tytul, opis, sekundy, zwyciezcy, kolor)

token = os.getenv('DISCORD_TOKEN')
bot.run(token)
