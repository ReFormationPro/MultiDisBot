from news_bot.CommandManager import CommandManager
from common.BaseBot import BaseBot
from database.ReplitDatabase import ReplitDatabaseManager as RDM

from .Config import Config
from .CommandManager import CommandManager

class NewsBot(BaseBot):
    @staticmethod
    def initialize(bot):
        CommandManager.initialize(bot)
        server = "DeliciousMalicious's server"
        if not RDM.serverExists(server):
            RDM.createServer(server)
        if not RDM.tableExists(server, Config.ALARMS_TABLE):
            RDM.createTable(server, Config.ALARMS_TABLE)
    
    @staticmethod
    async def on_guild_join(guild):
        # TODO use server id instead of server name
        server = guild.name
        if not RDM.serverExists(server):
            RDM.createServer(server)
        if not RDM.tableExists(server, Config.ALARMS_TABLE):
            RDM.createTable(server, Config.ALARMS_TABLE)
    
    @staticmethod
    async def on_guild_remove(guild):
        server = guild.name
        if RDM.serverExists(server):
            RDM.deleteServer(server)