import sys
import pyrebase
import os 
import firebase_admin
from firebase_admin import credentials
import json

# cred = credentials.Certificate("./serviceAccountKey.json")
# firebase = firebase_admin.initialize_app(cred)


# cwd = os.getcwd()

# print(os.getcwd() + "\n")
print('start')

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

print('init done..')

# Log the user in
user = auth.sign_in_with_email_and_password('arnonhecht@gmail.com', 'noninoni')
print('auth done..')

storage = firebase.storage()
db = firebase.database()
file_structure = db.child("fugara-revelations").get()
print json.dumps(file_structure.val())

for firebase_folder in file_structure.val():
  folder = os.path.join("incoming_images", firebase_folder)
  
  if not os.path.exists(folder):
    os.makedirs(folder)
  for i in range(6):
    firebase_path = "%s/fan_%s-file_%s.zip" % (firebase_folder, i, i)
    local_path = "%s/fan_%s-file_%s.zip" % (folder, i, i)
    print "firebase_path:  %s, local_path: %s" % (firebase_path, local_path)
    try:
      storage.child(firebase_path).download(local_path)
    except Exception as e:
      print "failed. exception: %s" % (sys.exc_info()[0])
      print "Make you sure you've created the 'incoming_images' folder under the current working directory"

# as admin
# storage.child("images/example.jpg").put("example2.jpg")

print('lalala.. Done!')
# storage.child('222/styles.css').download('here.png')
# download