
class Error(Exception):
    pass

class DESBlockError(Error):
    def __init__(self , message):
        self.message = message

class EncryptionError(Error):
    def __init__(self, message):
        self.message = message

class DecryptionError(Error):
    def __init__(self , message):
        self.message = message

class DESError(Error):
    def __init__(self, message):
        self.message = message
