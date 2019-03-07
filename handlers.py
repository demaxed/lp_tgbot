import settings
from telegram.ext import Updater, CommandHandler, \
                    MessageHandler, Filters, RegexHandler
from glob import glob
from random import choice
from emoji import emojize

from utils import get_keyboard, get_user_emo


def greet_user(bot, update, user_data):
    smile = get_user_emo(user_data)
    user_data['smile'] = smile
    text = f"Hi! {smile} Wuz up!"
    update.message.reply_text(text, reply_markup=get_keyboard())


def talk_to_me(bot, update, user_data):
    smile = get_user_emo(user_data)
    user_text = f"Hi, {update.message.chat.first_name} {smile}!\n" \
                f"You have written: '{update.message.text}'"
    logging.info(
            f"User: {update.message.chat.username},\n"
            f"Chat id: {update.message.chat.id},\n"
            f"Message: {update.message.text}"
    )
    update.message.reply_text(user_text, reply_markup=get_keyboard())


def send_cat_picture(bot, update, user_data):
    cat_list = glob('images/cat*.jp*g')
    cat_pic = choice(cat_list)
    bot.send_photo(
                chat_id=update.message.chat.id,
                photo=open(cat_pic, 'rb'),
                reply_markup=get_keyboard()
    )


def get_contact(bot, update, user_data):
    print(update.message.contact)
    update.message.reply_text(
            f'Спасибо {user_data}', reply_markup=get_keyboard()
    )


def get_location(bot, update, user_data):
    print(update.message.location)
    update.message.reply_text(
        f'Спасибо {user_data}', reply_markup=get_keyboard()
    )
