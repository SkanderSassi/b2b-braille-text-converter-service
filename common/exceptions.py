


class EmptyFileName(Exception):
    """Still an exception raised when uncommon things happen"""
    def __init__(self, message, payload=None):
        self.message = message
        self.payload = payload 
    def __str__(self):
        return str(self.message) 
    
class FileTypeNotAllowed(Exception):
    def __init__(self, message, payload=None):
        self.message = message
        self.payload = payload
    def __str__(self):
        return str(self.message) 
    
class TranslationTableNotFound(Exception):
    def __init__(self, message, payload=None):
        self.message = message
        self.payload = payload
    def __str__(self):
        return str(self.message) 