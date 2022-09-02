""" Flask server is needed for hosting this bot on replit """
import subprocess
import shlex
from flask import Flask
app = Flask('app')

# Checks for and Kills any duplicate instances of bot running
cmd1 = subprocess.Popen(["pgrep", "-f", "bot.py"], stdout=subprocess.PIPE)
cmd2 = subprocess.run(['xargs', 'kill'], stdin=cmd1.stdout)

print(str(cmd2))

# Spawns an instance of the bot as a subprocess
cmd = "python bot.py"
cmds = shlex.split(cmd)
p = subprocess.Popen(cmds, start_new_session=True)
print(str(p))


@app.route('/')
def hello_world():
    return 'Hello, I am flask server for a telegram bot on replit!'


app.run(host='0.0.0.0', port=8080)
