from telebot import TeleBot
# from decouple import config
from scrapper import scrape
from db import subscribe, unsubscribe, users, relevantsub, getData, setData
from apscheduler.schedulers.background import BackgroundScheduler
from nlp import relevant
import requests
import time
import os

token = os.environ['TOKEN']
bot = TeleBot(token)

admin = os.environ['ADMIN']
notifs = getData()


def get_contents():
    """
        Checks for changes in ktu site and returns the new notifs
    """
    global notifs
    contents = []
    scraped = scrape()
    if scraped != []:
        datas = notifs
        for scrap in scraped:
            k = 0
            for data in datas:
                # Can't do a "not in" comparison with dictionary element coz download links inside it are
                # unique to each request
                if data['title'] == scrap['title'] and data['date'] == scrap['date']:
                    k = 1
                    break

            if k == 0:
                relevance = relevant(scrap['content'])
                contents.append(
                    dict({'data': scrap, 'relevance': str(relevance)}))

        notifs = scraped
        return contents
    else:
        return []


def send_notifs(chat_id, contents, value):
    """ Sends the newly scraped notification to individual users
    based on Relevance if user has opted"""

    for content in contents:
        relevance = content['relevance']
        content = content['data']

        """ Checking for Relevance using ML and also whether user wants all notifs """
        if relevance == '1' or value == 'T':
            msg_content = content['date']+'\n\n' + \
                content["title"]+':\n\n'+content["content"]
            for link in content["link"]:
                # telegram supports html like hyperlinks!! :)
                msg_link_text = "<a href=\"" + \
                    link["url"]+"\">"+link["text"]+"</a>"
                msg_content += "\n"+msg_link_text
            bot.send_message(
                int(chat_id), msg_content, parse_mode="html",
            )


def scheduledjob():
    """ Send new notifications that come on KTU site. \n
        Checks subscription status of each user from Firebase Realtime Database and sends notifs
        to subscribers
    """

    contents = get_contents()
    if contents and contents != []:
        for key, value in users().items():
            chat_id = key
            """ checking if unsubscribed and send the notification """
            if value != "F":
                send_notifs(chat_id, contents, value)

        setData(notifs)


@bot.message_handler(commands=["view"])
def fetch_notifs(message):
    """ view """
    contents = scrape()

    # If dumb KTU is down as expected, fetch from previously scraped data
    if contents == [] or not contents:
        contents = notifs

    for i in range(10):
        content = contents[i]
        msg_content = content['date']+'\n\n' + \
            content["title"]+':\n\n'+content["content"]
        for link in content["link"]:
            # telegram supports html like hyperlinks!! :)
            msg_link_text = "<a href=\""+link["url"]+"\">"+link["text"]+"</a>"
            msg_content += "\n"+msg_link_text
        bot.send_message(
            message.chat.id, msg_content, parse_mode="html",
        )


@bot.message_handler(commands=["subscribe"])
def subscribed(message):
    """ subscribe """

    subscribe(message.chat.id)
    bot.send_message(
        message.chat.id, "Subscribed!!", parse_mode="markdown",
    )


@bot.message_handler(commands=["filtered"])
def filtered(message):
    """ subscribe for relevant notifs only """

    relevantsub(message.chat.id)
    bot.send_message(
        message.chat.id, "Subscribed to Relevant Notiications (*Beta*)", parse_mode="markdown",
    )


@bot.message_handler(commands=["unsubscribe"])
def unsubscribed(message):
    """ unsubscribe """

    unsubscribe(message.chat.id)
    bot.send_message(
        message.chat.id, "Unsubscribed", parse_mode="markdown",
    )


@bot.message_handler(commands=["start"])
def send_instructions(message):
    """/start"""
    msg_content = (
        "*Available commands:*\n\n /subscribe - Subscribe to KTU Notifs \n\n /filtered - Subscribe to *only Relevant* KTU Notifs (*Beta*) \n\n /unsubscribe - Unsubscribe from KTU Notifs \n\n /view - Fetch latest 10 Notifs from KTU \n\n /code - View source code GitHub"
    )
    bot.send_message(
        message.chat.id, msg_content, parse_mode="markdown",
    )


@bot.message_handler(commands=["code"])
def start_bot(message):
    """code - Displays link to Github repo of this project"""

    bot.send_message(
        message.chat.id, "View the complete code at \n\n https://github.com/AJAYK-01/ktu-notifier ", parse_mode="markdown",
    )


def ping_repl():
    """ ping flask server in replit to avoid sleeping of the bot """
    repl_res = requests.get("https://ktu-notif.telegramgdrive.repl.co")
    print(str(repl_res))


# first executions
ping_repl()
scheduledjob()

scheduler = BackgroundScheduler()
scheduler.add_job(scheduledjob, 'interval', minutes=10)
scheduler.add_job(ping_repl, 'interval', seconds=20)
scheduler.start()

# infinity_polling to prevent timeout to telegram api
bot.infinity_polling(True)
