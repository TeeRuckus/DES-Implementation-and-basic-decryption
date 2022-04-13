
class Error(Exception):
    pass

class DESBlockError(Error):
    def __init__(self , message):
        self.message = message

