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
    at_hour, at_min, pagesize  = int(at_hour), int(at_min), int(pagesize)
    server = CommandManager.getGuildName(ctx)
    print("Alarm set is called on %s with %d.%d"%(server, at_hour, at_min))
    AlarmManager.addAlarm(server, 
        AlarmConfig(channel, at_hour, at_min, 
            country, pagesize, timezone, endpoint))
    resp = Config.localeManager.get("AlarmSetResponse")
    await ctx.send(resp%(at_hour, at_min, channel))

@commands.command()
async def alarmunset(ctx, idx):
    # TODO Accept multiple indexes
    idx = int(idx)
    server = CommandManager.getGuildName(ctx)
    print("Alarm unset called on %s"%server)
    # NOTE We do this once more in removeAlarm
    alarmConfig = RDM.getAtIdx(server, Config.ALARMS_TABLE, idx)
    b = AlarmManager.removeAlarm(server, int(idx))
    if b:
        resp = Config.localeManager.get("AlarmUnsetResponseSuccess")%()
        resp = resp%(int(alarmConfig["at_hour"]), 
                    int(alarmConfig["at_min"]), 
                    alarmConfig["channel"])
    else:
        resp = Config.localeManager.get("AlarmUnsetResponseFail")
    await ctx.send(resp)

@commands.command()
async def alarminfo(ctx):
    server = CommandManager.getGuildName(ctx)
    l = RDM.list(server, Config.ALARMS_TABLE)
    resp = Config.localeManager.get("AlarminfoBegin")
    item = Config.localeManager.get("AlarminfoItem")
    for idx, alarm in enumerate(l):
        h, m, c = int(alarm["at_hour"]), int(alarm["at_min"]), alarm["channel"]
        resp += item%(idx, h, m, c)
    resp += Config.localeManager.get("AlarminfoEnd")
    await ctx.send(resp)

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