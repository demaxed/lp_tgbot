import logging
import settings
from telegram.ext import Updater, CommandHandler, \
                    MessageHandler, Filters, RegexHandler, \
                    ConversationHandler

from handlers import greet_user, talk_to_me, send_cat_picture, get_contact, \
                    get_location, check_user_photo, anketa_get_name, \
                    anketa_rating, anketa_comment, anketa_skip_comment, \
                    anketa_start, dontknow


logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    filename='bot.log'
)


def main():
    mybot = Updater(
        settings.API_KEY,
        request_kwargs=settings.PROXY
    )

    logging.info('Бот запускается')

    dp = mybot.dispatcher

    anketa = ConversationHandler(
                    entry_points=[
                        RegexHandler('^(Fill in the form)$',
                        anketa_start,
                        pass_user_data=True)
                    ],
                    states={
                        "name": [
                            MessageHandler(
                            Filters.text,
                            anketa_get_name,
                            pass_user_data=True
                        )],
                        "rating": [
                            RegexHandler(
                            '^(1|2|3|4|5)$',
                            anketa_rating,
                            pass_user_data=True
                        )],
                        "comment": [
                            MessageHandler(
                            Filters.text,
                            anketa_comment,
                            pass_user_data=True),
                            CommandHandler(
                            'skip',
                            anketa_skip_comment,
                            pass_user_data=True
                        )],
                    },
                    fallbacks=[
                            MessageHandler(
                            Filters.text |
                            Filters.video |
                            Filters.photo |
                            Filters.document,
                            dontknow,
                            pass_user_data=True
                        )]
    )
    dp.add_handler(CommandHandler("start", greet_user, pass_user_data=True))
    dp.add_handler(anketa)
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
    dp.add_handler(MessageHandler(
                                Filters.contact,
                                get_contact,
                                pass_user_data=True
    ))
    dp.add_handler(MessageHandler(
                                Filters.location,
                                get_location,
                                pass_user_data=True
    ))
    dp.add_handler(MessageHandler(
                                Filters.photo,
                                check_user_photo,
                                pass_user_data=True
    ))

    dp.add_handler(MessageHandler(
                                Filters.text,
                                talk_to_me,
                                pass_user_data=True
    ))

    mybot.start_polling()
    mybot.idle()


if __name__ == '__main__':
    main()
