from discord.ext import commands
import discord
import logging
import json
import difflib
import re
import config
#https://discordapp.com/oauth2/authorize?&client_id=485773594543128597&scope=bot&permissions=8

log = logging.getLogger(__name__)

EMPTY = u'\u200b'
BLANK = u'\u202F'

with open("runeword-data.json", "r") as read_file:
    data = json.load(read_file)

runeword_array = []
for word in data['collection1']:
    runeword_array.append(word['runeword-name']['text'])

with open("runes.json", "r") as read_file:
    runes_data = json.load(read_file)

with open("gems.json", "r") as read_file:
    gems_data = json.load(read_file)

gems_array = []
for word in gems_data:
    gems_array.append(word['name'])

with open("sets.json", "r") as read_file:
    sets_data = json.load(read_file)

sets_array = []
for word in sets_data:
    sets_array.append(word['name'])


class Diablo:
    def __init__(self, bot):
        self.bot = bot

    def lookup_emoji(self, name):
        for guild in config.EMOTESERVERID:
            emojiguild = self.bot.get_guild(guild)
            emoji1 = discord.utils.get(emojiguild.emojis, name=str(name))
            if emoji1 is not None:
                return f"<:{emoji1.name}:{emoji1.id}>"
        return f"**{name}**"

    @commands.command(name='runeword')
    async def runeword(self, ctx, *, rune):
        """
        Displays runeword information
        """
        matches = difflib.get_close_matches(rune, runeword_array, 1, cutoff=0.4)[0]
        for item in data['collection1']:
            if item['runeword-name']['text'] == matches:
                embed = discord.Embed(title=f"__{matches}__", description="", color=ctx.me.color)
                versionlist = [item['runeword-1.11'], item['runeword-1.10'], item['runeword-1.09']]
                versionnumber= ""
                versionnumbers = ["1.11", "1.10", "1.09"]
                for i in range(0, len(versionlist)):
                    if versionlist[i] == "Yes":
                        versionnumber = f"✅ {versionnumbers[i]}+"
                        if item['ladder-only'] == "Yes":
                            versionnumber = versionnumber + " (Ladder Only)"
                    else:
                        break

                sockets = []
                split_runes = re.findall('[A-Z][^A-Z]*', item['runeword-runes'])
                for i in range(0, len(split_runes)):
                    split_runes[i] = self.lookup_emoji(f"28px{split_runes[i]}_Rune")
                    sockets.append(self.lookup_emoji("socket"))

                info = item['runeword-info'].split("\n")
                info.pop(0)

                info = "\n".join(info)
                info = re.sub("([{]).*?([}])", "", info)
                info = re.sub("([/(]).*?([/)])", "", info)

                properties = item['runeword-properties']
                if "Both" in properties:
                    properties = properties.replace("Both\n", "**Both**\n")
                    properties = properties.replace("Weapons\n", "**Weapons**\n")
                    properties = properties.replace("Armor\n", "**Armor**\n")
                    properties = properties.replace("Shields\n", "**Shields**\n")
                    properties = properties.replace("Swords\n", "**Swords**\n")
                    properties = properties.replace("Headgear\n", "**Headgear**\n")


                embed.add_field(name="Runes", value="  ".join(split_runes))
                embed.add_field(name="Sockets", value="  ".join(sockets))
                embed.add_field(name="Versions", value=versionnumber, inline=True)
                embed.add_field(name="Info", value=info, inline=False)
                embed.add_field(name="Properties", value=properties, inline=False)
                await ctx.send(embed=embed)

    @commands.command(name='rune')
    async def rune(self, ctx, *, rune):
        """
        Displays rune information
        """
        for item in runes_data:
            if item['name'].lower() == rune.lower():
                embed = discord.Embed(title=item['name'],
                                      description=self.lookup_emoji(f"28px{item['name']}_Rune"),
                                      color=ctx.me.color)
                embed.add_field(name="Clvl", value = item['lvl'])
                embed.add_field(name="Weapon", value = item['weapon'])
                embed.add_field(name="Armor", value= item['etc'])
                await ctx.send(embed=embed)

    @commands.command(name='gem')
    async def gem(self, ctx, *, gem):
        """
        Displays rune information
        """
        matches = difflib.get_close_matches(gem, gems_array, 1, cutoff=0.4)[0]
        for item in gems_data:
            if item['name'] == matches:
                emote = item['name'].lower().replace(" ", "")
                embed = discord.Embed(title=matches,
                                      description=self.lookup_emoji(f"{emote}"),
                                      color=ctx.me.color)
                embed.add_field(name="Clvl", value = item['lvl'])
                embed.add_field(name="Weapon", value = item['weapon'])
                embed.add_field(name="Armor & Helms", value= item['armour'])
                embed.add_field(name="Shield", value= item['shields'])
                await ctx.send(embed=embed)

    @commands.command(name='set')
    async def item_set(self, ctx, *, item_set):
        """
        Displays set information
        """
        matches = difflib.get_close_matches(item_set, sets_array, 1, cutoff=0.4)[0]
        for item in sets_data:
            if item['name'] == matches:
                emote = item['name'].lower().replace(" ", "")
                embed = discord.Embed(title=matches,
                                      description=BLANK,
                                      color=ctx.me.color)
                embed.add_field(name="Properties", value=item['properties'])
                embed.set_thumbnail(url=item["url"])
                await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Diablo(bot))
    log.info("Cog loaded: Diablo")
