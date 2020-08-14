from telebot import TeleBot, types
from decouple import config
from scrapper import scrape
from apscheduler.schedulers.blocking import BlockingScheduler
import requests
import json
import time

token = config('TOKEN')
bot = TeleBot(token)


def get_contents(chat_id):
    contents = []
    scraped = scrape()
    if scraped != []:
        js = open("data/"+chat_id+"_data.json","r")
        datas = json.load(js)
        for scrap in scraped:
            k = 0
            for data in datas:
            # Can't do a "not in" comparison with dictionary element coz dload links in it are unique to each request
                if data['title'] == scrap['title']:
                    k = 1
                    break   
            
            if k == 0:
                contents.append(scrap)
        js.close()
        js = open("data/"+chat_id+"_data.json","w")
        json.dump(scraped, js, indent=4)
        js.close()
        
        return contents
    else:
        return []

def send_notifs(message):
    """/notifs."""
    chat_id = str(message.chat.id)
    contents = get_contents(chat_id)
    if contents and contents != []:
        for content in contents:
            msg_content = content['date']+'\n\n'+content["title"]+':\n\n'+content["content"]
            for link in content["link"]:
                msg_link_text = "<a href=\""+link["url"]+"\">"+link["text"]+"</a>"
                msg_content += "\n"+msg_link_text
            bot.send_message(
                message.chat.id, msg_content, parse_mode="html",
            )
            
    else:
        pass

@bot.message_handler(commands=["view"])
def fetch_notifs(message):
    contents = scrape()
    for i in range(10):
        content = contents[i]
        msg_content = content['date']+'\n\n'+content["title"]+':\n\n'+content["content"]
        for link in content["link"]:
            msg_link_text = "<a href=\""+link["url"]+"\">"+link["text"]+"</a>"
            msg_content += "\n"+msg_link_text
        bot.send_message(
            message.chat.id, msg_content, parse_mode="html",
        )


def scheduledjob(message):
    
    file2 = open("sub/"+str(message.chat.id)+".txt", "r")
    #checking if unsubscribed
    if file2.read() == "F":
        pass
    else:
        send_notifs(message)
    file2.close()


@bot.message_handler(commands=["subscribe"])
def subscribed(message):
    file1 = open("sub/"+str(message.chat.id)+".txt", "w")
    file1.write("T")
    file1.close()
    scheduler = BlockingScheduler()
    scheduler.add_job(scheduledjob, 'interval', minutes=1, args=[message])
    scheduler.start()

    
                
@bot.message_handler(commands=["unsubscribe"])
def unsubscribed(message):
    file1 = open("sub/"+str(message.chat.id)+".txt", "w")
    file1.write("F")
    file1.close()


@bot.message_handler(commands=["start", "help"])
def send_instructions(message):
    """/start, /help"""
    chat_id = str(message.chat.id)
    js = open("data/"+chat_id+"_data.json","w")
    data = scrape()
    json.dump(data, js, indent=4)
    js.close()
    msg_content = (
        "*Available commands:*\n\n" "/subscribe - Subscribe to KTU Notifs \n\n /unsubscribe - Unsubscribe from KTU Notifs \n\n /view - Fetch latest 10 Notifs from KTU"
    )
    bot.send_message(
        message.chat.id, msg_content, parse_mode="markdown",
    )


bot.polling(none_stop=True)