import html
import importlib
import json
import re
import traceback
from typing import Optional

from telegram import Message, Chat, User
from telegram import ParseMode, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CommandHandler, Filters, MessageHandler, CallbackQueryHandler
from telegram.ext.dispatcher import run_async, DispatcherHandlerStop
from telegram.utils.helpers import escape_markdown
from Bot import (
    dispatcher,
    updater,
    TOKEN,
    LOGGER,
)
from Bot.modules import start, anilist, lewd

from Bot import (TOKEN, LOGGER,)





LOGGER.info("Using long polling.")
updater.start_polling(timeout=15, read_latency=4)
        
updater.idle()