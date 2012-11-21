from urllib.parse import urlparse

class URLValidator:
    
    @staticmethod
    def isValidURL(link):
        link = str(link)
        parseResult = urlparse(link)
        protocols = ['http','https']
        if not parseResult.scheme in protocols:
            return False
        else:
            return True