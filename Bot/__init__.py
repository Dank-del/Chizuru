import logging
import os
import sys
import time
import telegram.ext as tg


StartTime = time.time()

# enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

LOGGER = logging.getLogger(__name__)

# if version < 3.6, stop bot.
if sys.version_info[0] < 3 or sys.version_info[1] < 6:
    LOGGER.error(
        "You MUST have a python version of at least 3.6! Multiple features depend on this. Bot quitting."
    )
    quit(1)
    
from Bot.config import Development as Config    
TOKEN = Config.TOKEN    
    
    
updater = tg.Updater(TOKEN, use_context=True)
dispatcher = updater.dispatcher