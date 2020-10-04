import requests
import nekos
from PIL import Image
import os
from typing import NamedTuple, Optional

from telegram import Message, Chat, Update, Bot, MessageEntity
from telegram import ParseMode
from telegram.ext import CommandHandler, run_async

from Bot import dispatcher, updater


def is_user_in_chat(chat: Chat, user_id: int) -> bool:
    member = chat.get_member(user_id)
    return member.status not in ("left", "kicked")


class Lewd(NamedTuple):
    target: str
    command: Optional[str] = None
    is_video: bool = False


lewds = [
    Lewd('neko'),
    Lewd('feet'),
    Lewd('yuri'),
    Lewd('trap'),
    Lewd('futanari'),
    Lewd('hololewd'),
    Lewd('lewdkemo'),
    Lewd('solog', command="sologif", is_video=True),
    Lewd('feetg', command="feetgif", is_video=True),
    Lewd('cum', command="cumgif", is_video=True),
    Lewd('erokemo'),
    Lewd('erokemo'),
    Lewd('les', command="lesbian", is_video=True),
    Lewd('wallpaper'),
    Lewd('lewdk'),
    Lewd('ngif', is_video=True),
    Lewd('tickle', is_video=True),
    Lewd('lewd'),
    Lewd('feed', is_video=True),
    Lewd('eroyuri'),
    Lewd("eron"),
    Lewd("cum_jpg", command="cum"),
    Lewd("bj", command="bjgif", is_video=True),
    Lewd("blowjob", command="bj"),
    Lewd("nsfw_neko_gif", command="nekonsfw", is_video=True),
    Lewd("solo"),
    Lewd("kemonomimi"),
    Lewd("poke", is_video=True),
    Lewd("anal", is_video=True),
    Lewd("hentai"),
    Lewd("erofeet"),
    Lewd("holo"),
    Lewd("pussy", command="pussygif", is_video=True),
    Lewd("tits"),
    Lewd("holoero"),
    Lewd("pussy_jpg", command="pussy"),
    Lewd("random_hentai_gif", command="hentaigif", is_video=True),
    Lewd("classic", is_video=True),
    Lewd("kuni", is_video=True),
    Lewd("kiss", is_video=True),
    Lewd("femdom"),
    Lewd("cuddle", is_video=True),
    Lewd("erok"),
    Lewd("fox_girl", command="foxgirl"),
    Lewd("boobs", command="titsgif", is_video=True),
    Lewd("ero"),
    Lewd("smug", is_video=True),
    Lewd("baka", is_video=True),
]

__handlers__ = []
for lewd in lewds:
    @run_async
    def callback(update, context):
        msg = update.effective_message
        if lewd.is_video:
            msg.reply_video(nekos.img(lewd.target))
        else:
            msg.reply_photo(nekos.img(lewd.target))

    command = lewd.command or lewd.target
    handler = CommandHandler(command, callback)
    dispatcher.add_handler(handler)
    __handlers__.append(handler)


@run_async
def avatarlewd(update, context):
    msg = update.effective_message
    target = "nsfw_avatar"
    with open("temp.png", "wb") as f:
        f.write(requests.get(nekos.img(target)).content)
    img = Image.open("temp.png")
    img.save("temp.webp", "webp")
    msg.reply_document(open("temp.webp", "rb"))
    os.remove("temp.webp")


@run_async
def gasm(update, context):
    msg = update.effective_message
    target = "gasm"
    with open("temp.png", "wb") as f:
        f.write(requests.get(nekos.img(target)).content)
    img = Image.open("temp.png")
    img.save("temp.webp", "webp")
    msg.reply_document(open("temp.webp", "rb"))
    os.remove("temp.webp")


@run_async
def avatar(update, context):
    msg = update.effective_message
    target = "nsfw_avatar"
    with open("temp.png", "wb") as f:
        f.write(requests.get(nekos.img(target)).content)
    img = Image.open("temp.png")
    img.save("temp.webp", "webp")
    msg.reply_document(open("temp.webp", "rb"))
    os.remove("temp.webp")


@run_async
def waifu(update, context):
    msg = update.effective_message
    target = "waifu"
    with open("temp.png", "wb") as f:
        f.write(requests.get(nekos.img(target)).content)
    img = Image.open("temp.png")
    img.save("temp.webp", "webp")
    msg.reply_document(open("temp.webp", "rb"))
    os.remove("temp.webp")


@run_async
def dva(update, context):
    msg = update.effective_message
    nsfw = requests.get("https://api.computerfreaker.cf/v1/dva").json()
    url = nsfw.get("url")
    # do shit with url if you want to
    if not url:
        msg.reply_text("No URL was received from the API!")
        return
    msg.reply_photo(url)

AVATARLEWD_HANDLER = CommandHandler("avatarlewd", avatarlewd)
AVATAR_HANDLER = CommandHandler("avatar", avatar)
GASM_HANDLER = CommandHandler("gasm", gasm)
DVA_HANDLER = CommandHandler("dva", dva)
WAIFU_HANDLER = CommandHandler("waifu", waifu)

dispatcher.add_handler(AVATARLEWD_HANDLER)
dispatcher.add_handler(AVATAR_HANDLER)
dispatcher.add_handler(GASM_HANDLER)
dispatcher.add_handler(DVA_HANDLER)
dispatcher.add_handler(WAIFU_HANDLER)

__handlers__ += [
    AVATARLEWD_HANDLER,
    AVATAR_HANDLER,
    GASM_HANDLER,
    DVA_HANDLER,
    WAIFU_HANDLER,
]
