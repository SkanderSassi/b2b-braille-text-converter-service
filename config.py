import os
from attr import attrs
from dotenv import load_dotenv



class Config():
    def __init__(self):
        
        self.API_KEY = os.environ['API_KEY']
        self.HOST_IP = os.environ['HOST_IP']
        self.PORT = os.environ['PORT']
        self.ALLOWED_TYPES = set(os.environ['ALLOWED_TYPES'].split(','))
        self.SAVE_DIR = os.environ['SAVE_DIR']
        self.ALLOWED_CONVERSIONS = set(os.environ['ALLOWED_CONVERSIONS'].split(','))
    def __repr__(self) -> str:
        attrs = vars(self)
        return ', '.join("%s: %s" % item for item in attrs.items())
class DevelopmentConfig(Config):
    def __init__(self):
        Config.__init__(self)
        self.DEBUG = True
        
class ProductionConfig(Config):
    def __init__(self):
        Config.__init__(self)
        self.DEBUG = False
    

def load_config() -> Config:
    load_dotenv()
    env = os.environ['FLASK_ENV']
    if env == 'production':
        return ProductionConfig()
    return DevelopmentConfig()

config = load_config()