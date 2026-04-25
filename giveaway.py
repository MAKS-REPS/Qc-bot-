import discord
import datetime
import asyncio
import random
import re

BONUS_ROLE_ID = 1497656242615746721

class GiveawayView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None) # timeout=None, aby przycisk nie wygasł
        self.entries = []

    @discord.ui.button(emoji="🎉", style=discord.ButtonStyle.blurple, custom_id="join_giveaway")
    async def join_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id in self.entries:
            return await interaction.response.send_message("Już bierzesz udział!", ephemeral=True)
        
        self.entries.append(interaction.user.id)
        await interaction.response.send_message("Dołączyłeś do giveaway!", ephemeral=True)

def parse_time(time_str):
    pos = {"s": 1, "m": 60, "h": 3600, "d": 86400}
    match = re.match(r"(\d+)([smhd])", time_str.lower())
    if match:
        return int(match.group(1)) * pos[match.group(2)]
    return None

async def run_giveaway(interaction, tytul, opis, sekundy, zwyciezcy, kolor_hex):
    # Konwersja koloru
    try:
        color_value = int(kolor_hex.replace("#", ""), 16)
    except:
        color_value = 0x3498db

    end_time = datetime.datetime.now() + datetime.timedelta(seconds=sekundy)
    timestamp = int(end_time.timestamp())

    embed = discord.Embed(
        title=tytul,
        description=f"{opis}\n\n**Konta mają być nowe, na dowód należy wysłać ssa po założeniu / brak spełnienia wymagań = ponowne losowanie**",
        color=discord.Color(color_value)
    )
    embed.add_field(name="Ends:", value=f"<t:{timestamp}:R> (<t:{timestamp}:f>)", inline=False)
    embed.add_field(name="Hosted by:", value=interaction.user.mention, inline=True)
    embed.add_field(name="Winners:", value=str(zwyciezcy), inline=True)
    embed.set_footer(text=f"Dziś o {datetime.datetime.now().strftime('%H:%M')}")

    view = GiveawayView()
    await interaction.response.send_message(content="🎉 **GIVEAWAY** 🎉", embed=embed, view=view)
    msg = await interaction.original_response()

    await asyncio.sleep(sekundy)

    if not view.entries:
        return await interaction.followup.send(f"Nikt nie wziął udziału w **{tytul}**.")

    # System wag (2x szansa dla roli)
    pool = []
    for u_id in view.entries:
        pool.append(u_id)
        member = interaction.guild.get_member(u_id)
        if member and any(r.id == BONUS_ROLE_ID for r in member.roles):
            pool.append(u_id)

    # Losowanie
    winners_list = []
    actual_winners_count = min(zwyciezcy, len(set(view.entries)))
    while len(winners_list) < actual_winners_count:
        w_id = random.choice(pool)
        if w_id not in winners_list:
            winners_list.append(w_id)

    mentions = ", ".join([f"<@{wid}>" for wid in winners_list])
    
    end_embed = embed.copy()
    end_embed.clear_fields()
    end_embed.add_field(name="Zwycięzcy:", value=mentions if mentions else "Brak", inline=False)
    end_embed.color = discord.Color.red()
    
    await msg.edit(embed=end_embed, view=None)
    await interaction.followup.send(f"Gratulacje {mentions}! Wygraliście: **{tytul}**!")
