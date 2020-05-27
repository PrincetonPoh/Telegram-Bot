# Tutorial: https://towardsdatascience.com/how-to-deploy-a-telegram-bot-using-heroku-for-free-9436f89575d2

"""
First, a few callback functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Example of a bot-user conversation using ConversationHandler.
Send /start to initiate the conversation.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging
from telegram import ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler, CallbackQueryHandler)

TOKEN = 'ReplaceMe'


# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


svc = {'role':None, 'Name of service':None, 'Description':None, 'Price':None, 'Time period':None}
NAME, DESCRIPTION, VALUE, DURATION, CONFIRM, POST_SVC = range(6)
ASKING_BTN, OFFERING_BTN = range(6, 8)


def start(update, context):
    buttons = [[InlineKeyboardButton('asking', callback_data=str(ASKING_BTN)),
                InlineKeyboardButton('offering', callback_data=str(OFFERING_BTN))]]
    keyboard = InlineKeyboardMarkup(buttons)
    update.message.reply_text(text = 'This is a pilot program to see if we can expand our services beyond delivery.', reply_markup=keyboard)
    
    ud = context.user_data
    ud = svc
    return NAME

def name_svc_o(update, context):
    query = update.callback_query
    query.answer()

    ud = context.user_data
    ud['role'] = 'OFFERer'
    query.edit_message_text(text = 'Alright OFFERer!\nWhat is the name of the service you are offering?')    
    # update.message.reply_text('testing message') #cant solve this issue..........idky cant use this line of quote for callbackquery
    return DESCRIPTION

def name_svc_a(update, context):
    query = update.callback_query
    query.answer()

    ud = context.user_data
    ud['role'] = 'ASKer'
    query.edit_message_text(text = 'Alright ASKer!\nWhat is the name of the service you are asking for?')
    return DESCRIPTION


def description_svc(update, context):
    ud = context.user_data
    ud['Name of service'] = str(update.message.text)
    update.message.reply_text(text = 'Give us a short description of your service. ')
    return VALUE


def value_svc(update, context):
    ud = context.user_data
    ud['Description'] = str(update.message.text)

    if ud['role'] == 'OFFERer':
        update.message.reply_text(text = 'How much are you willing to charge?')
    elif ud['role'] == 'ASKer':
        update.message.reply_text(text = 'How much are you willing to pay?')
    
    return DURATION

def duration_svc(update, context):
    ud = context.user_data
    ud['Price'] = str(update.message.text)

    if ud['role'] == 'OFFERer':
        update.message.reply_text(text = 'How long is the duration of your offer?')
    elif ud['role'] == 'ASKer':
        update.message.reply_text(text = 'How long is the duration of your request?')

    return CONFIRM

def facts_to_str(user_data):
    facts = list()

    for key, value in user_data.items():
        facts.append('{}: {}'.format(key, value))

    return "\n".join(facts).join(['\n', '\n'])

def confirm_svc(update, context):
    ud = context.user_data
    ud['Time period'] = str(update.message.text)

    reply_keyboard = [['Yes!','Cancel!']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    update.message.reply_text("FANTASTIC! Just so you know, this is what you already told me:\n"
                              "{} \nAre you willing to proceed to posting?".format(facts_to_str(ud)),
                              reply_markup=markup)
    
    return POST_SVC


def posting_svc(update, context):
    ud = context.user_data

    # find out how to retrive sender's username

    # craft message to post in the main chat group

    # this is how to post to another channel
    # context.bot.send_message(chat_id='@neibbb123', text='SUCCESS AGAIN YES!')

    ud.clear()
    return ConversationHandler.END

def filler_f(update, context):
    ud = context.user_data
    ud.clear()
    print('Filler here for food. go back main menu')
    # need to return to mainmenu
    return ConversationHandler.END


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add conversation handler with the states CHOOSING, TYPING_CHOICE and TYPING_REPLY
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            NAME: [CallbackQueryHandler(name_svc_o, pattern='^'+str(ASKING_BTN)+'$'),
                    CallbackQueryHandler(name_svc_a, pattern='^'+str(OFFERING_BTN)+'$')],
            DESCRIPTION: [MessageHandler(Filters.text, description_svc)],
            VALUE: [MessageHandler(Filters.text, value_svc)],
            DURATION: [MessageHandler(Filters.text, duration_svc)],
            CONFIRM: [MessageHandler(Filters.text, confirm_svc)],
            POST_SVC: [MessageHandler(Filters.regex('^Yes!$'), posting_svc),
                       MessageHandler(Filters.regex('^Cancel!$'), filler_f)
                       ]
        },

        fallbacks=[MessageHandler(Filters.regex('^Done$'), filler_f)]
    )

    dp.add_handler(conv_handler)

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