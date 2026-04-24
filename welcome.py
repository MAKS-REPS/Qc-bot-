import discord

async def handle_welcome(member, channel_id, color):
    channel = member.guild.get_channel(channel_id)
    if channel:
        count = member.guild.member_count
        embed = discord.Embed(
            title="👋 Maks Reps × WITAMY",
            description=(
                f"• 🤱 × Witaj {member.mention} na **Maks Reps**\n"
                f"• 👥 × Jesteś **{count} osobą** na naszym serwerze!\n"
                f"• ✨ × Liczymy, że zostaniesz z nami na dłużej!"
            ),
            color=color
        )
        embed.set_thumbnail(url=member.display_avatar.url)
        await channel.send(embed=embed)
