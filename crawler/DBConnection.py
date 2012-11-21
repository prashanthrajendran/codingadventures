
import sqlite3 as db

class DBConnection:
    
    def __init__(self,dbFile):
        self.dbcon = None
        self.dbName = dbFile
        
    def __enter__(self):
        self.dbcon = db.connect(self.dbName)
        return self.dbcon
    
    def __exit__(self, typ, value, tb):
        self.dbcon.commit()
        self.dbcon.close()
        