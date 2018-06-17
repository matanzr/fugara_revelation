import sys

import os 

import json
import shutil
import zipfile
import glob

TARGET_FOLDER = os.path.join("led_control", "incoming_images")


def sync_firebase(force_update):
  import pyrebase
  import firebase_admin
  from firebase_admin import credentials

  config = {
  "apiKey": "AIzaSyD7XsUY6ObxE4Z7iLg7rZW-0TZCqK5bvec",
  "authDomain": "fugara-revelations.firebaseapp.com",
  "projectId": "fugara-revelations",
  "databaseURL": "https://fugara-revelations.firebaseio.com",
  "storageBucket": "fugara-revelations.appspot.com",
  "messagingSenderId": "892679996381",
  "serviceAccount": os.path.join("led_control","serviceAccountKey.json"),
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
  if force_update:
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
      fan_folder = "%s/fan_%s" % (folder, i+1)
      if not os.path.exists(fan_folder):
        os.makedirs(fan_folder)
      fan_file = "fan_%s.zip" % (i+1) # TODO: what's the meaning of file number in zip?

      firebase_path = os.path.join(firebase_folder, fan_file)
      local_path = os.path.join(fan_folder, fan_file)

      if not os.path.isfile(local_path) or force_update: 
        try:
          storage.child(firebase_path).download(local_path)
          print "Got firebase_path: %s, written local_path: %s" % (firebase_path, local_path)      

        except Exception as e:
          print local_path, "download failed. exception: %s" % (sys.exc_info()[0])
      else:
        print local_path," exists. skipping"


  print('lalala.. Done!')

def extract_all_sequences():
  for seq in glob.glob(os.path.join(TARGET_FOLDER, '*')):
    if os.path.isdir(seq):
      for fan_seq in glob.glob(os.path.join(seq, '*')):
        zips = glob.glob(os.path.join(fan_seq, '*.zip'))
        if len(zips) > 0: 
          zip_ref = zipfile.ZipFile(zips[0], 'r')
          zip_ref.extractall(fan_seq)
          zip_ref.close()
          print "extracted ", zips[0]

def extract_selective_sequences(fans_list):
  for seq in glob.glob(os.path.join(TARGET_FOLDER, '*')):
    if os.path.isdir(seq):
      for fan_seq in glob.glob(os.path.join(seq, '*')):
        zips = glob.glob(os.path.join(fan_seq, '*'+fans_list+'.zip'))
        if len(zips) > 0: 
          zip_ref = zipfile.ZipFile(zips[0], 'r')
          zip_ref.extractall(fan_seq)
          zip_ref.close()
          print "extracted ", zips[0]


if __name__ == "__main__":
  if (len(sys.argv) == 2):
    if sys.argv[1] == 'extract':
      extract_all_sequences()
    if sys.argv[1] == 'force':
      sync_firebase(True)
    else:
      print """ 
      Usage:
      - no args syncs from firebase
      - extract: attempt to extract all zip files in TARGET_FOLDER
      """
  elif (len(sys.argv) == 3):
    if sys.argv[1] == 'extract': 
      extract_selective_sequences(sys.argv[2])
  else:
    sync_firebase(False)
  