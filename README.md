# KTU Notifier

Gives Notifications of KTU announcements from their site using a Telegram Bot ( http://t.me/ktunotifbot )

## Instructions to create your own version of this bot

- Clone the Repo
- Create a new Telegram Bot using BotFather in telegram
- Make a file named .env in the root folder and add the line TOKEN=XXXXXX (Your telegram bot token)
- Run bot.py and send subscribe command, you'll now see new .txt file in sub folder whose name is your Telegram chat id
- Add that chat id to your .env file as a line ADMIN=XXXXX (XXXXX is chat id)
- Your bot should work as long as you have bot.py running
- You can host it to Heroku to run forever using instructions at https://github.com/michaelkrukov/heroku-python-script

### Contributions will be Appreciated :blush:
