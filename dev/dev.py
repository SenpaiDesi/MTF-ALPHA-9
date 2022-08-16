import discord
import aiosqlite
import sqlite3
from discord.ext import commands 
import asyncio
import re 
import assets




class admins(commands.Cog):
    """Bot dev only commands"""
    def __init__(self, bot):
        self.bot = bot


    @commands.command(name='setup')
    @commands.is_owner()
    async def dbsetup(self, ctx):
        """Db setup and init."""
        try:
            db = await aiosqlite.connect(assets.server_db_path)
            msg = await ctx.send("Initialising....")
            await asyncio.sleep(2)
            await msg.edit(content = "Setting up log db (task 1/3)")
            try:
                await db.execute("CREATE TABLE IF NOT EXISTS moderationLogs (logid INTEGER PRIMARY KEY, guildid int, moderationLogTypes int, userid int, moduserid int, content varchar, duration VARCHAR)")
                await db.commit()
            except Exception as e:
                return msg.edit(content = f"FAILED TASK 1/3 because of \n{e}")
            await asyncio.sleep(2)
            await msg.edit(content = "Creating log type converter (task 2/3)")
            try:
                await db.execute("CREATE TABLE IF NOT EXISTS logtypes (Type INTEGER PRIMARY KEY, Form TEXT)")
                await db.commit()
            except Exception as e:
                return await msg.edit(content  = f"FAILED TASK 2/3 because of \n{e}")
            await asyncio.sleep(2)
            await msg.edit(content  = "Inserting default logtype converter (task 3/3)")
            try:
                await db.execute("INSERT OR IGNORE INTO logtypes VALUES (?, ?)", (1, "warn",))
                await db.execute("INSERT OR IGNORE INTO logtypes VALUES (?, ?)", (2, "mute",))
                await db.execute("INSERT OR IGNORE INTO logtypes VALUES (?, ?)", (3, "unmute",))
                await db.execute("INSERT OR IGNORE INTO logtypes VALUES (?, ?)", (4, "kick",))
                await db.execute("INSERT OR IGNORE INTO logtypes VALUES (?, ?)", (5, "softban",))
                await db.execute("INSERT OR IGNORE INTO logtypes VALUES (?, ?)", (6, "ban",))
                await db.execute("INSERT OR IGNORE INTO logtypes VALUES (?, ?)", (7, "unban",))
                await db.commit()
            except Exception as e:
                return await msg.edit(content = f"FAILED TASK 3/3 because of \n{e}")
            await asyncio.sleep(2)
            await msg.edit(content = f"Closing database")
            try:
                await db.close()
            except ValueError:
                pass
            except Exception as e:
                return await msg.edit(content = f"Failed to close db because of \n{e}")
            await asyncio.sleep(2)
            await msg.edit(content =  "Done!")
        except commands.NotOwner:
            return await ctx.send("You do not own this bot!")


def setup(bot):
    bot.add_cog(admins(bot))