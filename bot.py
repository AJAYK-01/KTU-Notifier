from telebot import TeleBot, types
import requests
from scrapper import scrape

bot = TeleBot("1357670474:AAG00NzfMKT578_qJY3bDnbPjbLW8VImfIo")


def get_contents():
    contents = scrape()
    return contents

@bot.message_handler(commands=["notifs"])
def send_random_article(message):
    """/notifs."""
    contents = get_contents()
    i = 0
    for content in contents:
        if i < 5:
            msg_content = content["title"]
            for link in content["link"]:
                msg_link_text = "<a href=\""+link["url"]+"\">"+link["text"]+"</a>"
                msg_content += "\n"+msg_link_text
            bot.send_message(
                message.chat.id, msg_content, parse_mode="html",
            )
            i += 1
        else:
            break


@bot.message_handler(commands=["start", "help"])
def send_instructions(message):
    """/start, /help"""
    msg_content = (
        "*Available commands:*\n\n" "/notifs - get first 5 ktu announcements (wait some time after giving command)"
    )
    bot.send_message(
        message.chat.id, msg_content, parse_mode="markdown",
    )


bot.polling(none_stop=True)