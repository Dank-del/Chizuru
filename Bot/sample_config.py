class Config(object):
    LOGGER = True
    TOKEN = ""
    MONGO_URI = ""


class Production(Config):
    LOGGER = True


class Development(Config):
    LOGGER = True
