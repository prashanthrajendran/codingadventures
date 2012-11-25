from urllib.parse import urljoin

class URLValidator:
    
    @staticmethod
    def isValidURL(link):
        link = str(link)
        if link.startswith('http') or link.startswith('https'):
            return True
        else:
            return False 
        
    @staticmethod
    def isValidSubUrl(link):
        if link.startswith('#'):
            return False
        else:
            return True
    
    @staticmethod
    def formValidURL(link,sublink):
        if not URLValidator.isValidSubUrl(sublink):
            return None
        else:
            return urljoin(link,sublink)    
            
        