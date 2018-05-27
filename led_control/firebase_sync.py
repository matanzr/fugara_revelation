import pyrebase
import os 
import firebase_admin
from firebase_admin import credentials

# cred = credentials.Certificate("./serviceAccountKey.json")
# firebase = firebase_admin.initialize_app(cred)


# cwd = os.getcwd()

# print(os.getcwd() + "\n")

config = {
  "apiKey": "AIzaSyD7XsUY6ObxE4Z7iLg7rZW-0TZCqK5bvec",
  "authDomain": "fugara-revelations.firebaseapp.com",
  "projectId": "fugara-revelations",
  "databaseURL": "https://fugara-revelations.firebaseio.com",
  "storageBucket": "fugara-revelations.appspot.com",
  "messagingSenderId": "892679996381",
  "serviceAccount": "serviceAccountKey.json",
}
firebase = pyrebase.initialize_app(config)

auth = firebase.auth()
firebase = pyrebase.initialize_app(config)

# Log the user in
user = auth.sign_in_with_email_and_password('arnonhecht@gmail.com', 'noninoni')


storage = firebase.storage()
# as admin
storage.child("images/example.jpg").put("example2.jpg")

# download
storage.child("images/").download("images/")