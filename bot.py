import logging
from flask import Flask, request
from queue import Queue
from telegram.ext import Updater, MessageHandler, CommandHandler, Filters, Dispatcher
from telegram import Bot, Update, ParseMode, ReplyKeyboardMarkup
import os
import dialogflow_v2 as dialogflow
import subprocess
from utils import video_links, compiler, topics_key

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = 'BOT_TOKEN'

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello!"

@app.route(f'/{TOKEN}', methods={'GET', 'POST'})
def webhook():
    update = Update.de_json(request.get_json(), bot)
    dp.process_update(update)
    return "ok"




os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "client.json"

df_session_client = dialogflow.SessionsClient()
PROJECT_ID = "PROJECT_ID"

def detect_intent_from_text(text, session_id, lang='en'):
    session = df_session_client.session_path(PROJECT_ID, session_id)
    text_input = dialogflow.types.TextInput(text=text, language_code=lang)
    query_input = dialogflow.types.QueryInput(text=text_input)
    response = df_session_client.detect_intent(session=session, query_input=query_input)
    return response.query_result




def _start(bot, update):
    logger.info("{} {} started chatting".format(update['message']['chat']['first_name'], update['message']['chat']['last_name']))
    user = update.message.from_user.first_name
    reply = "Hi! {}\n".format(user)
    welcome = """I am GeekGod, your guide to basic data structures where you will get to learn about DS + you can also compile your codes and check their outputs.\n\nFor more info-\nReply with "/help" to me.\n<b>I will be happy to help you.</b>"""
    reply += welcome
    bot.send_message(chat_id=update.message.chat_id, text=reply, parse_mode=ParseMode.HTML)



def _help(bot,update):
    help_text = "I have come to save you. What help do you need?\n\n<b>Commands-</b>\n/start - Introduction\n/code - To see how can you compile and run code/script.\n/language - What languages available."
    bot.send_message(chat_id=update.message.chat_id, text=help_text, parse_mode=ParseMode.HTML)



def _language(bot, update):
    reply = "<b>Programming Languages supported-</b>\nC++\nC\nPHP\nJava\nPython"
    bot.send_message(chat_id=update.message.chat_id, text=reply, parse_mode=ParseMode.HTML)



def _learn(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Choose a data structure.",
    reply_markup=ReplyKeyboardMarkup(keyboard=topics_key, one_time_keyboard=True))



def _code(bot, update):
    reply = """Welcome to the compiler, GeekGod here to help you with the codes you have.\n\n/language - To see what languages are supported.\n\nTo compile and check output of the code,
write '!code<space>Language<space>' followed by your code to run.
    
For Example-
    !code C #include<stdio.h>
    int main()
    {
    printf("Hello World");
    }"""

    bot.send_message(chat_id=update.message.chat_id, text=reply)



def text_reply(bot, update):
    ds = {
        'Arrays' : 'array-data-structure/',
        'Linked list' : 'data-structures/linked-list/',
        'Stack' : 'stack-data-structure/',
        'Queue' : 'queue-data-structure/',
        'Binary Tree' : 'binary-tree-data-structure/',
        'Binary Search Tree' : 'binary-search-tree-data-structure/',
        'Heap' : 'heap-data-structure/',
        'Hashing' : 'hashing-data-structure/',
        'Graph' : 'graph-data-structure-and-algorithms/',
        'Advance Data Structure' : 'advanced-data-structures/',
        'Matrix' : 'matrix/',
        'Strings' : 'string-data-structure/'
    }

    lang = {
        "c++": "cpp14",
        "c": "c",
        "php": "php",
        "java": "java",
        "python": "python3"
    }

    text = update.message.text

    lines = text.split(" ")
    if lines[0]=="!code":
        language = lines[1].lower()
        if language in lang.keys():
            count=0
            for idx,char in enumerate(text):
                if count == 2:
                    break

                if char == ' ':
                    count += 1
            
            logger.info("Started compiling...!!!")
            data = compiler(code=text[idx:], lang=lang[language])
            bot.send_message(chat_id=update.message.chat_id, text="<b>Output-</b>\n"+data['output'], parse_mode=ParseMode.HTML)


        else:
            logger.error("{} caused error {}".format(lines[1],"Language not supported"))
            lang_error = "Language not supported. Make sure you have given a valid language. For more info- Text '/language' to the bot"
            bot.send_message(chat_id=update.message.chat_id, text=lang_error)



    else:
        response = detect_intent_from_text(text,update.message.chat_id)
    
        if response.fulfillment_text:
            reply = response.fulfillment_text
            bot.send_message(chat_id=update.message.chat_id, text=reply)
        elif bool(dict(response.parameters)):
            data = dict(response.parameters)
            topic = data['topic']

            logger.info("Fetching data and articles on {}.".format(topic))
            with open("scraper.bat", 'w') as fp:
                fp.write("cd botSpider\n")
                fp.write("scrapy crawl bot -a category="+ds[topic]+'\n')
                fp.write("cd ..\n")

            subprocess.call([r'scraper.bat'])

            with open("botSpider/article.txt",'r') as f:
                reply = f.read()
        
            try:
                bot.send_message(chat_id=update.message.chat_id, text=reply)
                
            except:
                bot.send_message(chat_id=update.message.chat_id, text="Article is too long to display")
            
            logger.info("Getting video information...!!!")
            links = video_links(query=topic+'Data structures')
            for l in links:
                bot.send_message(chat_id=update.message.chat_id, text=l)




def echo_sticker(bot, update):
    bot.send_sticker(chat_id=update.message.chat_id, 
    sticker=update.message.sticker.file_id)




def _error(bot, update, error):
    logger.error("{} has caused error {}.".format(update['message']['text'], error))



bot = Bot(TOKEN)
try:
    bot.set_webhook("https://radiant-mesa-36509.herokuapp.com/" + TOKEN)
except Exception as e:
    print(e)

dp = Dispatcher(bot, Queue())
dp.add_handler(CommandHandler('start', _start))
dp.add_handler(CommandHandler('help', _help))
dp.add_handler(CommandHandler('code', _code))
dp.add_handler(CommandHandler('language', _language))
dp.add_handler(CommandHandler('learn', _learn))
dp.add_handler(MessageHandler(Filters.text, text_reply))
dp.add_handler(MessageHandler(Filters.sticker, echo_sticker))
dp.add_error_handler(_error)

if __name__ == '__main__':
    app.run(port=8443)