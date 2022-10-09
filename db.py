from firebase import Firebase
# from decouple import config
import os

config = {
    "apiKey": os.environ['APIKEY'],
    "authDomain": os.environ['AUTHDOMAIN'],
    "databaseURL": os.environ['DATABASEURL'],
    "projectId": os.environ['PROJECTID'],
    "storageBucket": os.environ['STORAGEBUCKET']
}

firebase = Firebase(config)

db = firebase.database()


def getData():
    data = []
    notifs = db.child("notifs").get().val()
    for notif in notifs:
        data.append(notif)
    return data


def setData(data):
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
