import html
import importlib
import json
import re
import time
import traceback
from typing import Optional

from telegram import Message, Chat, User
from telegram import ParseMode, InlineKeyboardMarkup, InlineKeyboardButton, Update
from telegram.ext import (
    CommandHandler,
    Filters,
    MessageHandler,
    CallbackQueryHandler,
    CallbackContext,
)
from telegram.ext.dispatcher import run_async, DispatcherHandlerStop
from telegram.utils.helpers import escape_markdown

from Bot import (
    dispatcher,
    updater,
)

StartTime = time.time()




help_text = """
*NEKOS API* [.](https://telegra.ph/file/d59eaf89cf934fb2feeec.jpg)
 - /neko: Sends Random SFW Neko source Images.
 - /feet: Sends Random Anime Feet Images.
 - /yuri: Sends Random Yuri source Images.
 - /trap: Sends Random Trap source Images.
 - /futanari: Sends Random Futanari source Images.
 - /hololewd: Sends Random Holo Lewds.
 - /lewdkemo: Sends Random Kemo Lewds.
 - /sologif: Sends Random Solo GIFs.
 - /cumgif: Sends Random Cum GIFs.
 - /erokemo: Sends Random Ero-Kemo Images.
 - /lesbian: Sends Random Les Source Images.
 - /wallpaper: Sends Random Wallpapers.
 - /lewdk: Sends Random Kitsune Lewds.
 - /ngif: Sends Random Neko GIFs.
 - /tickle: Sends Random Tickle GIFs.
 - /lewd: Sends Random Lewds.
 - /feed: Sends Random Feeding GIFs.
 - /eroyuri: Sends Random Ero-Yuri source Images.
 - /eron: Sends Random Ero-Neko source Images.
 - /cum: Sends Random Cum Images.
 - /bjgif: Sends Random Blow Job GIFs.
 - /bj: Sends Random Blow Job source Images.
 - /nekonsfw: Sends Random NSFW Neko source Images.
 - /solo: Sends Random NSFW Neko GIFs.
 - /kemonomimi: Sends Random KemonoMimi source Images.
 - /avatarlewd: Sends Random Avater Lewd Stickers.
 - /gasm: Sends Random Orgasm Stickers.
 - /poke: Sends Random Poke GIFs.
 - /anal: Sends Random Anal GIFs.
 - /hentai: Sends Random Hentai source Images.
 - /avatar: Sends Random Avatar Stickers.
 - /erofeet: Sends Random Ero-Feet source Images.
 - /holo: Sends Random Holo source Images.
 - /tits: Sends Random Tits source Images.
 - /pussygif: Sends Random Pussy GIFs.
 - /holoero: Sends Random Ero-Holo source Images.
 - /pussy: Sends Random Pussy source Images.
 - /hentaigif: Sends Random Hentai GIFs.
 - /classic: Sends Random Classic Hentai GIFs.
 - /kuni: Sends Random Pussy Lick GIFs.
 - /waifu: Sends Random Waifu Stickers.
 - /kiss: Sends Random Kissing GIFs.
 - /femdom: Sends Random Femdom source Images.
 - /cuddle: Sends Random Cuddle GIFs.
 - /erok: Sends Random Ero-Kitsune source Images.
 - /foxgirl: Sends Random FoxGirl source Images.
 - /titsgif: Sends Random Tits GIFs.
 - /ero: Sends Random Ero source Images.
 - /smug: Sends Random Smug GIFs.
 - /baka: Sends Random Baka Shout GIFs.
 - /dva: Sends Random D.VA source Images.

 *AniList*
 - /anime: search anime
 - /character: search character
 - /manga: search manga
 - /airing: get anime airing status
 """


@run_async
def edit_msg(update, context):
    update.effective_message.delete()
    update.effective_message.reply_text(help_text, parse_mode=ParseMode.MARKDOWN)


@run_async
def help(update, context):
    if update.effective_chat.type == "private":
        args = context.args
        update.effective_message.reply_text(
            help_text,
            parse_mode=ParseMode.MARKDOWN,
            timeout=60,
            disable_web_page_preview=False,
        )
    else:
        update.effective_message.reply_text("do that in pm")


# Kanged from PaperPlane Extended userbot
def speed_convert(size):
    """
    Hi human, you can't read bytes?
    """
    power = 2 ** 10
    zero = 0
    units = {0: "", 1: "Kb/s", 2: "Mb/s", 3: "Gb/s", 4: "Tb/s"}
    while size > power:
        size /= power
        zero += 1
    return f"{round(size, 2)} {units[zero]}"


def get_readable_time(seconds: int) -> str:
    count = 0
    ping_time = ""
    time_list = []
    time_suffix_list = ["s", "m", "h", "days"]

    while count < 4:
        count += 1
        if count < 3:
            remainder, result = divmod(seconds, 60)
        else:
            remainder, result = divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)

    for x in range(len(time_list)):
        time_list[x] = str(time_list[x]) + time_suffix_list[x]
    if len(time_list) == 4:
        ping_time += time_list.pop() + ", "

    time_list.reverse()
    ping_time += ":".join(time_list)

    return ping_time


def ping(update: Update, context: CallbackContext):
    msg = update.effective_message

    start_time = time.time()
    message = msg.reply_text("Pinging...")
    end_time = time.time()
    telegram_ping = str(round((end_time - start_time) * 1000, 3)) + " ms"
    uptime = get_readable_time((time.time() - StartTime))

    message.edit_text(
        "PONG!!\n"
        "<b>Time Taken:</b> <code>{}</code>\n"
        "<b>Service uptime:</b> <code>{}</code>".format(telegram_ping, uptime),
        parse_mode=ParseMode.HTML,
    )

help_handler = CommandHandler("help", help, pass_args=True)
CALLBACK_QUERY_HANDLER = CallbackQueryHandler(edit_msg, pattern="help")
PING_HANDLER = CommandHandler("ping", ping)
dispatcher.add_handler(help_handler)
dispatcher.add_handler(CALLBACK_QUERY_HANDLER)
dispatcher.add_handler(PING_HANDLER)
