from firebase import Firebase
from decouple import config

config = {
  "apiKey": config('APIKEY'),
  "authDomain": config('AUTHDOMAIN'),
  "databaseURL": config('DATABASEURL'),
  "projectId": config('PROJECTID'),
  "storageBucket": config('STORAGEBUCKET')
}

firebase = Firebase(config)

db = firebase.database()

def users():
    """ Gathers the list of Users from the Firebase Database as a dictionary"""
    users = []
    users = db.child("subs").get()
    return dict(users.val())

def subscribe(chat_id):
    """ Adds the user as a Subscriber in the Firebase Database """
    db.child("subs").child(str(chat_id)).set("T")

def unsubscribe(chat_id):
    """ Sets the Subscription status of user to False in the Firebase Database """
    db.child("subs").child(str(chat_id)).set("F")