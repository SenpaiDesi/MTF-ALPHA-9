import discord
from discord.ext import commands
from discord.errors import Forbidden

async def send_embed(ctx, embed):
    """Function to send embeds"""
    try:
        await ctx.send(embed = embed)
    except Forbidden:
        try:
            await ctx.send("Hey, I can not send embeds here. Please check my permissions.")
        except Forbidden:
            await ctx.author.send(f"Hey, It seems I can not send any messages in {ctx.guild.name} at {ctx.channel.name}. Please inform a staff member.")


class HelpCommand(commands.Cog):
    """This module"""
    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    async def help (self, ctx, *input):
        """Shows a beutifull help command. """
        prefix = ctx.prefix
        version = "0.0.1"

        if not input:
            emb = discord.Embed(title ="Commands and modules", color = discord.Color.darker_grey(), description= f"Use {ctx.prefix}help <module> to gain more information about that module.")
            cogs_desc = ''
            for cog in self.bot.cogs:
                cogs_desc += f'`{cog}` {self.bot.cogs[cog].__doc__}\n'

            emb.add_field(name = "Modules", value = cogs_desc, inline=False)

            commands_desc = ''
            for command in self.bot.walk_commands():
                if not command.cog_name and not command.hidden:
                    commands_desc += f"`{command.name}` - {command.help}\n"

            if commands_desc:
                emb.add_field(name='Not belonging to a module', value=commands_desc, inline=False)

            emb.add_field(name = "About", value=f"This bot is currenly being developed by Senpai_Desi#4108.")
            emb.set_footer(text = f"Running {version}.")

        elif len(input) == 1:
            for cog in self.bot.cogs:
                if cog.lower() == input[0].lower():
                    emb = discord.Embed(title = f"{cog} - Commands", description= self.bot.cogs[cog].__doc__, color = discord.Color.random())

                    for command in self.bot.get_cog(cog).get_commands():
                        if not command.hidden:
                            emb.add_field(name=f"`{ctx.prefix}{command.name}`", value = command.help, inline=False)
                    break
                else:
                    emb = discord.Embed(title="Oh no!", description=f"I dont know the module {input[0]}.", color = discord.Color.red())

        elif len(input) > 1:
            emb = discord.Embed(title="Slow down there operative!", description=f"Please use only one module at the time.", color = discord.Color.gold())

        else:
            emb = discord.Embed(title = "Oh oh, I miscalculated. Unable to fetch commands at this time.", color = discord.Color.red())

        await send_embed(ctx, emb)


def setup(bot):
    bot.add_cog(HelpCommand(bot))