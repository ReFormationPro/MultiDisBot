"""
TODO Actually set alarm
TODO If server restarts, set alarms
TODO Allow only one alarm to be set (?)
TODO At alarm unset and at alarm info, check alarm count
"""

from discord.ext import commands

from common.BaseCommandManager import BaseCommandManager
from database.ReplitDatabase import ReplitDatabaseManager as RDM

from .News import News
from .Config import Config

@commands.command()
async def alarmset(ctx, hour, minute):
    server = CommandManager.getGuildName(ctx)
    print("Alarm set called on %s with %d.%d"%(server, int(hour), int(minute)))
    RDM.add(server, Config.ALARMS_TABLE, 
        {"hour": hour, "minute": minute})

@commands.command()
async def alarmunset(ctx):
    server = CommandManager.getGuildName(ctx)
    print("Alarm unset called on %s"%server)
    RDM.remove(server, Config.ALARMS_TABLE, 0)

@commands.command()
async def alarminfo(ctx):
    server = CommandManager.getGuildName(ctx)
    obj = RDM.getAtIdx(server, Config.ALARMS_TABLE, 0)
    print("Alarm info called on %s"%server)
    print(obj)

class CommandManager(BaseCommandManager):
    bot = None
    # Every command defined above
    COMMANDS = [alarmset, alarmunset, alarminfo]
    
    @classmethod
    def getCmdHelp(cls, cmdName):
        return "Help is not yet implemented"