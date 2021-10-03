import asyncio
import os
import requests  
from datetime import datetime, timedelta
import pytz
import traceback

import globals

from .Config import Config

class Categories:
    BUSINESS = "business"
    ENTERTAINMENT = "entertainment"
    GENERAL = "general"
    HEALTH = "health"
    SCIENCE = "science"
    SPORTS = "sports"
    TECHNOLOGY = "technology"
    
    @staticmethod
    def isValidCategory(category):
        """
        No category is valid
        """
        valid = ["", "business","entertainment","general",
                "health","science","sports","technology"]
        return category in valid


class AlarmConfig:
    endpoint = None
    country = None
    timezone = None
    at_hour = None
    at_min = None
    channel = None
    pagesize = None
    filter = None
    query = None
    FIELDS = ["endpoint", "country", "timezone", 
                "at_hour", "at_min", "channel", "pagesize", 
                "filter", "query"]

    def __init__(self, channel, at_hour=12, at_min=0,
                country="tr",
                query="",
                filter="",
                pagesize=1,
                timezone="Europe/Istanbul", 
                endpoint="https://newsapi.org/v2/top-headlines"):
        """
        Hour is in 24 hours format
        Timezone is a pytz timezone name
        filter is either a comma separated list of sources
        or a category.
        If filter is empty, no filter.
        
        For sources check command "sources".

        Valid categories: 
        business, entertainment, general, health, science, sports, technology
        """
        self.channel = channel
        self.at_hour = at_hour
        self.at_min = at_min
        self.timezone = timezone
        self.endpoint = endpoint
        self.country = country
        self.pagesize = pagesize
        self.filter = filter
        self.query = query
    
    def __eq__(self, other):
        for f in AlarmConfig.FIELDS:
            if self.__getattribute__(f) != other.__getattribute__(f):
                return False
        return True

    @staticmethod
    def fromDict(alarmConfigDict):
        return AlarmConfig(alarmConfigDict["channel"],
            alarmConfigDict["at_hour"],
            alarmConfigDict["at_min"],
            alarmConfigDict["country"],
            alarmConfigDict["query"],
            alarmConfigDict["filter"],
            alarmConfigDict["pagesize"],
            alarmConfigDict["timezone"],
            alarmConfigDict["endpoint"])
    
    @staticmethod
    def makeDict(channel, at_hour: int, at_min: int,
                country='tr', query="", filter="",
                pagesize: int = 1,
                timezone='Europe/Istanbul', 
                endpoint='https://newsapi.org/v2/top-headlines'):
        d = {"channel": channel,
                "at_hour": at_hour,
                "at_min": at_min,
                "country": country,
                "query": query,
                "filter": filter,
                "pagesize": pagesize,
                "timezone": timezone,
                "endpoint": endpoint}
        return d

    def toDict(self):
        return AlarmConfig.makeDict(self.channel, self.at_hour, self.at_min,
                                    self.country, self.query, self.filter,
                                    self.pagesize, self.timezone,
                                    self.endpoint)
    


class News:
    """
    Uses environment variable NEWS_API_KEY to use
    newsapi
    """
    @staticmethod
    def getHeadlines(endpoint, country, query, filter, pagesize: int):
        params = {
            "apiKey": os.getenv('NEWS_API_KEY'),
            "country": country,
            "pageSize": pagesize
        }
        if query != "":
            params["q"] = query
        if filter != "":
            # Filter is either a category or list of sources
            if Categories.isValidCategory(filter):
                params["category"] = filter
            else:
                params["sources"] = filter
                # Sources cannot be used with country
                del params["country"]
        print("[DEBUG] ", params)
        resp = requests.get(endpoint, params)
        if resp.status_code != 200:
            print("Error at getting headlines. Status code %s"
                %resp.status_code)
            return None
        headlines = resp.json()
        if headlines == None or len(headlines["articles"]) == 0:
            return None
        return headlines
    
    @staticmethod
    def getSources(category, language, country):
        params = {
            "apiKey": os.getenv('NEWS_API_KEY'),
            "category": category,
            "language": language,
            "country": country
        }
        resp = requests.get("https://newsapi.org/v2/sources", params)
        if resp.status_code != 200:
            print("Error at getting sources. Status code %s"
                %resp.status_code)
            return None
        sources = resp.json()
        if sources == None or len(sources["sources"]) == 0:
            return None
        return sources["sources"]

    @staticmethod
    def prettifySource(source):
        try:
            sourceBuilder = Config.localeManager.get("NewsPrettifySource")
            sourceBuilder = sourceBuilder%(
                source["category"], source["name"],
                source["id"], source["url"])
            return sourceBuilder
        except Exception as ex:
            traceback.print_exception(type(ex), ex, ex.__traceback__)
            return None

    @staticmethod
    def calculateSecondsTillAlarm(alarm_hour: int, alarm_min: int, timezone):
        """
        Creates alarm for next HOUR.MIN in given timezone
        """
        tz = pytz.timezone(timezone)
        dt = datetime.now(pytz.utc).astimezone(tz)
        # Create alarm time for today
        alarm = tz.localize(datetime(dt.year, dt.month, dt.day,
            alarm_hour, alarm_min, 0, 0))
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
            source = Config.localeManager.get("NewsPrettifyHeadline")
            s += source%headlines["articles"][0]["source"]["name"]
            print("[DEBUG]", headlines["articles"][0]["source"])
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
    def getHeadlinesForPosting(country, query, 
            filter, pagesize, endpoint):
        headlines = News.getHeadlines(endpoint, 
                        country, query,
                        filter, pagesize)
        if headlines != None:
            news = News.prettifyHeadlines(headlines)
            if news == None:
                resp = Config.localeManager.get("NewsPrettifyError")
                return resp
            else:
                return news
        else:
            # Send error message
            # TODO Raise an exception here instead so that
            # the caller can decide to retry or not
            resp = Config.localeManager.get("NewsRetrieveError")
            return resp

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
                resp = News.getHeadlinesForPosting(alarmConfig.country, 
                    alarmConfig.query, alarmConfig.filter, 
                    alarmConfig.pagesize, alarmConfig.endpoint)
                await ch.send(resp)
        except Exception as ex:
            traceback.print_exception(type(ex), ex, ex.__traceback__)
