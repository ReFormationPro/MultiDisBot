
class DatabaseManager:
    """
    Manages the database of a server
    
    At each instance check if serverExists, if not, createServer
    and then call createTable for each of your tables.
    
    """
    serverName = ""
    
    def __init__(self, serverName):
        self.serverName = serverName
    
    def serverExists(self):
        pass
    
    def createServer(self):
        pass
    
    def tableExists(self, tableName):
        pass
    
    def createTable(self, tableName, tableProperties):
        pass
    
    def get(table, key):
        pass
    
    def add(table, key, value):
        pass

    def removeAll(table, keyList):
        """
        Remove all indexes in keyList
        Returns True if successful
        """
        pass
    
    def list(table):
        pass
    
    def count(table):
        """
        Returns the number of entries in the table
        """
        pass

    def getIdx(table, idx):
        """
        Returns the entry at index idx
        """
        pass



