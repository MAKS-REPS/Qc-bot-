import discord
from discord.ext import commands
import os

# Konfiguracja intencji (potrzebne do wykrywania nowych osób)
intents = discord.Intents.default()
intents.members = True  # KLUCZOWE: Musisz to włączyć w Discord Developer Portal!

bot = commands.Bot(command_prefix="!", intents=intents)

# ID kanału, na którym bot ma wysyłać powitania
WELCOME_CHANNEL_ID = 1457756805173084309

@bot.event
async def on_ready():
    print(f'Zalogowano jako {bot.user.name}')

@bot.event
async def on_member_join(member):
    channel = bot.get_channel(WELCOME_CHANNEL_ID)
    if channel:
        # Pobieranie liczby osób na serwerze
        member_count = member.guild.member_count
        
        # Tworzenie Embedu (niebieski pasek)
        embed = discord.Embed(
            title="👋 Maks Reps × WITAMY",
            description="",
            color=0x3498db  # Kolor niebieski
        )
        
        # Treść powitania
        embed.add_field(
            name="", 
            value=f"• 👶 × Witaj {member.mention} na **Maks Reps**\n"
                  f"• 👥 × Jesteś **{member_count} osobą** na naszym serwerze!\n"
                  f"• ✨ × Liczymy, że zostaniesz z nami na dłużej!",
            inline=False
        )
        
        # Ikonka osoby (Avatar) po prawej stronie
        embed.set_thumbnail(url=member.display_avatar.url)
        
        # Wysyłanie wiadomości
        await channel.send(f"{member.mention}", embed=embed)

# Railway używa zmiennych środowiskowych dla bezpieczeństwa
token = os.getenv('DISCORD_TOKEN')
if token:
    bot.run(token)
else:
    print("Błąd: Nie znaleziono tokenu DISCORD_TOKEN w zmiennych środowiskowych!")
