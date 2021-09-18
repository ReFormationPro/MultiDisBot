import asyncio

from database.ReplitDatabase import ReplitDatabaseManager as RDM

from .Config import Config
from .News import AlarmConfig, News

class Task:
    promise = None
    alarmConfig = None
    server = None
    result = None

    def __init__(self, server, alarmConfig):
        self.promise = News.sendNews(alarmConfig)
        self.server = server
        self.alarmConfig = alarmConfig
    
    def run(self, loop):
        print ("Running a task for %d.%d on '%s' channel"%
            (self.alarmConfig.at_hour,
            self.alarmConfig.at_min,
            self.alarmConfig.channel))
        self.result = asyncio.run_coroutine_threadsafe(self.promise, loop)

    def cancel(self):
        return self.promise.cancel()


class AlarmManager:
    runningTasks = []
    loop = None

    @staticmethod
    def init():
        AlarmManager.loop = asyncio.get_event_loop()

    @staticmethod
    def __runAlarm(server, alarmConfig):
        """
        Creates and runs an alarm task
        """
        # Create a task for this
        task = Task(server, alarmConfig)
        AlarmManager.runningTasks.append(task)
        task.run(AlarmManager.loop)
        return task

    @staticmethod
    def addAlarm(server, alarmConfig):
        """
        Creates and runs an alarm task and
        stores the alarms in the database

        alarmConfig cannot be a dict!
        """
        AlarmManager.__runAlarm(server, alarmConfig)
        RDM.add(server, Config.ALARMS_TABLE, alarmConfig.toDict())
    
    @staticmethod
    def removeAlarm(server, idx):
        """
        Cancels alarm task at index and removes it from
        the alarms table.
        Return True if task is cancelled
        """
        alarmConfig = RDM.getAtIdx(server, Config.ALARMS_TABLE, idx)
        if alarmConfig == None:
            print ("Alarm is NOT found in db")
            return False
        # TODO Make comparisons without creating AlarmConfig objects?
        alarmConfig = AlarmConfig.fromDict(alarmConfig)
        print ("Alarm is found in db")
        RDM.remove(server, Config.ALARMS_TABLE, idx)
        # TODO Use a lock before erasing?
        for t in AlarmManager.runningTasks:
            # TODO
            print ("Ours", server, alarmConfig)
            print ("Other", t.server, t.alarmConfig)
            if t.server == server and t.alarmConfig == alarmConfig:
                t.cancel()
                AlarmManager.runningTasks.remove(t)
                return True
        return False
    
    @staticmethod
    def restoreAlarms():
        """
        Lists alarms from database and creates tasks for each.
        Then the tasks are run.
        """
        for server in RDM.listServers():
            for alarm in RDM.list(server, Config.ALARMS_TABLE):
                alarmConfig = AlarmConfig.fromDict(alarm)
                AlarmManager.__runAlarm(server, alarmConfig)