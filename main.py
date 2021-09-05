import os

from discord.ext import commands

from .CommandManager import CommandManager
from .ReplitDatabase import ReplitDatabaseManager as RDM

bot = commands.Bot(command_prefix='$')
CommandManager.initialize(bot)

@bot.event
async def on_guild_join(guild):
    server = guild.name
    if not RDM.serverExists(server):
        RDM.createServer(server)
        RDM.createTable(server, RDM.QUESTION_TABLE)
        RDM.createTable(server, RDM.SESSION_TABLE)

@bot.event
async def on_guild_remove(guild):
    server = guild.name
    if RDM.serverExists(server):
        RDM.deleteServer(server)

# DEBUG
# TODO use server id instead of server name
server = "DeliciousMalicious's server"
if not RDM.serverExists(server):
    RDM.createServer(server)
    RDM.createTable(server, RDM.QUESTION_TABLE)
    RDM.createTable(server, RDM.SESSION_TABLE)

bot.run(os.getenv('TOKEN'))