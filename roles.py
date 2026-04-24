import discord

class RoleView(discord.ui.View):
    def __init__(self, role_tiktok_id, role_promocje_id):
        super().__init__(timeout=None)
        self.role_tiktok_id = role_tiktok_id
        self.role_promocje_id = role_promocje_id

    async def toggle_role(self, interaction: discord.Interaction, role_id: int):
        role = interaction.guild.get_role(role_id)
        if role in interaction.user.roles:
            await interaction.user.remove_roles(role)
            await interaction.response.send_message(f"❌ Usunięto rolę {role.mention}", ephemeral=True)
        else:
            await interaction.user.add_roles(role)
            await interaction.response.send_message(f"✅ Nadano rolę {role.mention}", ephemeral=True)

    @discord.ui.button(label="Ping Promocje", style=discord.ButtonStyle.blurple, emoji="🎁", custom_id="role_promocje")
    async def promocje(self, interaction, button):
        await self.toggle_role(interaction, self.role_promocje_id)

    @discord.ui.button(label="Ping TikTok", style=discord.ButtonStyle.gray, emoji="🎬", custom_id="role_tiktok")
    async def tiktok(self, interaction, button):
        await self.toggle_role(interaction, self.role_tiktok_id)
