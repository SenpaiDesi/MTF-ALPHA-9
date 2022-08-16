import json
import aiosqlite
import assets
import sqlite3
def loadjson(path):
    with open(path, "r") as f:
        return json.load(f)


async def get_prefix(_bot, message):
    db = await aiosqlite.connect(assets.server_db_path)
    async with db.execute("SELECT prefix FROM guilds WHERE guildid = ?", (message.guild.id,)) as cursor:
        async for entry in cursor:
            prefix = entry
            return prefix
    try:
       await db.close()
    except ValueError:
        pass


async def servdbint():
    db = await aiosqlite.connect(assets.server_db_path)
    try:
        await db.execute("CREATE TABLE IF NOT EXISTS modlogs (caseid TEXT PRIMARY KEY, guildid INT, user INT, moderator INT, type TEXT, reason TEXT, duration TEXT)")
        await db.commit()
        await db.close()
    except ValueError:
        pass
    print("[INFO] Created db because it did not exist yet.\n")
