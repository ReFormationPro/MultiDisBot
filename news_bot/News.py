import asyncio
import os
import requests  
from datetime import datetime, timedelta
import pytz
import traceback

import globals

from .Config import Config

class AlarmConfig:
    endpoint = None
    country = None
    timezone = None
    at_hour = None
    at_min = None
    channel = None
    pagesize = None
    def __init__(self, channel, at_hour=12, at_min=0,
                country='tr', pagesize=1,
                timezone='Europe/Istanbul', 
                endpoint='https://newsapi.org/v2/top-headlines'):
        """
        Hour is in 24 hours format
        Timezone is a pytz timezone name
        """
        self.channel = channel
        self.at_hour = at_hour
        self.at_min = at_min
        self.timezone = timezone
        self.endpoint = endpoint
        self.country = country
        self.pagesize = 1
    
    def __eq__(self, other):
        return  self.channel == other.channel and \
                self.at_hour == other.at_hour and \
                self.at_min == other.at_min and \
                self.timezone == other.timezone and \
                self.endpoint == other.endpoint and \
                self.country == other.country and \
                self.pagesize == other.pagesize

    @staticmethod
    def fromDict(alarmConfigDict):
        return AlarmConfig(alarmConfigDict["channel"],
            alarmConfigDict["at_hour"],
            alarmConfigDict["at_min"],
            alarmConfigDict["country"],
            alarmConfigDict["pagesize"],
            alarmConfigDict["timezone"],
            alarmConfigDict["endpoint"])
    
    @staticmethod
    def makeDict(channel, at_hour=12, at_min=0,
                country='tr', pagesize=1,
                timezone='Europe/Istanbul', 
                endpoint='https://newsapi.org/v2/top-headlines'):
        d = {"channel": channel,
                "at_hour": int(at_hour),
                "at_min": int(at_min),
                "country": country,
                "pagesize": int(pagesize),
                "timezone": timezone,
                "endpoint": endpoint}
        return d

    def toDict(self):
        return AlarmConfig.makeDict(self.channel, self.at_hour, self.at_min,
                                    self.country, self.pagesize, self.timezone,
                                    self.endpoint)
    


class News:
    """
    Uses environment variable NEWS_API_KEY to use
    newsapi
    """
    @staticmethod
    def getHeadlines(endpoint, country, pagesize):
        resp = requests.get(endpoint, params={
            "apiKey": os.getenv('NEWS_API_KEY'),
            "country": country,
            "pageSize": pagesize
        })
        if resp.status_code != 200:
            print("Error at getting headlines. Status code %s"
                %resp.status_code)
            return None
        headlines = resp.json()
        if headlines == None or len(headlines["articles"]) == 0:
            return None
        return headlines
    
    @staticmethod
    def calculateSecondsTillAlarm(alarm_hour, alarm_min, timezone):
        """
        Creates alarm for next HOUR.MIN in given timezone
        """
        tz = pytz.timezone(timezone)
        dt = datetime.now(pytz.utc).astimezone(tz)
        # Create alarm time for today
        alarm = datetime(dt.year, dt.month, dt.day,
            alarm_hour, alarm_min, 0, 0).astimezone(tz)
        delta = alarm - dt
        if delta != abs(delta): # If negative
            # Alarm of today has passed, set for tomorrow
            alarm = alarm + timedelta(days=1)
            delta = alarm - dt
        return delta

    @staticmethod
    def findChannel(channel):
        ch = None
        for c in globals.bot.guilds[0].channels:
            if c.name == channel:
                ch = c
                break
        else:
            return None
        return ch
        
    @staticmethod
    def prettifyHeadlines(headlines):
        try:
            s = ""
            # Source
            source = Config.localeManager.get("NewsPrettifySource")
            s += source%headlines["articles"][0]["source"]["name"]
            # Title
            s += "**%s**\n"%headlines["articles"][0]["title"]
            # Description
            s += headlines["articles"][0]["description"] + "\n"
            # URL
            s += headlines["articles"][0]["url"] + "\n"
            return s
        except Exception as ex:
            traceback.print_exception(type(ex), ex, ex.__traceback__)
            return None

    @staticmethod
    async def sendNews(alarmConfig):
        try:
            while True:
                delta = News.calculateSecondsTillAlarm(alarmConfig.at_hour,
                            alarmConfig.at_min, alarmConfig.timezone)
                # Sleep till alarm
                secs = delta.total_seconds()
                print("[DEBUG] sendNews task is sleeping for %d hour(s) %d minute(s) %d second(s)"%
                    (int(secs/60/60), int((secs/60))%60, int(secs%60)))
                await asyncio.sleep(delta.total_seconds())
                # Wake up and do the task
                ch = News.findChannel(alarmConfig.channel)
                if ch == None:
                    # TODO Message admin?
                    print("Channel %s not found!"%alarmConfig.channel)
                    continue
                headlines = News.getHeadlines(alarmConfig.endpoint, 
                                alarmConfig.country, alarmConfig.pagesize)
                if headlines != None:
                    news = News.prettifyHeadlines(headlines)
                    if news == None:
                        resp = Config.localeManager.get("NewsPrettifyError")
                        await ch.send(resp)
                    else:
                        await ch.send(news)
                else:
                    # Send error message
                    resp = Config.localeManager.get("NewsRetrieveError")
                    await ch.send(resp)
                    # NOTE Retry in 10 minutes maybe?
        except Exception as ex:
            traceback.print_exception(type(ex), ex, ex.__traceback__)
