import discord
from discord.ext import commands, tasks
import utils
import aiosqlite
from aiosqlite import IntegrityError
import assets
from itertools import cycle
global status 
#-----------------------------------------------------------
intents = discord.Intents()
intents.all()
bot = commands.Bot(command_prefix=utils.get_prefix, intents=intents.all(), case_insensitive=True)
bot.remove_command("ping")
bot.remove_command("help")

@bot.event
async def on_guild_join(guild):
    # we don't need to add the guild if it was already there
    db = await aiosqlite.connect(assets.server_db_path)
    await db.execute("CREATE TABLE IF NOT EXISTS guilds (guildid INTEGER UNIQUE, prefix TEXT)")
    await db.commit()
    for guild in bot.guilds:
        try:
            await db.execute(f"INSERT OR IGNORE INTO guilds VALUES(?, ?)", (guild.id, "sdOS-",))
            await db.commit()
            print(f"Added {guild.id} to the db!\n")
        except IntegrityError:
            print(f"{guild.id} already exists.\n")
        except ValueError:
            pass
        try:
            await db.close()
        except ValueError:
            pass


# Starts the presence loop.
@tasks.loop(minutes=3)
async def change_status():
    global status
    # Setting the status cycle.
    status = cycle(assets.statuses)  # Creates statuses for the status cycle.
    await bot.change_presence(activity=discord.Game(next(status)))

@bot.event
# Logging in and selecting the first status for the status cycler to use.
async def on_ready():
    # sanity check, in case the bot was added during downtime'
    for guild in bot.guilds:
        await on_guild_join(guild)  
    for extension in assets.extensions:
        bot.load_extension(extension)
    change_status.start()



@bot.command(name="prefix")
async def prefix(ctx,*, prefix=None):
    """Change my prefix"""
    db = await aiosqlite.connect(assets.server_db_path)
    if prefix is not None:
        await db.execute("DELETE FROM guilds WHERE guildid = ?", (ctx.guild.id,))
        await db.commit()
        await db.execute("INSERT INTO guilds VALUES (?, ?)", (ctx.guild.id, prefix,))
        await db.commit()
        await db.close()
        await ctx.send(f"New prefix set to {prefix}")
    else:
        return await ctx.send(f"My current prefix is {ctx.prefix}")



token = utils.loadjson(assets.conf_path)
runtoken = token["token"]

bot.run(runtoken)