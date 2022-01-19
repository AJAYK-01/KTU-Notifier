from firebase import Firebase
from decouple import config

config = {
  "apiKey": os.getenv('APIKEY'),
  "authDomain": os.getenv('AUTHDOMAIN'),
  "databaseURL": os.getenv('DATABASEURL'),
  "projectId": os.getenv('PROJECTID'),
  "storageBucket": os.getenv('STORAGEBUCKET')
}

firebase = Firebase(config)

db = firebase.database()

def getData():
    """ Returns the scraped notifications from the Firebase Database as dictionary """
    data = []
    notifs = db.child("notifs").get().val()
    for notif in notifs:
        data.append(notif)
    return data

def setData(data):
    """ Updates the notifications Firebase DB with the new notifications """
    db.child("notifs").set(data)

def users():
    """ Gathers the list of Users from the Firebase Database as a dictionary"""
    users = []
    users = db.child("subs").get()
    return dict(users.val())

def subscribe(chat_id):
    """ Adds the user as a Subscriber in the Firebase Database """
    db.child("subs").child(str(chat_id)).set("T")

def relevantsub(chat_id):
    """ Adds the user as subscriber of Relevant notifications in the Firebase Database """
    db.child("subs").child(str(chat_id)).set("R")

def unsubscribe(chat_id):
    """ Sets the Subscription status of user to False in the Firebase Database """
    db.child("subs").child(str(chat_id)).set("F")
