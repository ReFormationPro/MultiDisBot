"""
TODO Actually set alarm
TODO If server restarts, set alarms
TODO Allow only one alarm to be set (?)
TODO At alarm unset and at alarm info, check alarm count
"""

from discord.ext import commands

from common.BaseCommandManager import BaseCommandManager
from database.ReplitDatabase import ReplitDatabaseManager as RDM

from .News import AlarmConfig
from .Config import Config
from .Alarm import AlarmManager

@commands.command()
async def alarmset(ctx, channel, at_hour=12, at_min=0,
                country='tr', pagesize=1,
                timezone='Europe/Istanbul', 
                endpoint='https://newsapi.org/v2/top-headlines'):
    server = CommandManager.getGuildName(ctx)
    print("Alarm set called on %s with %d.%d"%(server, int(at_hour), int(at_min)))
    AlarmManager.addAlarm(server, 
        AlarmConfig(channel, at_hour, at_min, 
            country, pagesize, timezone, endpoint))
    await ctx.send(
        "Alarm set called on %s with %d.%d"%(server, int(at_hour), int(at_min)))

@commands.command()
async def alarmunset(ctx, idx):
    server = CommandManager.getGuildName(ctx)
    print("Alarm unset called on %s"%server)
    b = AlarmManager.removeAlarm(server, int(idx))
    await ctx.send("Status: %s"%b)

@commands.command()
async def alarminfo(ctx):
    server = CommandManager.getGuildName(ctx)
    l = RDM.list(server, Config.ALARMS_TABLE)
    print(l)
    await ctx.send(l)

class CommandManager(BaseCommandManager):
    bot = None
    # Every command defined above
    COMMANDS = [alarmset, alarmunset, alarminfo]
    
    @classmethod
    def initialize(cls, bot):
        super().initialize(bot)
        AlarmManager.init()
        AlarmManager.restoreAlarms()
    
    @classmethod
    def getCmdHelp(cls, cmdName):
        return "Help is not yet implemented"