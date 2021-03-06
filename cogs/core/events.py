import arrow
import discord
from discord.ext import commands
from random import choice


class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.db = self.bot.get_cog("Database")

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"\n\u001b[36;1m CONNECTED \u001b[0m [{self.bot.shard_count} Shards]\n")
        await self.bot.change_presence(activity=discord.Game(choice(["on Hypixel", "SkyBlock", "Bedwars", "Skywars"])),
                                       status=discord.Status.idle)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        await self.db.drop_prefix(guild.id)

    @commands.Cog.listener()
    async def on_message(self, msg):
        if msg.content.startswith(f'<@!{self.bot.user.id}>'):
            if msg.guild is not None:
                prefix = await self.db.get_prefix(msg.guild.id)
                prefix = prefix if prefix is not None else "h!"
            else:
                prefix = "h!"
            help_embed = discord.Embed(color=await self.bot.cc(msg.author.id),
                                       description=f"The prefix for this server is ``{prefix}`` and the help command is ``{prefix}help``\n"
                                                   f"If you are in need of more help, you can join the **[Support Server](https://discord.gg/{self.bot.guild_invite_code})**.")
            help_embed.set_author(name="Hypixel Stats", icon_url=str(self.bot.user.avatar_url_as(static_format="png")))
            help_embed.set_footer(text="Made by Iapetus11 & TrustedMercury!")
            try:
                await msg.channel.send(embed=help_embed)
            except discord.errors.Forbidden:
                pass


def setup(bot):
    bot.add_cog(Events(bot))
