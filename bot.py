import logging
import settings
from telegram.ext import Updater, CommandHandler, \
                    MessageHandler, Filters, RegexHandler
from telegram import ReplyKeyboardMarkup, KeyboardButton
from glob import glob
from random import choice
from emoji import emojize


logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    filename='bot.log'
)


def greet_user(bot, update, user_data):
    smile = emojize(choice(settings.USER_EMOJI), use_aliases=True)
    user_data['smile'] = smile
    text = f"Hi! {smile} Wuz up!"
    update.message.reply_text(text, reply_markup=get_keyboard())


def talk_to_me(bot, update, user_data):
    user_text = f"Hi, {update.message.chat.first_name}!\n" \
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
    bot.send_photo(chat_id=update.message.chat.id, photo=open(cat_pic, 'rb'), reply_markup=get_keyboard())


def get_contact(bot, update, user_data):
    print(update.message.contact)
    update.message.reply_text(f'Спасибо {user_data}', reply_markup=get_keyboard())


def get_location(bot, update, user_data):
    print(update.message.location)
    update.message.reply_text('Спасибо {user_data}', reply_markup=get_keyboard())


def get_keyboard():
    contact_button = KeyboardButton('Контактные данные', request_contact=True)
    location_button = KeyboardButton('Геолокация', request_location=True)
    my_keyboard = ReplyKeyboardMarkup([
                                    ['Прислать котика'],
                                    [contact_button, location_button]
    ], resize_keyboard=True)

    return my_keyboard


def main():
    mybot = Updater(
        settings.API_KEY,
        request_kwargs=settings.PROXY
    )

    logging.info('Бот запускается')

    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("start", greet_user, pass_user_data=True))
    dp.add_handler(CommandHandler(
                                "cat",
                                send_cat_picture,
                                pass_user_data=True
    ))
    dp.add_handler(
    RegexHandler('^(Прислать котика)$', 
                send_cat_picture, 
                pass_user_data=True)
    )
    dp.add_handler(MessageHandler(Filters.contact, get_contact, pass_user_data=True))
    dp.add_handler(MessageHandler(Filters.location, get_location, pass_user_data=True))

    dp.add_handler(MessageHandler(
                                Filters.text,
                                talk_to_me,
                                pass_user_data=True
    ))

    mybot.start_polling()
    mybot.idle()


if __name__ == '__main__':
    main()
