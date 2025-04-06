import discord
from discord.ext import commands
import aiohttp
import random

class Anime(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def fetch_image(self, url, key=None):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as r:
                data = await r.json()
                return data[key] if key else random.choice(data)

    async def send_embed(self, ctx, action, target, image_url):
        embed = discord.Embed(
            title=f"✨ {ctx.author.display_name} {action} {target.display_name if target else 'the air'}!",
            color=random.choice([discord.Color.purple(), discord.Color.blue(), discord.Color.teal(), discord.Color.orange()])
        )
        embed.set_image(url=image_url)
        embed.set_thumbnail(url=ctx.author.display_avatar.url)
        embed.set_footer(text=f"Requested by {ctx.author.display_name}", icon_url=ctx.author.display_avatar.url)
        await ctx.send(embed=embed)

    # SFW ACTIONS
    @commands.command()
    async def kiss(self, ctx, member: discord.Member = None):
        if not member:
            return await ctx.send("💋 Who are you kissing? Mention someone!")
        url = await self.fetch_image("https://nekos.best/api/v2/kiss", "results")
        await self.send_embed(ctx, "kissed", member, url[0]["url"])

    @commands.command()
    async def hug(self, ctx, member: discord.Member = None):
        if not member:
            return await ctx.send("🤗 Who are you hugging? Mention someone!")
        url = await self.fetch_image("https://nekos.best/api/v2/hug", "results")
        await self.send_embed(ctx, "hugged", member, url[0]["url"])

    @commands.command()
    async def slap(self, ctx, member: discord.Member = None):
        if not member:
            return await ctx.send("👋 Who are you slapping? Mention someone!")
        url = await self.fetch_image("https://nekos.best/api/v2/slap", "results")
        await self.send_embed(ctx, "slapped", member, url[0]["url"])

    @commands.command()
    async def cuddle(self, ctx, member: discord.Member = None):
        if not member:
            return await ctx.send("🐻 Who are you cuddling? Mention someone!")
        url = await self.fetch_image("https://nekos.best/api/v2/cuddle", "results")
        await self.send_embed(ctx, "cuddled", member, url[0]["url"])

    @commands.command()
    async def pat(self, ctx, member: discord.Member = None):
        if not member:
            return await ctx.send("🫶 Who are you patting? Mention someone!")
        url = await self.fetch_image("https://nekos.best/api/v2/pat", "results")
        await self.send_embed(ctx, "patted", member, url[0]["url"])

    @commands.command()
    async def lick(self, ctx, member: discord.Member = None):
        if not member:
            return await ctx.send("👅 Who are you licking? Mention someone!")
        url = await self.fetch_image("https://api.waifu.pics/sfw/lick", "url")
        await self.send_embed(ctx, "licked", member, url)

    @commands.command()
    async def blush(self, ctx):
        url = await self.fetch_image("https://nekos.best/api/v2/blush", "results")
        await self.send_embed(ctx, "is blushing!", None, url[0]["url"])

    @commands.command()
    async def rage(self, ctx):
        url = await self.fetch_image("https://nekos.best/api/v2/angry", "results")
        await self.send_embed(ctx, "is raging!", None, url[0]["url"])

    @commands.command()
    async def angry(self, ctx):
        url = await self.fetch_image("https://nekos.best/api/v2/angry", "results")
        await self.send_embed(ctx, "is angry!", None, url[0]["url"])

    @commands.command()
    async def sad(self, ctx):
        url = await self.fetch_image("https://nekos.best/api/v2/cry", "results")
        await self.send_embed(ctx, "is feeling sad.", None, url[0]["url"])

    # NSFW
    @commands.command()
    async def boobs(self, ctx):
        if not ctx.channel.is_nsfw():
            return await ctx.send("🔞 This command can only be used in NSFW channels.")
        url = await self.fetch_image("https://nekos.life/api/v2/img/boobs", "url")
        await self.send_embed(ctx, "is staring at some boobs 😳", None, url)

    @commands.command()
    async def thighs(self, ctx):
        if not ctx.channel.is_nsfw():
            return await ctx.send("🔞 This command can only be used in NSFW channels.")
        url = await self.fetch_image("https://nekos.life/api/v2/img/thigh", "url")
        await self.send_embed(ctx, "is admiring some thighs 👀", None, url)

    @commands.command()
    async def hentai(self, ctx):
        if not ctx.channel.is_nsfw():
            return await ctx.send("🔞 This command can only be used in NSFW channels.")
        url = await self.fetch_image("https://nekos.life/api/v2/img/hentai", "url")
        await self.send_embed(ctx, "is watching hentai 🤤", None, url)

    @commands.command()
    async def ass(self, ctx):
        if not ctx.channel.is_nsfw():
            return await ctx.send("🔞 This command can only be used in NSFW channels.")
        url = await self.fetch_image("https://nekos.life/api/v2/img/ass", "url")
        await self.send_embed(ctx, "is looking at some booty 🍑", None, url)

async def setup(bot):
    await bot.add_cog(Anime(bot))