import discord
import asyncio

# --- KONFIGURACJA PRZENIESIONA ---
ID_KATEGORII_TICKETOW = 1486842150661656767
REQUIRED_ROLE_ID = 1457769309735485450
MAKS_BLUE = 0x3498db

class TicketCloseView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="🔒 Zamknij ticket", style=discord.ButtonStyle.danger, custom_id="persistent_close_ticket")
    async def close_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        # 👑 Sprawdzenie, czy klikający to na pewno Owner serwera
        if interaction.user.id != interaction.guild.owner_id:
            return await interaction.response.send_message(
                "❌ Tylko **Owner serwera** ma uprawnienia do zamknięcia i usunięcia tego ticketu!", 
                ephemeral=True
            )
        
        # Deferowanie odpowiedzi, żeby Discord nie rzucił błędem czasu oczekiwania
        await interaction.response.defer()
        
        # 🎬 Rozpoczęcie mini animacji zamykania za pomocą Embedu
        anim_embed = discord.Embed(
            title="🔒 PROCEDURA ZAMYKANIA TICKETU",
            description="⚙️ Inicjalizacja procesu kasowania pokoju...\n`[⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜]` 0%",
            color=discord.Color.red()
        )
        
        msg = await interaction.followup.send(embed=anim_embed)
        
        # Klatki animacji: (tekst, czas oczekiwania)
        frames = [
            ("⚙️ Generowanie archiwum rozmowy...\n`[🟩🟩🟩⬜⬜⬜⬜⬜⬜⬜]` 30%", 0.8),
            ("⚙️ Czyszczenie uprawnień i ról...\n`[🟩🟩🟩🟩🟩🟩🟩⬜⬜⬜]` 70%", 0.8),
            ("⚠️ Kanał zostanie bezpowrotnie usunięty za **3**...\n`[🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩]` 100%", 1.0),
            ("⚠️ Kanał zostanie bezpowrotnie usunięty za **2**...\n`[🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩]` 100%", 1.0),
            ("⚠️ Kanał zostanie bezpowrotnie usunięty za **1**...\n`[🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩]` 100%", 1.0)
        ]
        
        for text, delay in frames:
            await asyncio.sleep(delay)
            anim_embed.description = text
            await msg.edit(embed=anim_embed)
            
        # Ostateczne usunięcie kanału
        await asyncio.sleep(0.2)
        await interaction.channel.delete()


class TicketMenu(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="POMOC", description="Ogólna pomoc i pytania", emoji="❓"),
            discord.SelectOption(label="POMOC Z ZAMÓWIENIEM", description="Kliknij, jeśli potrzebujesz pomocy z zamówieniem", emoji="🛒"),
            discord.SelectOption(label="PROBLEM Z SHIPPINGIEM", description="Kliknij, jeśli masz problem z shippingiem", emoji="🚛"),
            discord.SelectOption(label="DOSTĘP", description="Kliknij, aby uzyskać dostęp", emoji="🔑"),
            discord.SelectOption(label="WSPÓŁPRACA", description="Chcesz zostać naszym promotorem? Kliknij tutaj!", emoji="🤝"),
        ]
        super().__init__(
            placeholder="❌ Nie wybrano żadnej z kategorii", 
            min_values=1, 
            max_values=1, 
            options=options, 
            custom_id="persistent_ticket_select"
        )

    async def callback(self, interaction: discord.Interaction):
        guild = interaction.guild
        category = guild.get_channel(ID_KATEGORII_TICKETOW)
        admin_role = guild.get_role(REQUIRED_ROLE_ID)
        
        if not category or not admin_role:
            return await interaction.response.send_message("❌ Błąd konfiguracji serwera (brak kategorii lub roli).", ephemeral=True)

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            interaction.user: discord.PermissionOverwrite(read_messages=True, send_messages=True, attach_files=True),
            admin_role: discord.PermissionOverwrite(read_messages=True, send_messages=True, attach_files=True)
        }
        
        # Tworzenie kanału
        channel = await guild.create_text_channel(
            name=f"ticket-{interaction.user.name}", 
            category=category, 
            overwrites=overwrites
        )
        
        embed = discord.Embed(
            title="🎫 MAKS REPS × TICKET", 
            description=f"Witaj {interaction.user.mention}!\nWybrałeś kategorię: **{self.values[0]}**.\nZaraz ktoś z administracji Ci pomoże.", 
            color=MAKS_BLUE
        )
        
        # 🔥 Podpięcie widoku z przyciskiem zamykania do wiadomości powitalnej wewnątrz ticketu
        await channel.send(
            content=f"{interaction.user.mention} | {admin_role.mention}", 
            embed=embed, 
            view=TicketCloseView()
        )
        await interaction.response.send_message(f"✅ Otwarto ticket: {channel.mention}", ephemeral=True)


class TicketView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(TicketMenu())
