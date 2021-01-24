class Config(object):
    LOGGER = True
    TOKEN = ""
    DB_URI = ""
    OWNER_ID = 895373440


class Production(Config):
    LOGGER = True


class Development(Config):
    LOGGER = True
