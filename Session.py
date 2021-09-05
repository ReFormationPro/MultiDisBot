from .ReplitDatabase import ReplitDatabaseManager as RDM

class SessionManager:
    currSession = None
    
    @staticmethod
    def startSession(server, channel, session):
        """
        Adds session to server's active sessions list
        A channel can have at most 1 active session
        """
        if SessionManager.getSession(server, channel) != None:
            return False
        RDM.add(server, RDM.SESSION_TABLE, session.toDict())
        return True

    @staticmethod
    def endSession(server, channel):
        """
        Removes session from server's active sessions list
        TODO Is this an event we need to catch for updating rank etc?
        TODO Optimize
        """
        def findChannel(idx, val):
            return val["channel"] == channel
        result = RDM.find(server, RDM.SESSION_TABLE, findChannel)
        if result != None:
            RDM.remove(server, RDM.SESSION_TABLE, result[0])
            return True
        else:
            return False

    @staticmethod
    def suggestAnswer(server, channel, answer):
        """
        Returns 
        None if no active session is found
        False if answer is incorrect
        True if answer is correct
        """
        session = SessionManager.getSession(server, channel)
        if session == None:
            return None
        result = Session.compare(answer, session.answer)
        if result:
            SessionManager.endSession(server, channel)
        return result

    @staticmethod
    def getSession(server, channel):
        """
        Finds and returns the channel or None
        """
        def findChannel(idx, val):
            return val["channel"] == channel
        result = RDM.find(server, RDM.SESSION_TABLE, findChannel)
        if result != None:
            return Session.fromDict(result[1], channel)

class Session:
    answer = ""
    channel = ""
    
    def __init__(self, channel, answer):
        self.answer = Session.makeComparable(answer)
        self.channel = channel
    
    @staticmethod
    def compare(suggested, expected):
        return Session.makeComparable(suggested) == expected

    @staticmethod
    def makeComparable(answer):
        """
        Makes an answer a comparable string
        """
        return " ".join(answer.split(" ")).casefold()

    def toDict(self):
        return {"channel": self.channel, "answer": self.answer}
    
    @staticmethod
    def fromDict(dict, channel=None):
        if channel:
            return Session(channel, dict["answer"])
        return Session(dict["channel"], dict["answer"])
