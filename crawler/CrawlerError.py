class CrawlerError(RuntimeError):
    def __init__(self, args):
        self.args = args