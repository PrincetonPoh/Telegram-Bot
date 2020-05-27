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


reply_keyboard = [['Age', 'Favourite colour'],
                  ['Number of siblings', 'Something else...'],
                  ['Done']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)


food = {'role':None, 'what':None, 'where':None, 'when_purchase':None, 'when':None, 'price':None}

WHAT, WHERE, WHEN_PURCHASE, WHEN, PRICE, CONFIRMATION, POST_FOOD = range(7)
REQUEST_BTN, DELIVER_BTN = range(7, 9)

def facts_to_str(user_data):
    facts = list()

    for key, value in user_data.items():
        facts.append('{} - {}'.format(key, value))

    return "\n".join(facts).join(['\n', '\n'])


# def start(update, context):
#     reply_keyboard = [['requester', 'deliverer']]
#     markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
#     update.message.reply_text(text = 'Do you wish to be a requester or deliverer?', reply_markup=markup)
    
#     ud = context.user_data
#     ud = food
#     return WHAT

def start(update, context):
    buttons = [[InlineKeyboardButton('requester', callback_data=str(REQUEST_BTN)),
                InlineKeyboardButton('deliverer', callback_data=str(DELIVER_BTN))]]
    keyboard = InlineKeyboardMarkup(buttons)
    update.message.reply_text(text = 'Do you wish to be a requester or deliverer?', reply_markup=keyboard)
    
    ud = context.user_data
    ud = food
    return WHAT

def what_food_r(update, context):
    query = update.callback_query
    query.answer()

    ud = context.user_data
    ud['role'] = 'requester'
    query.edit_message_text(text = 'Alright requester!\nNow what food do you want to buy?')    
    # update.message.reply_text('testing message') #cant solve this issue..........idky cant use this line of quote for callbackquery
    return WHERE

def what_food_d(update, context):
    query = update.callback_query
    query.answer()

    ud = context.user_data
    ud['role'] = 'deliverer'
    query.edit_message_text(text = 'Alright deliverer!\nNow what food do you want to sell?')
    return WHERE

def where_food(update, context):
    ud = context.user_data
    ud['what'] = str(update.message.text)
    update.message.reply_text(text = 'Where do we meet then?')
    if ud['role'] == 'requester':
        return WHEN
    elif ud['role'] == 'deliverer':
        return WHEN_PURCHASE

def when_purchase_food(update, context):
    ud = context.user_data
    ud['where'] = str(update.message.text)
    update.message.reply_text(text = 'When do you plan to make the purchase at the location?')
    return WHEN

def when_food(update, context):
    ud = context.user_data

    if ud['role'] == 'requester':
        ud['where'] = str(update.message.text)
        update.message.reply_text(text = 'When shall we meet your seller?')
    elif ud['role'] == 'deliverer':
        ud['where_purchase'] = str(update.message.text)
        update.message.reply_text(text = 'When shall we meet your buyer?')
    
    return PRICE

def price_food(update, context):
    ud = context.user_data
    ud['when'] = str(update.message.text)
    update.message.reply_text(text = 'What is the price you wish to set?')

    return CONFIRMATION

def confirmation_food(update, context):
    ud = context.user_data
    ud['price'] = str(update.message.text)

    reply_keyboard = [['Yes!','Cancel!']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    update.message.reply_text("FANTASTIC! Just so you know, this is what you already told me:"
                              "{} Are you willing to proceed to posting?".format(facts_to_str(ud)),
                              reply_markup=markup)
    
    return POST_FOOD


def posting_food(update, context):
    ud = context.user_data

    # find out how to retrive sender's username

    # craft message to post in the main chat group

    # this is how to post to another channel
    # context.bot.send_message(chat_id='@ReplaceMe', text='SUCCESS AGAIN YES!')

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
            WHAT: [CallbackQueryHandler(what_food_r, pattern='^'+str(REQUEST_BTN)+'$'),
                    CallbackQueryHandler(what_food_d, pattern='^'+str(DELIVER_BTN)+'$')],
            WHERE: [MessageHandler(Filters.text, where_food)],
            WHEN_PURCHASE: [MessageHandler(Filters.text, when_purchase_food)],
            WHEN: [MessageHandler(Filters.text, when_food)],
            PRICE: [MessageHandler(Filters.text, price_food)],
            CONFIRMATION: [MessageHandler(Filters.text, confirmation_food)],
            POST_FOOD: [MessageHandler(Filters.regex('^Yes!$'), posting_food),
                       MessageHandler(Filters.regex('^Cancel!$'), fller_f)
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