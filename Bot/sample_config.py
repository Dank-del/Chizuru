class Config(object):
    LOGGER = True
    TOKEN = ""
    
    
class Production(Config):
    LOGGER = True


class Development(Config):
    LOGGER = True