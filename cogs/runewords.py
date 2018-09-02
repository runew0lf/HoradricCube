from discord.ext import commands
import discord
import logging
import json
import difflib
import re
#https://discordapp.com/oauth2/authorize?&client_id=485773594543128597&scope=bot&permissions=8

log = logging.getLogger(__name__)

EMPTY = u'\u200b'

with open("runeword-data.json", "r") as read_file:
    data = json.load(read_file)

runeword_array = []
for word in data['collection1']:
    runeword_array.append(word['runeword-name']['text'])

with open("runes.json", "r") as read_file:
    runes_data = json.load(read_file)

class Diablo:
    def __init__(self, bot):
        self.bot = bot

    def lookup_emoji(self, name):
        emojiguild = self.bot.get_guild(469882233751076874)
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
                for i in range(0, len(versionlist)):
                    if versionlist[i] == "Yes":
                        versionlist[i] = "✅"
                    else:
                        versionlist[i] = "❌"

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

                embed.add_field(name="Runes", value="  ".join(split_runes))
                embed.add_field(name="Sockets", value="  ".join(sockets))
                embed.add_field(name=EMPTY, value=EMPTY)
                embed.add_field(name="1.11", value=versionlist[0])
                embed.add_field(name="1.10", value=versionlist[1])
                embed.add_field(name="1.09", value=versionlist[2])
                embed.add_field(name="Info", value=info)
                embed.add_field(name="Properties", value=item['runeword-properties'])
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
                embed.add_field(name="Ilvl/Clvl", value = item['lvl'])
                embed.add_field(name="Weapon", value = item['weapon'])
                embed.add_field(name="Armor", value= item['etc'])
                await ctx.send(embed=embed)




def setup(bot):
    bot.add_cog(Diablo(bot))
    log.info("Cog loaded: Diablo")
