import discord
import datetime
import asyncio
import random
import re

# --- KONFIGURACJA SZANSY ---
# ID roli, która ma 2x więcej szans na wygraną
BONUS_ROLE_ID = 1497656242615746721

class GiveawayView(discord.ui.View):
    def __init__(self):
        # timeout=None sprawia, że przyciski nie przestaną działać po czasie
        super().__init__(timeout=None)
        self.entries = []

    @discord.ui.button(emoji="🎉", style=discord.ButtonStyle.blurple, custom_id="persistent_giveaway_button")
    async def join_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id in self.entries:
            return await interaction.response.send_message("Już bierzesz udział w tym losowaniu!", ephemeral=True)
        
        self.entries.append(interaction.user.id)
        await interaction.response.send_message("Pomyślnie dodano Cię do listy uczestników!", ephemeral=True)

def parse_time(time_str):
    """Konwertuje format czasu (np. 10m, 1h) na sekundy."""
    pos = {"s": 1, "m": 60, "h": 3600, "d": 86400}
    match = re.match(r"(\d+)([smhd])", time_str.lower())
    if match:
        return int(match.group(1)) * pos[match.group(2)]
    return None

async def run_giveaway_logic(interaction, tytul, opis, sekundy, zwyciezcy, kolor_hex, default_color):
    """Główna logika tworzenia i rozstrzygania konkursu."""
    
    # Przetworzenie koloru HEX
    try:
        color_val = int(kolor_hex.replace("#", ""), 16)
    except:
        color_val = default_color

    end_time = datetime.datetime.now() + datetime.timedelta(seconds=sekundy)
    timestamp = int(end_time.timestamp())

    # Tworzenie Embeda na wzór screenshota
    embed = discord.Embed(
        title=tytul,
        description=f"{opis}\n\n**Konta mają być nowe, na dowód należy wysłać ssa po założeniu (przykład poniżej) / brak spełnienia któregoś z wymagań = ponowne losowanie**",
        color=discord.Color(color_val)
    )
    
    # Dynamiczne formatowanie czasu (R = Relative, f = Full date)
    embed.add_field(name="Ends:", value=f"<t:{timestamp}:R> (<t:{timestamp}:f>)", inline=False)
    embed.add_field(name="Hosted by:", value=interaction.user.mention, inline=True)
    embed.add_field(name="Winners:", value=str(zwyciezcy), inline=True)
    embed.set_footer(text=f"Dziś o {datetime.datetime.now().strftime('%H:%M')}")

    view = GiveawayView()
    await interaction.response.send_message(content="🎉 **GIVEAWAY** 🎉", embed=embed, view=view)
    
    # Pobranie wysłanej wiadomości, aby móc ją edytować na koniec
    msg = await interaction.original_response()

    # Oczekiwanie na zakończenie konkursu
    await asyncio.sleep(sekundy)

    if not view.entries:
        return await interaction.followup.send(f"Konkurs **{tytul}** zakończył się, ale nikt nie wziął w nim udziału.")

    # --- SYSTEM LOSOWANIA Z WAGAMI (2x SZANSA) ---
    pool = []
    guild = interaction.guild
    
    for user_id in view.entries:
        # Każdy dostaje 1 "los" domyślnie
        pool.append(user_id)
        
        # Sprawdzamy, czy użytkownik ma specjalną rolę
        member = guild.get_member(user_id)
        if member and any(role.id == BONUS_ROLE_ID for role in member.roles):
            # Jeśli ma rolę, dodajemy jego ID drugi raz (2x większa szansa)
            pool.append(user_id)

    # Wybieranie zwycięzców (bez duplikatów)
    winners_ids = []
    max_possible_winners = min(zwyciezcy, len(set(view.entries)))
    
    while len(winners_ids) < max_possible_winners:
        winner = random.choice(pool)
        if winner not in winners_ids:
            winners_ids.append(winner)

    mentions = ", ".join([f"<@{w}>" for w in winners_ids])

    # Edycja Embedu na zakończenie
    end_embed = embed.copy()
    end_embed.clear_fields()
    end_embed.description = f"Zakończono! Nagroda: **{tytul}**"
    end_embed.add_field(name="Zwycięzcy:", value=mentions if mentions else "Brak", inline=False)
    end_embed.add_field(name="Entries:", value=str(len(set(view.entries))), inline=True)
    end_embed.color = discord.Color.red() # Zmiana koloru na czerwony po zakończeniu

    await msg.edit(content="🎉 **GIVEAWAY ZAKOŃCZONY** 🎉", embed=end_embed, view=None)
    await interaction.followup.send(f"Gratulacje {mentions}! Wygraliście: **{tytul}**!")
