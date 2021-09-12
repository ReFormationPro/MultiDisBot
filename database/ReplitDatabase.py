"""
db[server]["Questions"][i] = {"text": "", "answer": ""}
"""

from replit import db

from .Database import DatabaseManager

class ReplitDatabaseManager(DatabaseManager):
    """
    Uses replit db as its db
    value = db[server][tableName][key] is the way
    it is structured
    """
    
    @staticmethod
    def serverExists(server):
        return db.get(server) != None
    
    @staticmethod
    def createServer(server):
        db[server] = {}
    
    @staticmethod
    def deleteServer(server):
        del db[server]
    
    @staticmethod
    def tableExists(server, tableName):
        return db[server].get(tableName) != None
    
    @staticmethod
    def createTable(server, tableName, unused=None):
        db[server][tableName] = []
    
    @staticmethod
    def getAtIdx(server, table, idx):
        """
        Returns the entry at index idx
        """
        return db[server][table][idx]
    
    @staticmethod
    def getIdxOf(server, table, value):
        """
        Returns the entry at index idx
        """
        try:
            return db[server][table].index(value)
        except:
            return None
    
    @staticmethod
    def find(server, table, func):
        """
        Finds the first entry in the table
        accepted by func

        func takes index value pairs

        Returns index value pair of the entry
        or None
        """
        table = db[server][table]
        for idx, val in enumerate(table):
            if func(idx, val):
                return (idx, val)
    
    @staticmethod
    def add(server, table, value):
        """
        Appends value to the table
        """
        db[server][table].append(value)

    @staticmethod
    def remove(server, table, idx):
        """
        Removes idx from the table
        """
        del db[server][table][idx]

    @staticmethod
    def removeAll(server, table, idxList):
        """
        Remove all indexes in idxList
        Returns True if successful
        """
        # As erasing from a list
        idxList = sorted(idxList, reverse=True)
        for idx in idxList:
            del db[server][table][idx]
    
    @staticmethod
    def list(server, table):
        return db[server][table]
    
    @staticmethod
    def count(server, table):
        """
        Returns the number of entries in the table
        """
        return len(db[server][table])

