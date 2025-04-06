import discord
from discord.ext import commands

class Sticky(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.sticky_data = {
            # channel_id: message_content
            1157945275546075258: {
                "title": "HOW TO VOUCH ?",
                "description": "Please Use `/vouch` command To Write A review"
            }
        }
        self.last_sent = {}  # channel_id: message_id

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        sticky = self.sticky_data.get(message.channel.id)
        if not sticky:
            return

        # Delete previous sticky if exists
        last_id = self.last_sent.get(message.channel.id)
        if last_id:
            try:
                old_msg = await message.channel.fetch_message(last_id)
                await old_msg.delete()
            except:
                pass  # message may be gone

        embed = discord.Embed(
            title=f"**{sticky['title']}**",
            description=sticky['description'],
            color=discord.Color.from_rgb(0, 204, 255)  # that light blue line vibe
        )

        sent = await message.channel.send(embed=embed)
        self.last_sent[message.channel.id] = sent.id

async def setup(bot):
    await bot.add_cog(Sticky(bot))
