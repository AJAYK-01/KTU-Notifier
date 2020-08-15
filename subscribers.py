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
    users = []
    users = db.child("subs").get()
    # print(users.val())
    return dict(users.val())

def subscribe(chat_id):
    db.child("subs").child(str(chat_id)).set("T")

def unsubscribe(chat_id):
    db.child("subs").child(str(chat_id)).set("F")