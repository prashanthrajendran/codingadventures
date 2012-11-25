import sys
import urllib
from lxml.html import parse
from urllib.request import urlopen
from URLValidator import URLValidator
from CrawlerLogger import CrawlerLogger

'''
LinkExtracter is responsible for parsing the web page and extracting the urls
'''
class LinkExtracter:
    
    def __init__(self):
        self.log = CrawlerLogger.getlogger()
        
    def fetchLinks(self,url):
        dom = None
        try:
            response = urlopen(url)
            contenttype = response.info()['Content-Type']
            contenttype = contenttype.strip().lower()
            '''
            if the conten-type is not text/html the url is rejected as it could be images or something else
            that could not be parsed 
            '''
            if not contenttype.startswith('text/html'):
                self.log.debug('rejected = '+url+' Content-Type = '+contenttype)
                return
            dom = parse(response).getroot()
        except urllib.error.HTTPError as e1:
            self.log.warn(''.join(['HTTP error for ',url]))
            self.log.debug(e1,exc_info=sys.exc_info()[2]) 
            return
        except Exception as  e2:
            self.log.warn('cannot parse '+url)
            self.log.debug(e2,exc_info=sys.exc_info()[2]) 
            return
        if not dom is None:
            links = dom.cssselect('a')
            if not links is None:
                linksList = []
                for link in links:
                    if not link is None: 
                        href = link.get('href')
                        if href is None:
                            continue
                        suburl = URLValidator.formValidURL(url,href)
                        if not suburl is None:
                            linksList.append(suburl)
                        else:
                            self.log.debug('rejected href = '+href)
                if not linksList:
                    return None
                else:
                    return linksList