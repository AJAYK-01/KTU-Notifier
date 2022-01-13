# KTU Notifier

#### The Easiest Way [Heroku ONLY 👾]

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

Gives Notifications of KTU announcements from their site using a Telegram Bot ( http://t.me/ktunotifbot )

## Workflow
<img src="https://github.com/AJAYK-01/ktu-notifier/blob/master/screenshots/Workflow.png" />

## Instructions to create your own version of this bot

- Clone the Repo.
- Install the requirements.txt using pip.
- Create a new Telegram Bot using BotFather in telegram.
- Create a Firebase Realtime Database for handling subscribers and storing notifications cache.
- Make a file named .env in the root folder and add the line TOKEN=XXXXXX (Your telegram bot token).
- Also add the firebase credentials to the .env file.
- Run bot.py in your system and you'll see that the bot starts responding to commands on Telegram.
- Your bot should work as long as you have bot.py running.
- You can host it to Heroku to run forever using instructions at https://github.com/michaelkrukov/heroku-python-script.

#### Big thanks to [@nandakishormpai2001](https://github.com/nandakishormpai2001) for adding an NLP based filterer that checks for relevancy of each KTU Notification

## Screenshot of .env file

<img src="https://github.com/AJAYK-01/ktu-notifier/blob/master/screenshots/env-screenshot.png" />

#### Contributions will be Appreciated :blush:
