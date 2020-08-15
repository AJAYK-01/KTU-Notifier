from telebot import TeleBot, types
from decouple import config
from scrapper import scrape
from apscheduler.schedulers.background import BackgroundScheduler
import requests
import json
import time
import os

#the token is stored in a file named .env in My system. Add your own token or .env file
token = config('TOKEN')
bot = TeleBot(token)

"""Chat id of the admin, so that only he/she can execute the code command 
 after maintanence to start the bot service """
admin = config('ADMIN')


def get_contents():
    """
        Checks for changes in ktu site and returns the new notifs
    """
    contents = []
    scraped = scrape()
    if scraped != []:
        js = open("data.json","r")
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
        js = open("data.json","w")
        json.dump(scraped, js, indent=4)
        js.close()
        
        return contents
    else:
        return []

def send_notifs(chat_id, contents):
    """/notifs."""
    # chat_id = str(message.chat.id)
    # contents = get_contents(chat_id)
    if contents and contents != []:
        for content in contents:
            msg_content = content['date']+'\n\n'+content["title"]+':\n\n'+content["content"]
            for link in content["link"]:
                #telegram supports html like hyperlinks!! :)
                msg_link_text = "<a href=\""+link["url"]+"\">"+link["text"]+"</a>"
                msg_content += "\n"+msg_link_text
            bot.send_message(
                int(chat_id), msg_content, parse_mode="html",
            )
            
    else:
        pass

def scheduledjob():
    """ Send notifications after checking if subscribed or not. \n
        Couldn't figure out a way to use global variables, so instead uses
        variable-like .txt files
    """

    contents = get_contents()
    for filename in os.listdir(os.getcwd()+'/sub/'):
        
        chat_id = filename.split('.')[0]
        filename = 'sub/'+filename
        if filename.split('.')[-1] == "txt":

            with open(filename, "r") as file2:
                
                """ checking if unsubscribed """
                if file2.read() == "F":
                    pass
                else:
                    # print(chat_id)
                    send_notifs(chat_id, contents)
                file2.close()



@bot.message_handler(commands=["view"])
def fetch_notifs(message):
    """ view """
    contents = scrape()
    
    #If dumb KTU is down as expected, fetch from previously scraped data
    if contents == [] or not contents:
        file1 = open('data.json', 'r')
        contents = json.load(file1)
        file1.close()

    for i in range(10):
        content = contents[i]
        msg_content = content['date']+'\n\n'+content["title"]+':\n\n'+content["content"]
        for link in content["link"]:
            #telegram supports html like hyperlinks!! :)
            msg_link_text = "<a href=\""+link["url"]+"\">"+link["text"]+"</a>"
            msg_content += "\n"+msg_link_text
        bot.send_message(
            message.chat.id, msg_content, parse_mode="html",
        )


@bot.message_handler(commands=["subscribe"])
def subscribed(message):
    """ subscribe """
    file1 = open("sub/"+str(message.chat.id)+".txt", "w")
    file1.write("T")
    file1.close()
    bot.send_message(
            message.chat.id, "Subscribed!!", parse_mode="markdown",
    )  

    
                
@bot.message_handler(commands=["unsubscribe"])
def unsubscribed(message):
    """ unsubscribe """
    file1 = open("sub/"+str(message.chat.id)+".txt", "w")
    file1.write("F")
    file1.close()
    bot.send_message(
            message.chat.id, "Unsubscribed", parse_mode="markdown",
    )  


@bot.message_handler(commands=["start"])
def send_instructions(message):
    """/start"""
    msg_content = (
        "*Available commands:*\n\n" "/subscribe - Subscribe to KTU Notifs \n\n /unsubscribe - Unsubscribe from KTU Notifs \n\n /view - Fetch latest 10 Notifs from KTU \n\n /code - View source code GitHub"
    )
    bot.send_message(
        message.chat.id, msg_content, parse_mode="markdown",
    )

@bot.message_handler(commands=["code"])
def start_bot(message):
    """code"""

    if str(message.chat.id) == admin:
        scheduler = BackgroundScheduler()
        scheduler.add_job(scheduledjob, 'interval', minutes=10)
        scheduler.start()
        bot.send_message(
            message.chat.id, "Started service", parse_mode="markdown",
        )   
    
    else:
        bot.send_message(
            message.chat.id, "View the complete code at \n\n https://github.com/AJAYK-01/ktu-notifier ", parse_mode="markdown",
        ) 

#infinity_polling to prevent timeout to telegram api
bot.infinity_polling(True)