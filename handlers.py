import os
import settings
from telegram.ext import Updater, CommandHandler, \
                    MessageHandler, Filters, RegexHandler, \
                    ConversationHandler
from glob import glob
from random import choice
from emoji import emojize
from telegram import ReplyKeyboardRemove, ParseMode, ReplyKeyboardMarkup

from utils import get_keyboard, get_user_emo, is_cat


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


def check_user_photo(bot, update, user_data):
    update.message.reply_text("Обрабатываю фото")
    os.makedirs('downloads', exist_ok=True)
    photo_file = bot.getFile(update.message.photo[-1].file_id)
    filename = os.path.join('downloads', '{}.jpg'.format(photo_file.file_id))
    photo_file.download(filename)
    if is_cat(filename):
        update.message.reply_text("Обнаружен котик, добавляю в библиотеку.")
        new_filename = os.path.join('images', 'cat_{}.jpg'.format(photo_file.file_id))
        os.rename(filename, new_filename)
    else:
        os.remove(filename)
        update.message.reply_text("Тревога, котик не обнаружен!")


def anketa_start(bot, update, user_data):
    update.message.reply_text(
            "Как вас зовут? Напишите имя и фамилию",
            reply_markup=ReplyKeyboardRemove()
    )
    return "name"


def anketa_get_name(bot, update, user_data):
    user_name = update.message.text
    if len(user_name.split(" ")) < 2:
        update.message.reply_text("Пожалуйста, напишите имя и фамилию")
        return "name"
    else:
        user_data["anketa_name"] = user_name
        reply_keyboard = [["1", "2", "3", "4", "5"]]

        update.message.reply_text(
            "Понравился ли вам курс? Оцените по шкале от 1 до 5",
            reply_markup=ReplyKeyboardMarkup(
                    reply_keyboard,
                    one_time_keyboard=True,
                    resize_keyboard=True
            )
        )
        return "rating"


def anketa_rating(bot, update, user_data):
    user_data["anketa_rating"] = update.message.text

    update.message.reply_text("""Оставьте комментарий в свободной форме
        или пропустите этот шаг, введя /cancel""")
    return "comment"


def anketa_comment(bot, update, user_data):
    user_data["anketa_comment"] = update.message.text
    user_text = """
<b>Имя Фамилия:</b> {anketa_name}
<b>Оценка:</b> {anketa_rating}
<b>Комментарий:</b> {anketa_comment}""".format(**user_data)

    update.message.reply_text(
                        user_text,
                        reply_markup=get_keyboard(),
                        parse_mode=ParseMode.HTML
    )
    return ConversationHandler.END


def anketa_skip_comment(bot, update, user_data):
    user_text = """
<b>Имя Фамилия:</b> {anketa_name}
<b>Оценка:</b> {anketa_rating}"""

    update.message.reply_text(
                        user_text,
                        reply_markup=get_keyboard(),
                        parse_mode=ParseMode.HTML
    )
    return ConversationHandler.END


def dontknow(bot, update, user_data):
    update.message.reply_text("don\'t know")
