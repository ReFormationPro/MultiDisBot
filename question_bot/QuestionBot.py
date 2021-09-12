from common.BaseBot import BaseBot
from database import ReplitDatabase as RDM

from .CommandManager import CommandManager
from .Config import Config

class QuestionBot(BaseBot):
    """
    Initialize question bot for a server
    """
    
    @staticmethod
    def initialize(bot):
        CommandManager.initialize(bot)
        # DEBUG
        server = "DeliciousMalicious's server"
        if not RDM.serverExists(server):
            RDM.createServer(server)
            RDM.createTable(server, Config.QUESTION_TABLE)
            RDM.createTable(server, Config.SESSION_TABLE)

    @staticmethod
    async def on_guild_join(guild):
        # TODO use server id instead of server name
        server = guild.name
        if not RDM.serverExists(server):
            RDM.createServer(server)
        if not RDM.tableExists(server, Config.QUESTION_TABLE):
            RDM.createTable(server, Config.QUESTION_TABLE)
        if not RDM.tableExists(server, Config.SESSION_TABLE):
            RDM.createTable(server, Config.SESSION_TABLE)
    
    @staticmethod
    async def on_guild_remove(guild):
        server = guild.name
        if RDM.serverExists(server):
            RDM.deleteServer(server)