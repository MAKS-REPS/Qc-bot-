import discord
from discord import app_commands

async def setup_embed_command(bot, REQUIRED_ROLE_ID, MAKS_BLUE):
    @bot.tree.command(name="embed", description="Wysyła spersonalizowany komunikat w ramce (Embed)")
    @app_commands.describe(
        tytul="Nagłówek wiadomości",
        opis="Treść wiadomości (użyj \\n dla nowej linii)",
        kolor="Kolor paska w formacie HEX (np. #ff0000 lub zostaw puste dla domyślnego)"
    )
    async def create_embed(interaction: discord.Interaction, tytul: str, opis: str, kolor: str = None):
        # Sprawdzenie uprawnień
        if not any(role.id == REQUIRED_ROLE_ID for role in interaction.user.roles):
            return await interaction.response.send_message("❌ Brak uprawnień do używania tej komendy.", ephemeral=True)

        # Logika koloru
        if kolor:
            try:
                hex_str = kolor.replace("#", "")
                embed_color = int(hex_str, 16)
            except ValueError:
                return await interaction.response.send_message("❌ Błędny format koloru HEX! Użyj np. #ff0000", ephemeral=True)
        else:
            embed_color = MAKS_BLUE

        # Formatowanie nowej linii
        format_opis = opis.replace("\\n", "\n")
        
        new_embed = discord.Embed(
            title=tytul,
            description=format_opis,
            color=embed_color
        )
        
        new_embed.set_footer(text=f"Wysłane przez: {interaction.user.display_name}")

        await interaction.response.send_message("✅ Embed wysłany!", ephemeral=True)
        await interaction.channel.send(embed=new_embed)
