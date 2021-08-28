

class SessionManager:
    currSession = None
    
    @staticmethod
    def startSession(session):
        SessionManager.currSession = session

    @staticmethod
    def endSession():
        """
        TODO Is this an event we need to catch for updating rank etc?
        """
        SessionManager.currSession = None

    @staticmethod
    def suggestAnswer(answer):
        return SessionManager.currSession.suggestAnswer(answer)

class Session:
    answer = ""
    
    def __init__(self, answer):
        self.answer = Session.makeComparable(answer)
    
    def suggestAnswer(self, answer):
        if self.answer == answer:
            # Correct answer, end session
            self.endSession()
            return True
        return False
    
    def endSession(self):
        SessionManager.endSession()
    
    @staticmethod
    def makeComparable(answer):
        """
        Makes an answer a comparable string
        """
        return " ".join(answer.split(" ")).casefold()


