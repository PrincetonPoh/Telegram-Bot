# Project Neighbourly!
In view of Covid 19, a large chunk of the economy ceased to function. Even simple tasks such as getting food or printing worksheets are tough. In these times, we turn to our friends and family for help. I asked myself why stop there? 

In Singapore, we all live in HDBs where we are mere metres away from multiple households. Despite living so physically close to each other, we are so socially distant. What if we can have a way to find out what each other need? What if we can share our resources with those closest to us in these tough times?

Hence, ***Neighbourly!*** A telegram bot to help people in my neighbourhood share their resources. People use the bot to post requests/offers in the community channel. People then private message (PM) each other to find out more on how they can help each other.


# My Plan
- Stage 1
    - Learn how telegram API works through the [examples](https://github.com/python-telegram-bot/python-telegram-bot/tree/master/examples) on telegram api github

- Stage 2
    - Learn to host it online using [Heroku](https://towardsdatascience.com/how-to-deploy-a-telegram-bot-using-heroku-for-free-9436f89575d2) services.

- Stage 3
    - Write logic for the actual chatbot
    
- Stage 4
    - Launch first version!
    
- Moving forward
    - Based on results, determine if should scale this and make a Neighbourly2.0

# Stage 1 & 2
I am mostly learning as much as I can at these stages so not much to say.

# Stage 3
I split the development of the main.py file in to 3 parts.

1. Top level conversation handler (main menu)
2. Second level conversation handler
    - Food chain
    - Service chain
3. Firebase database for capturing feedback

In the stage 3 folder, you can find all the files to be able to work independently. The food_chain.py and svc_chain.py files each runs a conversation handler locally. The pyrebase.py file teaches me how to upload to firebase via a few simple commands. The pyrebase documentation is [here](https://github.com/thisbejim/Pyrebase).

## Structure of second level conversation handlers
Each question I wish to ask my users represent a state in the statemachine. For example in the food_chain.py:
```
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
```
Each user's reply to the questions are stored in the context.user_data as a dictionary:
```
food = {'role':None, 'what':None, 'where':None, 'when_purchase':None, 'when':None, 'price':None}

ud = context.user_data
ud = food
ud['price'] = str(update.message.text)
```
Upon confirmation, the requests will be posted to the main channel
```
context.bot.send_message(chat_id='@ReplaceMe', text='ReplaceMe')
```

# Stage 4
Posting on this initiative in neighbouring HDB lift blocks to test if people will join.
<img src="neighbourly%20updated.jpg" width="400">
- Day 1 (2blocks): 
    - 1 subscribed to channel! YAS ^^
- Day 2 (5blocks):
    - 7 subscribed + FIRST person who posted on the channel with the bot!! (proves that someone know how to use the bot!! YASS ^^)
- Day 3 (9blocks):
    - 21 subscribed + same person as previous day posted again! (proves that the free bot timing out is not too big an issue!)
- Day 4 (10blocks):
    - 29 subscribed + 3 new people posted to the channel
- Day 7:
    - 40+ users! :)
- Day 16:
    - 60+ users!

# Moving forward
16 days into launching Neighbourly 1.0: I have learned a lot through this project. Seeing actual users using the platform compelled me to think more about how to scale this. My number one issue will be how to demarcate groups. For example, there can be instances where the building right beside me belongs to another telegram channel. In the end, I will have to create many channels. Instead, I asked if there is a way I can have messages only sent to those within a **certain radius** of where I stay. Hence forth, Neighbourly2.0 is born!

# Neighbourly 2.0
Main Uncertainties:
- Can a bot send messages privately to specific users?
- Is there a way which I can blast my message out to only those 300m from me?
- Will my current users stick to the older platform or switch over?
- What are the limits of Heroku, Firebase realtime database and telegram api? How does this affect user experience?
- How do I scale (commercialisation plan)? I will have the achieve critical mass everytime beyond certain radius distance

Update: I have addressed the first 4 uncertainties and launched Neighourly2.0! I have joined a team to make this more successful and so will not be disclosing too much information. Do look out for us as we strive to create a better future for everyone.


# Known minor problems/issues
1. (telegram api) I am unable to reply text if the function is answering a callbackquery. I am only able to edit existing text. This can be found in the what_food_r function inside main.py
```
update.message.reply_text('testing message')    # this gives an error
query.edit_message_text(text = '')              # this can only edit text
```
