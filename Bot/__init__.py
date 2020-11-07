from Bot.config import Development as Config
import logging
import sys
import telegram.ext as tg
import pymongo
import time

StartTime = time.time()

# enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

LOGGER = logging.getLogger(__name__)
LOGGER.info("Chizuru is now online, you perv.")

# if version < 3.6, stop bot.
if sys.version_info[0] < 3 or sys.version_info[1] < 6:
    LOGGER.error(
        "You MUST have a python version of at least 3.6! Multiple features depend on this. Bot quitting."
    )
    quit(1)

TOKEN = Config.TOKEN
MONGO_CLIENT = pymongo.MongoClient(Config.MONGO_URI)

updater = tg.Updater(TOKEN, use_context=True)
dispatcher = updater.dispatcher
