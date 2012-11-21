from DBConnection import DBConnection

'''
DataHandler is responsible for interaction with repository
'''
class DataHandler:
    
    def __init__(self,maxLinks,dbFile,outputFile):
        self.file = outputFile #name of the file to which links should be written after all the links have been fetched
        self.maxLinks = maxLinks # maximum number of links to be fetched
        self.db = dbFile #sqllite database file
        self.prevcount = 0 #used for displaying the progress to user(i.e) number of links fetched
    '''
    saveUnprocessedLinks is used to save the links that are fetched from the url
    ''' 
    def saveUnprocessedLinks(self,links):
        with DBConnection(self.db) as conn:
            cur = conn.cursor()
            for link in links:
                if not link is None:
                    # insert or ignore statement will insert a url if it's not present in the table
                    cur.execute("INSERT OR IGNORE INTO links VALUES(?,'N')",(link.lower(),))
                    conn.commit()
                    cur.execute("select count(link) from links")
                    count = cur.fetchone()[0]
                    if count-1 > self.prevcount:
                        print('links extracted = '+str(count-1))
                        self.prevcount = count-1      
                    if self.maxLinks > 0 and count == self.maxLinks:
                        return True
        return False
    
    '''
    setAsProcessedLink is used to update the link/url as crawled link after it has been crawled  
    '''
    def setLinkAsProcessed(self,link): 
        with DBConnection(self.db) as conn:
            cur = conn.cursor()
            cur.execute("UPDATE links set processed='Y' where link = ?",(link,))
    
    '''
    saveprocessedLink used to insert the link into database that has been already crawled  
    '''
    def saveprocessedLink(self,link):
        with DBConnection(self.db) as conn:
            cur = conn.cursor()
            cur.execute("INSERT INTO links VALUES(?,'Y')",(link,))
            
    '''
    getLinkforParsing gets the next url to be crawled from the database
    '''        
    def getLinkforParsing(self):
        with DBConnection(self.db) as conn:
            cur = conn.cursor()
            cur.execute("select link from links where processed='N' limit 1")
            record = cur.fetchone()
        if not record is None:
            return record[0]
        else:
            return None
        
    '''
    exportData is used to select the url from database in batches of 100 and write to the file.
    urls are fetched in batches because if we do select all blindly it might not fit into memory if 
    there are large number of urls
    '''     
    def exportData(self):
        batch = 100
        start = 1
        file = open(self.file,'w+')
        hasdata = False
        with DBConnection(self.db) as conn:
            while True:
                cur = conn.cursor()
                query = ['select link from links limit ',str(start),',',str(batch)]
                cur.execute(''.join(query))
                records = cur.fetchall()
                if not records:
                    break
                for record in records:
                    file.write(record[0] +'\n')
                    if not hasdata: 
                        hasdata = True
                start = start + batch
        file.close()
        return hasdata
    '''
    flushTable is used to clear the existing urls in the database
    '''
    def flushTable(self):
        with DBConnection(self.db) as conn:
            cur = conn.cursor()
            cur.execute("delete from links")