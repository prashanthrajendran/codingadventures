import logging.config

class CrawlerLogger:
    
    @staticmethod
    def init():
        logging.config.fileConfig('logger.config')
    
    @staticmethod
    def getlogger():
        return logging.getLogger('crawler')