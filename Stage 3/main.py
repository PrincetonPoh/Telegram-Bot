TOKEN = 'ReplaceMe'

import logging
import datetime

from telegram import (ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler, CallbackQueryHandler)

#####################################
import pyrebase

projectid = "ReplaceMe"
dburl = "https://" + projectid + ".firebaseio.com"
authdomain = projectid + ".firebaseapp.com"
apikey = "ReplaceMe"
email = "ReplaceMe"
password = "ReplaceMe"

config = {
    "apiKey": apikey,
    "authDomain": authdomain,
    "databaseURL": dburl,
    "storageBucket": projectid + ".appspot.com"
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
user = auth.sign_in_with_email_and_password(email, password)
db = firebase.database()
#######################################

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


# states
MAIN_MENU, SELECTING_ACTION, FEEDBACK = range(3)
# top layer buttons
MAIN_MENU_BTN, FEEDBACK_BTN, FAQ_BTN, FOOD_BTN, SVC_BTN  = range(3, 8)
# second layer buttons
REQUEST_BTN, DELIVER_BTN, ASKING_BTN, OFFERING_BTN = range(8, 12)
# Shortcut for ConversationHandler.END
END = ConversationHandler.END

# foodchain states
food = {'role':None, 'what':None, 'where':None, 'when_purchase':None, 'when':None, 'price':None}
WHAT, WHERE, WHEN_PURCHASE, WHEN, PRICE, CONFIRMATION, POST_FOOD = range(12,19)

# svcchain states
svc = {'role':None, 'Name of service':None, 'Description':None, 'Price':None, 'Time period':None}
NAME, DESCRIPTION, VALUE, DURATION, CONFIRM, POST_SVC = range(19,25)

# Top level conversation callbacks
def start(update, context):

    text = 'Hi, I\'m Bot called Neighbourly :D\n'\
        'My job is to collect information from you and post it to the channel called @neighbourlySGpendingRd. Click the channel to join.\n'\
        'My creator created me to help pool resources together due to Covid19. We live so close to each other yet we are so socially distant.\n'\
        'Sometimes the help you are looking for is...just next door!\n \n'\
        'Please choose which *action* to take. Any feedback is greatly appreciated too :)\n \n'\
        '(this bot is free and will timeout after 30min. Type /start and wait 10sec to restart)'
    buttons = [[
        InlineKeyboardButton(text='Food', callback_data=str(FOOD_BTN)),
        InlineKeyboardButton(text='Custom Services', callback_data=str(SVC_BTN))
    ], [
        InlineKeyboardButton(text='Feedback', callback_data=str(FEEDBACK_BTN)),
        InlineKeyboardButton(text='How to Use/FAQ', callback_data=str(FAQ_BTN))
    ]]
    keyboard = InlineKeyboardMarkup(buttons)
    
    update.message.reply_text(text=text, parse_mode='markdown', reply_markup=keyboard)
    return SELECTING_ACTION

def start_again(update, context):
    query = update.callback_query
    query.answer()

    text = 'Hi, I\'m Bot called Neighbourly :D\n'\
        'My job is to collect information from you and post it to the channel called @neighbourlySGpendingRd. Click the channel to join.\n'\
        'My creator created me to help pool resources together due to Covid19. We live so close to each other yet we are so socially distant.\n'\
        'Sometimes the help you are looking for is...just next door!\n \n'\
        'Please choose which *action* to take. Any feedback is greatly appreciated too :)\n \n'\
        '(this bot is free and will timeout after 30min. Type /start and wait 10sec to restart)'
    buttons = [[
        InlineKeyboardButton(text='Food', callback_data=str(FOOD_BTN)),
        InlineKeyboardButton(text='Custom Services', callback_data=str(SVC_BTN))
    ], [
        InlineKeyboardButton(text='Feedback', callback_data=str(FEEDBACK_BTN)),
        InlineKeyboardButton(text='How to use/FAQ', callback_data=str(FAQ_BTN))
    ]]
    keyboard = InlineKeyboardMarkup(buttons)
    
    query.edit_message_text(text=text, parse_mode='markdown', reply_markup=keyboard)
    return SELECTING_ACTION


def to_faq(update, context):
    query = update.callback_query
    query.answer()
    buttons = [[InlineKeyboardButton("main menu", callback_data=str(MAIN_MENU_BTN))]]
    keyboard = InlineKeyboardMarkup(buttons)
    query.edit_message_text(
        text='1) How to use this bot? \n'\
                'This is a bot to record your requests and post in the channel @NeighbourlySGpendingRd \n'\
                'Type /start to activate the bot.\n'\
                'Press the respective buttons to navigate the bot\n \n'\
            '2) What if the bot hangs?\n'\
                'Type /start to reset the bot\n \n'\
            '3) Where do I see my offer/request?\n'\
                'Head to the channel called @NeighbourlySGpendingRd to see your post\n \n'\
            '4) I am interested in one of the service. What do I do?\n'\
                'Clarify/inquire/place your orders through private messaging the person (click their @username).\n \n'\
            '5) Do the creators benefit from this? Are there hidden costs?\n'\
                'No and no. We actually lose money from hosting if too many people use this. Your only cost comes from negotiating with the seller/buyer.\n \n'\
                '(this bot is free and will timeout after 30min. Type /start and wait 10sec to restart)',
        reply_markup=keyboard, parse_mode='markdown')

    return MAIN_MENU


def to_feedback(update, context):
    query = update.callback_query
    query.answer()
    buttons = [
        [InlineKeyboardButton("main menu", callback_data=str(MAIN_MENU_BTN))]
    ]
    keyboard = InlineKeyboardMarkup(buttons)
    query.edit_message_text(
        text='Your feedback is very valuable :D Please type your feedback here:\n \n'\
            '(this bot is free and will timeout after 30min. Type /start and wait 10sec to restart)',
        reply_markup=keyboard)
    return FEEDBACK

def save_feedback(update, context):
    #hyperlink = 'https://t.me/' + username + ':   '
    username = '@' + str(update.message.from_user.username)
    user_feedback = str(update.message.text)
    time = str(datetime.datetime.now().isoformat(timespec='minutes') )     # e.g 2020-05-23T23:39 => (year-month-day hour:min)
    db.child("feedback").update({time:{username: user_feedback}}, user['idToken'])
    
    buttons = [[InlineKeyboardButton("main menu", callback_data=str(MAIN_MENU_BTN))]]
    keyboard = InlineKeyboardMarkup(buttons)
    update.message.reply_text(text = 'Thank you so much for your valuable feedback!\n \n'\
                                    '(this bot is free and will timeout after 30min. Type /start and wait 10sec to restart)',
                                    reply_markup = keyboard)
    
    return MAIN_MENU


########################################################## start of foodchain
def to_food(update, context):
    query = update.callback_query
    query.answer()

    buttons = [[InlineKeyboardButton('requester', callback_data=str(REQUEST_BTN)),
                InlineKeyboardButton('deliverer', callback_data=str(DELIVER_BTN))]]
    keyboard = InlineKeyboardMarkup(buttons)
    query.edit_message_text(text = 'Thank you for choosing FOOD.\n'\
                                    'Do you wish to be a requester or deliverer?\n \n'\
                                    '(this bot is free and will timeout after 30min. Type /start and wait 10sec to restart)', reply_markup=keyboard)
    
    ud = context.user_data
    ud = food
    return WHAT


def what_food_r(update, context):
    query = update.callback_query
    query.answer()

    ud = context.user_data
    ud['role'] = 'requester'

    buttons = [[InlineKeyboardButton("main menu", callback_data=str(MAIN_MENU_BTN))]]
    keyboard = InlineKeyboardMarkup(buttons)
    query.edit_message_text(text = 'Alright requester!\nNow, type in the food you want to request and please include the *store*.\n'\
                                '(e.g Earl Grey milk tea, 50% sugar, large, KOI)',reply_markup=keyboard, parse_mode='markdown')    
    # update.message.reply_text('testing message') #this is where i will get an error
    return WHERE

def what_food_d(update, context):
    query = update.callback_query
    query.answer()

    buttons = [[InlineKeyboardButton("main menu", callback_data=str(MAIN_MENU_BTN))]]
    keyboard = InlineKeyboardMarkup(buttons)

    ud = context.user_data
    ud['role'] = 'deliverer'
    query.edit_message_text(text = 'Alright deliverer!\nNow, type in the food you want to deliver and please include the *store*.\n'\
                                '(e.g Earl Grey milk tea, 50% sugar, large, KOI)',reply_markup=keyboard, parse_mode='markdown')
    return WHERE

def where_food(update, context):
    ud = context.user_data
    ud['what'] = str(update.message.text)

    buttons = [[InlineKeyboardButton("main menu", callback_data=str(MAIN_MENU_BTN))]]
    keyboard = InlineKeyboardMarkup(buttons)
    update.message.reply_text(text = '*Where* do you want to meet for collection?\n' \
                                    '(e.g Bukit Panjang rd, blk 123, lift loby)',reply_markup=keyboard, parse_mode='markdown')
    if ud['role'] == 'requester':
        return WHEN
    elif ud['role'] == 'deliverer':
        return WHEN_PURCHASE

def when_purchase_food(update, context):
    ud = context.user_data
    ud['where'] = str(update.message.text)

    buttons = [[InlineKeyboardButton("main menu", callback_data=str(MAIN_MENU_BTN))]]
    keyboard = InlineKeyboardMarkup(buttons)
    update.message.reply_text(text = '*Date and time* you will make the purchase?',reply_markup=keyboard, parse_mode='markdown')
    return WHEN

def when_food(update, context):
    ud = context.user_data

    buttons = [[InlineKeyboardButton("main menu", callback_data=str(MAIN_MENU_BTN))]]
    keyboard = InlineKeyboardMarkup(buttons)
    if ud['role'] == 'requester':
        ud['where'] = str(update.message.text)
        update.message.reply_text(text = '*Date and time* to meet the seller?',reply_markup=keyboard, parse_mode='markdown')
    elif ud['role'] == 'deliverer':
        ud['when_purchase'] = str(update.message.text)
        update.message.reply_text(text = '*Date and time* to meet the buyer?',reply_markup=keyboard, parse_mode='markdown')
    
    return PRICE

def price_food(update, context):
    ud = context.user_data
    ud['when'] = str(update.message.text)

    buttons = [[InlineKeyboardButton("main menu", callback_data=str(MAIN_MENU_BTN))]]
    keyboard = InlineKeyboardMarkup(buttons)

    if ud['role'] == 'requester':
        update.message.reply_text(text = 'How much *$* are you willing to pay for delivery?\n' \
                                    '(e.g $3.5 bubble tea + $2 delivery fee)',reply_markup=keyboard, parse_mode='markdown')
    elif ud['role'] == 'deliverer':
        update.message.reply_text(text = 'How much *$* are you willing to charge for delivery?\n' \
                                    '(e.g $3.5 bubble tea + $2 delivery fee)',reply_markup=keyboard, parse_mode='markdown')

    

    return CONFIRMATION

def facts_to_str(user_data):
    facts = list()

    for key, value in user_data.items():
        facts.append('{}: {}'.format(key, value))

    return "\n".join(facts).join(['\n', '\n'])

def confirmation_food(update, context):
    ud = context.user_data
    ud['price'] = str(update.message.text)

    reply_keyboard = [['Yes!','Cancel!']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    update.message.reply_text("FANTASTIC! This is what you have told me:\n"\
                            "{} \nAre you willing to proceed to posting?\n"\
                            'If buttons go missing, type Yes! or Cancel!\n \n'\
                            '(this bot is free and will timeout after 30min. Type /start and wait 10sec to restart)'.format(facts_to_str(ud)),
                              reply_markup=markup)
    
    return POST_FOOD

def posting_food(update, context):
    ud = context.user_data
    username = '@' + str(update.message.from_user.username)     # retrive sender's username
    
    if ud['role'] == 'requester':
        context.bot.send_message(chat_id='@neighbourlySGpendingRd', text = 'FOOD {}! from bot @neighbourly_bot\n'\
            'Contact info: {}\n'\
            'Food name: {}\n'\
            'Location: {}\n'\
            'Time to meet: {}\n'\
            'Cost: {}\n'.format(ud['role'], username, ud['what'], ud['where'], ud['when'], ud['price']) )
            
    elif ud['role'] == 'deliverer':
        context.bot.send_message(chat_id='@neighbourlySGpendingRd', 
                    text = 'FOOD {}!\n'\
                        'Contact info: {}\n'\
                        'Food name: {}\n'\
                        'Location: {}\n'\
                        'Time of order: {}\n'\
                        'Time to meet: {}\n'\
                        'Cost: {}\n \n'\
                        'Use the bot @neighbourly_bot to post messages'.format(ud['role'], username, ud['what'], ud['where'], ud['when_purchase'], ud['when'], ud['price']) 
                        )
    buttons = [[InlineKeyboardButton('main menu', callback_data=str(MAIN_MENU_BTN))]]
    keyboard = InlineKeyboardMarkup(buttons)
    update.message.reply_text(text = 'Successfully submitted!\n'\
                                'You can see your post on @neighbourlySGpendingRD in a few moments :D\n \n'\
                                '(this bot is free and will timeout after 30min. Type /start and wait 10sec to restart)', reply_markup=keyboard)
    ud.clear()
    return END

def cancellation(update, context):
    ud = context.user_data

    buttons = [[InlineKeyboardButton('main menu', callback_data=str(MAIN_MENU_BTN))]]
    keyboard = InlineKeyboardMarkup(buttons)
    update.message.reply_text(text = 'Cancelled! Go back to main menu bah\n \n'\
                                    '(this bot is free and will timeout after 30min. Type /start and wait 10sec to restart)', reply_markup=keyboard)

    ud.clear()
    return END

def fil(update,context):
    ud = context.user_data
    ud.clear()
    END
    return start_again(update,context)
############################################################# end of foodchain


########################################################## start of svcchain
def to_svc(update, context):
    query = update.callback_query
    query.answer()

    buttons = [[InlineKeyboardButton('asking', callback_data=str(ASKING_BTN)),
                InlineKeyboardButton('offering', callback_data=str(OFFERING_BTN))]]
    keyboard = InlineKeyboardMarkup(buttons)
    query.edit_message_text(text = 'Thank you for choosing CUSTOM SERVICES\n'\
                                    'Do you wish to be a ASKer or OFFERer?\n \n'\
                                    '(this bot is free and will timeout after 30min. Type /start and wait 10sec to restart)', reply_markup=keyboard)
    
    ud = context.user_data
    ud = svc
    return NAME


def name_svc_o(update, context):
    query = update.callback_query
    query.answer()

    ud = context.user_data
    ud['role'] = 'OFFERer'

    buttons = [[InlineKeyboardButton("main menu", callback_data=str(MAIN_MENU_BTN))]]
    keyboard = InlineKeyboardMarkup(buttons)
    query.edit_message_text(text = 'Alright OFFERer!\nWhat is the *name* of the service you are offering?\n'\
                                '(e.g Bulk buy lazada/3d printing/teach tuition/*recycle trash*/bball tgt)',reply_markup=keyboard, parse_mode='markdown')    
    # update.message.reply_text('testing message') #cant solve this issue..........idky cant use this line of quote for callbackquery
    return DESCRIPTION

def name_svc_a(update, context):
    query = update.callback_query
    query.answer()

    ud = context.user_data
    ud['role'] = 'ASKer'

    buttons = [[InlineKeyboardButton("main menu", callback_data=str(MAIN_MENU_BTN))]]
    keyboard = InlineKeyboardMarkup(buttons)
    query.edit_message_text(text = 'Alright ASKer!\nWhat is the *name* of the service you are asking for?\n'\
                                '(e.g Bulk buy lazada/3d printing/teach tuition/*recycle trash*/bball tgt)',reply_markup=keyboard, parse_mode='markdown')  
    return DESCRIPTION


def description_svc(update, context):
    ud = context.user_data
    ud['Name of service'] = str(update.message.text)

    buttons = [[InlineKeyboardButton("main menu", callback_data=str(MAIN_MENU_BTN))]]
    keyboard = InlineKeyboardMarkup(buttons)
    update.message.reply_text(text = 'Give a more detailed description/explanation of your service.\n'\
                                    '(e.g Im a student and recycling newspaper for project / Im looking for someone to bball tgt)',reply_markup=keyboard)
    return VALUE


def value_svc(update, context):
    ud = context.user_data
    ud['Description'] = str(update.message.text)
    
    buttons = [[InlineKeyboardButton("main menu", callback_data=str(MAIN_MENU_BTN))]]
    keyboard = InlineKeyboardMarkup(buttons)
    if ud['role'] == 'OFFERer':
        update.message.reply_text(text = 'How much are you willing to charge?\n'\
                                        '(e.g $1 per 10 pages/$10 per hour)',reply_markup=keyboard)
    elif ud['role'] == 'ASKer':
        update.message.reply_text(text = 'How much are you willing to pay?\n'\
                                        '(e.g $1 per 10 pages/$10 per hour)',reply_markup=keyboard)
    
    return DURATION

def duration_svc(update, context):
    ud = context.user_data
    ud['Price'] = str(update.message.text)

    buttons = [[InlineKeyboardButton("main menu", callback_data=str(MAIN_MENU_BTN))]]
    keyboard = InlineKeyboardMarkup(buttons)
    if ud['role'] == 'OFFERer':
        update.message.reply_text(text = 'How long is the duration of your offer?\n'\
                                    '(e.g 9May/available for this week/9pm on tues/weekends)',reply_markup=keyboard)
    elif ud['role'] == 'ASKer':
        update.message.reply_text(text = 'How long is the duration of your request?\n'\
                                        '(e.g TODAY 7pm/next tues 9am/every wed morning)',reply_markup=keyboard)

    return CONFIRM


def confirm_svc(update, context):
    ud = context.user_data
    ud['Time period'] = str(update.message.text)

    reply_keyboard = [['Yes!','Cancel!']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    update.message.reply_text("FANTASTIC! This is what you have told me:\n"
                            "{}\nAre you willing to proceed to posting?\n"\
                            'If buttons go missing, type Yes! or Cancel!\n \n'\
                            '(this bot is free and will timeout after 30min. Type /start and wait 10sec to restart)'.format(facts_to_str(ud)),
                              reply_markup=markup)
    
    return POST_SVC


def posting_svc(update, context):
    ud = context.user_data
    username = '@' + str(update.message.from_user.username)     # retrive sender's username

    text = 'SERVICE {}!\n'\
            'Contact info: {}\n'\
            'Name of service: {}\n'\
            'Description: {}\n'\
            'Price: {}\n'\
            'Duration of offer: {}\n \n'\
            'Use the bot @neighbourly_bot to post messages'.format(ud['role'], username, ud['Name of service'], ud['Description'], ud['Price'], ud['Time period'])
    context.bot.send_message(chat_id='@neighbourlySGpendingRd', text = text)    #post on channel

    buttons = [[InlineKeyboardButton('main menu', callback_data=str(MAIN_MENU_BTN))]]
    keyboard = InlineKeyboardMarkup(buttons)
    update.message.reply_text(text = 'Successfully submitted!\n'\
                                    'You can see your post on @neighbourlySGpendingRD in a few moments :D\n \n'\
                                    '(this bot is free and will timeout after 30min. Type /start and wait 10sec to restart)', reply_markup=keyboard)
    ud.clear()
    return END
########################################################## end of svcchain

# Error handler
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

    food_chain = ConversationHandler(
        entry_points=[CallbackQueryHandler(to_food, pattern='^' + str(FOOD_BTN) + '$')],

        states={
            WHAT: [CallbackQueryHandler(what_food_r, pattern='^'+str(REQUEST_BTN)+'$'),
                    CallbackQueryHandler(what_food_d, pattern='^'+str(DELIVER_BTN)+'$')],
            WHERE: [MessageHandler(Filters.text, where_food)],
            WHEN_PURCHASE: [MessageHandler(Filters.text, when_purchase_food)],
            WHEN: [MessageHandler(Filters.text, when_food)],
            PRICE: [MessageHandler(Filters.text, price_food)],
            CONFIRMATION: [MessageHandler(Filters.text, confirmation_food)],
            POST_FOOD: [MessageHandler(Filters.regex('^Yes!$'), posting_food),
                       MessageHandler(Filters.regex('^Cancel!$'), cancellation)]
        },

        fallbacks=[CallbackQueryHandler(fil, pattern='^' + str(MAIN_MENU_BTN) + '$')],

        map_to_parent={
            END: MAIN_MENU
        },
        allow_reentry=True
    )

    svc_chain = ConversationHandler(
        entry_points=[CallbackQueryHandler(to_svc, pattern='^' + str(SVC_BTN) + '$')],

        states={
            NAME: [CallbackQueryHandler(name_svc_a, pattern='^'+str(ASKING_BTN)+'$'),
                    CallbackQueryHandler(name_svc_o, pattern='^'+str(OFFERING_BTN)+'$')],
            DESCRIPTION: [MessageHandler(Filters.text, description_svc)],
            VALUE: [MessageHandler(Filters.text, value_svc)],
            DURATION: [MessageHandler(Filters.text, duration_svc)],
            CONFIRM: [MessageHandler(Filters.text, confirm_svc)],
            POST_SVC: [MessageHandler(Filters.regex('^Yes!$'), posting_svc),
                       MessageHandler(Filters.regex('^Cancel!$'), cancellation)
                       ]
        },

        fallbacks=[CallbackQueryHandler(fil, pattern='^' + str(MAIN_MENU_BTN) + '$')],

        map_to_parent={
            END: MAIN_MENU
        },
        allow_reentry=True
    )

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            MAIN_MENU: [CallbackQueryHandler(start_again, pattern='^' + str(MAIN_MENU_BTN) + '$')],
            
            SELECTING_ACTION: [CallbackQueryHandler(to_feedback, pattern='^' + str(FEEDBACK_BTN) + '$'),
                                CallbackQueryHandler(to_faq, pattern='^' + str(FAQ_BTN) + '$'),
                                svc_chain,
                                food_chain],
            
            FEEDBACK: [CallbackQueryHandler(start_again, pattern='^' + str(MAIN_MENU_BTN) + '$'),
                        MessageHandler(Filters.text, save_feedback)]
        },
        fallbacks = [CommandHandler('start', start)]
    )

    # Add ConversationHandler to dispatcher that will be used for handling
    # updates
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