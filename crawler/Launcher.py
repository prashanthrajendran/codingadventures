'''
 Launcher is responsible for getting inputs from the user and launching the crawler
'''

import sys
import webbrowser
import signal
import os
from Crawler import Crawler 
from CrawlerError import CrawlerError
from CrawlerLogger import CrawlerLogger
from URLValidator import URLValidator

crawler = None
lock = 'lock.txt' #lock for avoiding multiple executions in parallel

def removelock():
    try:
        if os.path.isfile(lock):
            os.remove(lock)
    except:
        return

def signal_handler(signal, frame):
    print('preparing to terminate')
    if not crawler is None:
        if crawler.writeDataToFile():
            webbrowser.open("links.txt")
    removelock()
    sys.exit()
    
if __name__ == '__main__':
    
    if os.path.isfile(lock):
        print('A process of crawler is already running . Multiprocessing is not supported')
        sys.exit()
    else:
        try:
            f = open(lock,'w+')
            f.close()
        except:
            pass #even if lock file cannot be created proceed with the rest of the code
    log = None
    url = None
    maxlinks = None
    cmdlength = len(sys.argv)
    if cmdlength < 2 :
        print("Please enter url to crawl and the maximum number of links to be extracted which is an optional one")
        print("Eg 1: python Main.py http://python.org 50")
        print("Eg 2: python Main.py http://python.org")
        sys.exit()
    elif cmdlength == 2 or cmdlength == 3:
        url = str(sys.argv[1])
        if not URLValidator.isValidURL(url):
            print("Either your url is not valid or a format that cannot be crawled")
            sys.exit()
        if cmdlength == 3:
            try:
                maxlinks = int(sys.argv[2])
            except ValueError:
                print('Invalid maximum links')
                sys.exit()
            if maxlinks < 1:
                print("maximum links should be minimum 1")
                sys.exit()
    else:
        print("Invalid number of arguments")
        sys.exit()
    try:
        signal.signal(signal.SIGINT, signal_handler)
        CrawlerLogger.init()
        log = CrawlerLogger.getlogger()
        if not url[len(url)-1] == '/':
            url = url + '/'
        crawler = Crawler(url,'crawler.db','links.txt',maxlinks)
        print('Crawling ....')
        res = crawler.Crawl()
        if res:
            webbrowser.open("links.txt")
        
    except CrawlerError as ce:
        print(ce)
        
    except Exception as e:
        if not log is None:
            log.error(e,exc_info=sys.exc_info()[2])
            print("Unexpected error occurred. Check log file for details")
        else:
            print("Unexpected error occurred")
            
    removelock()
