import discord
from discord import app_commands
from discord.ext import commands
import os

# Importy Twoich plików:
from welcome import handle_welcome
from roles import RoleView
# Importy z nowego pliku giveaway:
from giveaway import GiveawayView, parse_time, run_giveaway_logic

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
        # Rejestrujemy widoki z innych plików
        self.add_view(RoleView(ROLE_TIKTOK_ID, ROLE_PROMOCJE_ID))
        
        # Rejestrujemy widok Giveawaya, aby przycisk działał nawet po restarcie bota
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

# --- KOMENDA GIVEAWAY ---
@bot.tree.command(name="givcreate", description="Tworzy nowy giveaway")
@app_commands.describe(
    tytul="Tytuł konkursu",
    opis="Opis wymagań (np. link, co trzeba zrobić)",
    czas="Czas trwania (format np. 10m, 1h, 2d)",
    zwyciezcy="Ilu będzie zwycięzców?",
    kolor="Kolor paska bocznego w HEX (np. #5865F2) - opcjonalnie"
)
async def givcreate(
    interaction: discord.Interaction, 
    tytul: str, 
    opis: str, 
    czas: str, 
    zwyciezcy: int, 
    kolor: str = "#5865F2"
):
    # Weryfikacja uprawnień - nie każdy ma prawo robić giveaway
    if not interaction.user.guild_permissions.administrator:
        return await interaction.response.send_message("Nie masz uprawnień administratora, aby tego użyć!", ephemeral=True)

    sekundy = parse_time(czas)
    if not sekundy:
        return await interaction.response.send_message("Podałeś błędny format czasu! Użyj s (sekundy), m (minuty), h (godziny) lub d (dni). Np. `30m`", ephemeral=True)

    # Przekierowujemy wywołanie do odseparowanego pliku giveaway.py
    await run_giveaway_logic(interaction, tytul, opis, sekundy, zwyciezcy, kolor, MAKS_BLUE)

token = os.getenv('DISCORD_TOKEN')
bot.run(token)
