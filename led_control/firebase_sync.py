import sys
import pyrebase
import os 
import firebase_admin
from firebase_admin import credentials
import json
import shutil
import zipfile

TARGET_FOLDER = "incoming_images"

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

# clean
if os.path.exists(TARGET_FOLDER):
  shutil.rmtree(TARGET_FOLDER)
os.mkdir(TARGET_FOLDER)

file = open( os.path.join(TARGET_FOLDER, "README.md"), "w")
file.write("This folder is for incoming images downloaded by 'firebase_sync.py'")
file.close()

for firebase_folder in file_structure.val():
  folder = os.path.join(TARGET_FOLDER, firebase_folder)
  
  if not os.path.exists(folder):
    os.makedirs(folder)
  for i in range(6):
    fan_file = "fan_%s-file_%s.zip" % (i,i) # TODO: what's the meaning of file number in zip?

    firebase_path = os.path.join(firebase_folder, fan_file)
    local_path = os.path.join(folder, fan_file)

    try:
      storage.child(firebase_path).download(local_path)
      print "Got firebase_path: %s, written local_path: %s" % (firebase_path, local_path)
      zip_ref = zipfile.ZipFile(local_path, 'r')
      zip_ref.extractall(folder)
      zip_ref.close()

    except Exception as e:
      print fan_file, "download failed. exception: %s" % (sys.exc_info()[0])

# as admin
# storage.child("images/example.jpg").put("example2.jpg")

print('lalala.. Done!')
# storage.child('222/styles.css').download('here.png')
# download