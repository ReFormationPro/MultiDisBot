from discord.ext import commands

from common.BaseCommandManager import BaseCommandManager
from database.ReplitDatabase import ReplitDatabaseManager as RDM

from .News import AlarmConfig, News
from .Config import Config
from .Alarm import AlarmManager

@commands.command()
async def sendnews(ctx, country='tr', query="", filter="", 
                pagesize: int=1,
                endpoint='https://newsapi.org/v2/top-headlines'):
    """
    Same as alarmset but for posting an alarm immediately for one time.
    
    Sends an alarm from "country", having keyword "query" in it.

    Filter can be either a category or a comma separated list of sources.
    To list sources run command $sources.

    Valid categories are:
    business, entertainment, general, health, 
    science, sports, technology 

    You will probably not change the endpoint.
    """
    print("[DEBUG] '%s' '%s' '%s' '%d' '%s'"%(country, query, filter, 
        pagesize, endpoint))
    resp = News.getHeadlinesForPosting(country, query, filter, 
        pagesize, endpoint)
    await ctx.send(resp)

@commands.command()
async def sources(ctx, category="", language="", country=""):
    """
    Lists sources.
    """
    srcs = News.getSources(category, language, country)
    if srcs == None:
        resp = Config.localeManager.get("NewsPrettifySourceRetrieveError")
        await ctx.send(resp)
        return
    resp = Config.localeManager.get("NewsPrettifySourceBegin")
    # Send 5 source at once
    for i, s in enumerate(srcs):
        resp += News.prettifySource(s) + "\n"
        if i % 5 == 0:
            # Send and clear response
            await ctx.send(resp)
            resp = ""
    if resp != "":
        await ctx.send(resp)

@commands.command()
async def alarmset(ctx, channel, at_hour: int, at_min: int,
                country='tr', query="", filter="", pagesize: int=1,
                timezone='Europe/Istanbul', 
                endpoint='https://newsapi.org/v2/top-headlines'):
    """
    Sets an alarm for news-posting on "channel", "at_hour"."at_min",
    where news are from "country" and "pagesize" many news at once.
    
    Query is for keyword search.

    Filter is either a comma separated list of sources
    or a single category.
    For the list of sources, see sources command.

    Possible categories are:
    business, entertainment, general, health, 
    science, sports, technology 

    You will probably not change the "endpoint".
    """
    server = CommandManager.getGuildName(ctx)
    print("Alarm set is called on %s with %d.%d"%(server, at_hour, at_min))
    AlarmManager.addAlarm(server, 
        AlarmConfig(channel, at_hour, at_min, 
            country, query, filter,
            pagesize, timezone, endpoint))
    resp = Config.localeManager.get("AlarmSetResponse")
    await ctx.send(resp%(at_hour, at_min, channel))

@commands.command()
async def alarmunset(ctx, idx: int):
    # TODO Accept multiple indexes
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
    COMMANDS = [sendnews, sources, alarmset, alarmunset, alarminfo]
    
    @classmethod
    def initialize(cls, bot):
        super().initialize(bot)
        AlarmManager.init()
        AlarmManager.restoreAlarms()
    
    @classmethod
    def getCmdHelp(cls, cmdName):
        return "Help is not yet implemented"