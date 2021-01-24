from telegram import ParseMode, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CommandHandler, CallbackQueryHandler
from telegram.ext.dispatcher import run_async
import importlib
from Bot.modules import ALL_MODULES
from Bot import LOGGER, dispatcher, updater, OWNER_ID
from Bot.modules.helpers.misc import paginate_modules
import re
import traceback
import requests
import html

IMPORTED = {}
HELPABLE = {}
STATS = []

for module_name in ALL_MODULES:
    imported_module = importlib.import_module("Bot.modules." + module_name)
    if not hasattr(imported_module, "__mod_name__"):
        imported_module.__mod_name__ = imported_module.__name__

    if not imported_module.__mod_name__.lower() in IMPORTED:
        IMPORTED[imported_module.__mod_name__.lower()] = imported_module
    else:
        raise Exception("Can't have two modules with the same name! Please change one")
    
    if hasattr(imported_module, "__help__") and imported_module.__help__:
        HELPABLE[imported_module.__mod_name__.lower()] = imported_module
        
    if hasattr(imported_module, "__stats__"):
        STATS.append(imported_module)


def send_help(chat_id, text, keyboard=None):
    if not keyboard:
        keyboard = InlineKeyboardMarkup(paginate_modules(0, HELPABLE, "help"))
    dispatcher.bot.send_message(
        chat_id=chat_id, text=text, parse_mode=ParseMode.MARKDOWN, reply_markup=keyboard
    )
    
    
PM_START_TEXT = f"""
Hewwo, uwu >////<.
Tap on /help to know all my commands!
""" 

HELP_STRINGS = f"""
Hello there! My name is *{dispatcher.bot.first_name}*. The lewdest near you.
I provide lewds.
*Main* commands available:
 • /start: Starts me, can be used to check I'm alive or not.
 • /help: PM's you this message.
Click on the buttons below to get documentation about specific modules!
"""

@run_async
def start(update, context):
    buttons = [
    [
        InlineKeyboardButton(
            text="Add to Group 👥", url="t.me/{}?startgroup=true".format(context.bot.username)
        ),
        InlineKeyboardButton("Maintained by", url="t.me/dank_as_fuck"),
    ]
]
    if update.effective_chat.type == "private":
        args = context.args
        if len(args) >= 1:
            if args[0].lower() == "help":
                send_help(update.effective_chat.id, HELP_STRINGS)
        else:
            update.effective_message.reply_photo(
                "https://telegra.ph/file/1a94f94b54cb28cb4fb98.jpg",
                PM_START_TEXT,
                reply_markup=InlineKeyboardMarkup(buttons),
                parse_mode=ParseMode.MARKDOWN,
                timeout=60,
                disable_web_page_preview=True,
            )
    else:
        update.effective_message.reply_text(
            "Hi, I'm Chizuru."
        )

def error_handler(update, context):
    """Log the error and send a telegram message to notify the developer."""
    cmd, args = update.effective_message.text.split(None, 1)
    LOGGER.error(msg="Error found, check dump below:", exc_info=context.error)

    # traceback.format_exception returns the usual python message about an exception, but as a
    # list of strings rather than a single string, so we have to join them together.
    tb_list = traceback.format_exception(
        None, context.error, context.error.__traceback__
    )
    trace = "".join(tb_list)

    # lets try to get as much information from the telegram update as possible
    payload = f"\n<b>- Command</b>: <code>{cmd}</code>"
    payload += f"\n<b>- Arguments</b>: <code>{args}</code>"
    payload += f"\n<b>- Error message</b>:\n<code>{context.error}</code>"
    # normally, we always have a user. If not, its either a channel or a poll update.
    if update.effective_user:
        payload += f" \n<b>- User</b>: {mention_html(update.effective_user.id, update.effective_user.first_name)}"
    # there are more situations when you don't get a chat
    if update.effective_chat:
        if update.effective_chat.title == None:
            payload += f" \n<b>- Chat</b>: <i>Bot PM</i>"
        else:
            payload += (
                f" \n<b>- Chat</b>: <i>{update.effective_chat.title}</i>"
            )
    # but only one where you have an empty payload by now: A poll (buuuh)
    if update.poll:
        payload += f" \n<b>- Poll id</b>: {update.poll.id}."
    # lets put this in a "well" formatted text
    text = f"<b>Error found while handling an update!</b> {payload}"

    # now paste the error (trace) in nekobin and make buttons
    # with url of log, as log in telegram message is hardly readable..
    key = (
        requests.post(
            "https://nekobin.com/api/documents",
            json={
                "content": f"{trace}\n\n{json.dumps(update.to_dict(), indent=2, ensure_ascii=False)}"
            },
        )
        .json()
        .get("result")
        .get("key")
    )

    markup = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="Full traceback on nekobin",
                    url=f"https://nekobin.com/{key}.py",
                ),
                # InlineKeyboardButton(
                #     text="Send traceback as message",
                #     ,
                # ),
            ]
        ]
    )
    context.bot.send_message(
        OWNER_ID, text, reply_markup=markup, parse_mode="html"
    )

@run_async
def help_button(update, context):
    query = update.callback_query
    mod_match = re.match(r"help_module\((.+?)\)", query.data)
    prev_match = re.match(r"help_prev\((.+?)\)", query.data)
    next_match = re.match(r"help_next\((.+?)\)", query.data)
    back_match = re.match(r"help_back", query.data)

    print(query.message.chat.id)

    try:
        if mod_match:
            module = mod_match.group(1)
            text = (
                "Here is the help for the *{}* module:\n".format(
                    HELPABLE[module].__mod_name__
                )
                + HELPABLE[module].__help__
            )
            query.message.edit_text(text=text,
                                parse_mode=ParseMode.MARKDOWN,
                                reply_markup=InlineKeyboardMarkup(
                    [[InlineKeyboardButton(text="⬅️ Back", callback_data="help_back")]]
                ),
            )

        elif prev_match:
                curr_page = int(prev_match.group(1))
                query.message.edit_text(
                text=HELP_STRINGS,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(curr_page - 1, HELPABLE, "help")))

        elif next_match:
            next_page = int(next_match.group(1))
            query.message.edit_text(
                text=HELP_STRINGS,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(next_page + 1, HELPABLE, "help")))

        elif back_match:
            query.message.edit_text(
                text=HELP_STRINGS,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(paginate_modules(0, HELPABLE, "help")))

        # ensure no spinny white circle
        context.bot.answer_callback_query(query.id)
    except Exception as excp:
        if excp.message not in {
            "Message is not modified",
            "Query_id_invalid",
            "Message can't be deleted",
        }:
            query.message.edit_text(excp.message)
            LOGGER.exception("Exception in help buttons. %s", str(query.data))
        
        
@run_async
def get_help(update, context):
    chat = update.effective_chat  # type: Optional[Chat]
    args = update.effective_message.text.split(None, 1)

    # ONLY send help in PM
    if chat.type != chat.PRIVATE:

        update.effective_message.reply_text(
            "Contact me in PM to get the list of possible commands.",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="Help",
                            url="t.me/{}?start=help".format(context.bot.username),
                        )
                    ]
                ]
            ),
        )
        return

    elif len(args) >= 2 and any(args[1].lower() == x for x in HELPABLE):
        module = args[1].lower()
        text = (
            "Here is the available help for the *{}* module:\n".format(
                HELPABLE[module].__mod_name__
            )
            + HELPABLE[module].__help__
        )
        send_help(
            chat.id,
            text,
            InlineKeyboardMarkup(
                [[InlineKeyboardButton(text="Back", callback_data="help_back")]]
            ),
        )

    else:
        send_help(chat.id, HELP_STRINGS)

def main():
    dispatcher.add_handler(CommandHandler("start", start, pass_args=True))
    help_handler = CommandHandler("help", get_help)
    help_callback_handler = CallbackQueryHandler(help_button, pattern=r"help_")
    dispatcher.add_handler(help_handler)
    dispatcher.add_handler(help_callback_handler)
    dispatcher.add_error_handler(error_handler)


if __name__ == "__main__":
    LOGGER.info("Successfully loaded modules: " + str(ALL_MODULES))
    LOGGER.info("Using long polling.")
    main()
    updater.start_polling(timeout=15, read_latency=4)
    updater.idle()
