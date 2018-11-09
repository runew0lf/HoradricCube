from discord.ext import commands


def is_admin():
    async def predicate(ctx):
        permissions = ctx.channel.permissions_for(ctx.author)
        return permissions.administrator
    return commands.check(predicate)
