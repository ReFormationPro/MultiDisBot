from Database import DatabaseManager
from replit import db

class ReplitDatabaseManager(DatabaseManager):
    """
    Uses replit db as its db
    value = db[self.serverName][tableName][key] is the way
    it is structured
    """
    
    def __init__(self, serverName):
        DatabaseManager.__init__(self, serverName)
    
    def serverExists(self):
        return db.get(self.serverName) != None
    
    def createServer(self):
        db[self.serverName] = {}
    
    def tableExists(self, tableName):
        return db[self.serverName].get(tableName) != None
    
    def createTable(self, tableName, unused=None):
        db[self.serverName][tableName] = {}
    
    def get(table, key):
        return db[self.serverName][table][key]
    
    def add(table, key, value):
        db[self.serverName][table][key] = value

    def removeAll(table, keyList):
        """
        Remove all indexes in keyList
        Returns True if successful
        """
        for k in keyList:
            del db[self.serverName][table][k]
    
    def list(table):
        return db[self.serverName][table]
    
    def count(table):
        """
        Returns the number of entries in the table
        """
        return len(db[self.serverName][table].keys())

    def getIdx(table, idx):
        """
        Returns the entry at index idx
        """
        table = db[self.serverName][table]
        key = table.keys()[idx]
        return table[key]


