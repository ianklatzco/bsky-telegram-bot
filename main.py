from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from atprototools import Session
import logging, datetime
import random, os, json
import requests, random, datetime, re

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)
                    #  level=logging.DEBUG)
#logging.getLogger().setLevel(logging.DEBUG)

creds = json.load(open("credentials.json"))

ATP_HOST = "https://bsky.social"
ATP_AUTH_TOKEN = ""

TELEGRAM_BOT_TOKEN = creds.get("TELEGRAM_BOT_TOKEN")

USERNAME = creds.get("USERNAME")
PASSWORD = creds.get("PASSWORD")

BLUESKIES_USERNAME = creds.get("BLUESKIES_USERNAME")
BLUESKIES_PASSWORD = creds.get("BLUESKIES_PASSWORD")

BSKIES_AUTH_TOKEN = ""
BSKIES_DID = ""

TELEGRAM_CHAT_ID = creds.get("TELEGRAM_CHAT_ID")
allowlisted_chat_ids =  [TELEGRAM_CHAT_ID]

#  Primary object: updater
#  use_context is a back-compatibility thing

from telegram.ext import Updater, InlineQueryHandler, CommandHandler

def bop(update, context):
    message_text = update.message.text.replace("/s ","")
    # allowlist
    foo = update.effective_chat.id
    if foo not in allowlisted_chat_ids:
        context.bot.send_message(chat_id=TELEGRAM_CHAT_ID, text="recv'd unallowlisted from")
        context.bot.send_message(chat_id=TELEGRAM_CHAT_ID, text= update.effective_chat.username)
        raise
    # end allowlist

    thing_to_skoot = ""
    if message_text:
        thing_to_skoot = message_text
    else:
        thing_to_skoot = "testskoot from telegram bot"

    session = Session(USERNAME, PASSWORD)
    resp = session.post_skoot(thing_to_skoot)
    context.bot.send_message(chat_id=TELEGRAM_CHAT_ID, text="skooted!")


def save_image(update, context):
    """Save the image to disk."""
    # Get the file object from the message
    file_obj = context.bot.get_file(update.message.photo[-1])
    # Generate a unique filename
    filename = os.path.join('imgtmp', f"{file_obj.file_id}.jpg")
    # Save the file to disk
    file_obj.download(filename)
    update.message.reply_text(f"Image saved to {filename}")

    thing_to_bloot = update.message.caption

    session = Session(USERNAME, PASSWORD)
    resp = session.post_skoot(thing_to_bloot, image_path=filename)
    context.bot.send_message(chat_id=TELEGRAM_CHAT_ID, text="posted image!")


def bskies(update, context):
    message_text = update.message.text.replace("/b ","")
    # allowlist
    foo = update.effective_chat.id
    if foo not in allowlisted_chat_ids:
        context.bot.send_message(chat_id=TELEGRAM_CHAT_ID, text="recv'd unallowlisted from")
        context.bot.send_message(chat_id=TELEGRAM_CHAT_ID, text= update.effective_chat.username)
        raise
    # end allowlist


    try:
        session = Session(BLUESKIES_USERNAME, BLUESKIES_PASSWORD)
        resp = session.reskoot(message_text)
        context.bot.send_message(chat_id=TELEGRAM_CHAT_ID, text="reskoot made to blueskies.bsky.social!")
    except:
        context.bot.send_message(chat_id=TELEGRAM_CHAT_ID, text="reskoot failed!")
        


def main():
    updater = Updater(TELEGRAM_BOT_TOKEN)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('s',bop))
    dp.add_handler(CommandHandler('b',bskies))
    dp.add_handler(MessageHandler(Filters.photo, save_image))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()

