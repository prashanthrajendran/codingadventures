import sqlite3
import sys
from LinkExtracter import LinkExtracter
from DataHandler import DataHandler
from CrawlerError import CrawlerError
from CrawlerLogger import CrawlerLogger

'''
Crawler is the main class which coordinates between LinkExtracter and DataHandler for parsing the links 
and persisting them in the repository
'''

class Crawler:
    
    def __init__(self,url,dbFile,outputFile,maxCount=None):
        self.url = url # url to be crawled
        if maxCount == None:
            self.maxCount = -1
        else:
            '''
            maxcount is the maximum number of links to be fetched by the crawler.
            It is incremented as we should accommodate the initial user input while 
            counting the total number of links in the repository as the link entered by the user
            will also be persisted in the repository
            (i.e)if user requests to crawl python.org and asks to fetch 2 links , the program should 
            terminate when there are 3 links in repository as python.org is also one of the links in repository   
            '''
            self.maxCount = maxCount + 1
            
        self.extracter = LinkExtracter()
        self.dataHandler = DataHandler(self.maxCount,dbFile,outputFile)
        self.log = CrawlerLogger.getlogger()
    '''
    crawls the link given by the user using BFS traversal until it fetches the specified number of links or 
    till all the links have been fetched
    '''
    def Crawl(self):
 
        try:
            link = self.url
            self.log.info("crawling "+link)
            links = self.extracter.fetchLinks(link)
            
            if links is None:
                print("Either the url you entered cannot be crawled  or its does not contain any links")
                return False
        
            self.dataHandler.flushTable()
            maxLinkflag = self.dataHandler.saveUnprocessedLinks(links)
         
            if maxLinkflag:
                return self.writeDataToFile()
            else:
                self.crawlfetchedLinks()
                return self.writeDataToFile()
        except sqlite3.OperationalError as e:
            self.log.error(e,exc_info=sys.exc_info()[2]);
            raise CrawlerError(('Either invalid database entered or database does not have necessary tables',))
    
    '''
    Helper for crawl function
    '''
    def crawlfetchedLinks(self):
        
        maxLinkflag = True
        
        '''
        This loop will terminate when the specified number of links has been fetched or all the links 
        has been fetched
        ''' 
        while True:
            link = self.dataHandler.getLinkforParsing()
            if link is None:
                break
            links = self.extracter.fetchLinks(link)
            self.dataHandler.setLinkAsProcessed(link)
            if not links is None:
                maxLinkflag = self.dataHandler.saveUnprocessedLinks(links)
            if maxLinkflag:
                break
            
    '''
    writeDataToFile helps in writing the fetched links to file (links.txt) so that user can use it
    '''
    def writeDataToFile(self):
        try:
            res = self.dataHandler.exportData()
            self.dataHandler.flushTable()
            return res
        except IOError as e:
            self.log.error(e,exc_info=sys.exc_info()[2]);
            raise CrawlerError(('The path of the export file entered is invalid',))
    