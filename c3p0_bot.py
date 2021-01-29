from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import requests
import os

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi!')

def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')

def echo(update, context):
    """Echo the user message."""
    update.message.reply_text(update.message.text)

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def temp(update, context):
    try:
        city = ''
        if len(context.args) > 1:
            space = ' '
            city = space.join(context)
        else:
            city = context.args[0]

        key = os.getenv('OPENWEATHER_API_KEY')

        url = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid={}&units=metric'.format(city, key)

        weather_result = requests.get(url)
        weather_result_data = weather_result.json()
        
        update.message.reply_text("Right now, the temperature in {} is {} °C".format(city, weather_result_data['main']['temp']))
    except:
        update.message.reply_text('Error: Unrecognized city!')

def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(os.getenv('TELEGRAM_TOKEN'), use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("temp", temp))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':
    main()
