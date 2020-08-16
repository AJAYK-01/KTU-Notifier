# KTU Notifier

Gives Notifications of KTU announcements from their site using a Telegram Bot ( http://t.me/ktunotifbot )

## Instructions to create your own version of this bot

- Clone the Repo
- Install the requirements.txt using pip
- Create a new Telegram Bot using BotFather in telegram
- Create a Firebase Realtime Database for handling subscribers
- Make a file named .env in the root folder and add the line TOKEN=XXXXXX (Your telegram bot token)
- Also add the firebase credentials to the .env file
- Run bot.py and send subscribe command, you'll now see a new entry in your Firebase database which is your Telegram chat id
- Add that chat id to your .env file as a line ADMIN=XXXXX (XXXXX is chat id) (This is done to ensure that only your telegram account can start the web scraping scheduler in the bot)
- Your bot should work as long as you have bot.py running
- You can host it to Heroku to run forever using instructions at https://github.com/michaelkrukov/heroku-python-script

## Screenshot of .env file

<img src="https://github.com/AJAYK-01/ktu-notifier/blob/master/screenshots/env-screenshot.png" />

#### Contributions will be Appreciated :blush:
