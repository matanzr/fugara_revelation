import Queue, threading, time, os, sys
from flask import Flask, render_template, redirect, url_for, request
from werkzeug.utils import secure_filename
import zipfile
import playlist
sys.path.insert(0, '../led_control')

from pov_fan import PovFan

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = "./uploads"
app.config['FAN_SEQUENCE_FOLDER'] = "../led_control/incoming_images"


action_q = Queue.Queue()
response_q = Queue.Queue()
current_action = [None]

playlist = playlist.Playlist()

def worker():
    while True:
        item = action_q.get()
        current_action[0] = item

        current_track = playlist.getTrack()

        pov_fan = PovFan()
        pov_fan.images_folder = app.config['FAN_SEQUENCE_FOLDER']
        print "load sequence ", current_track[0]
        pov_fan.load_sequence(current_track[0], 1)
        print "play sequence ", current_track[2]
        pov_fan.play(current_track[2])

        playlist.nextTrack()
        action_q.task_done()

t = threading.Thread(target=worker)
t.daemon = True
t.start()

action_q.join()

def handle_new_sequence(zipfile_path, name, id=1):
    zip_ref = zipfile.ZipFile(zipfile_path, 'r')

    dest_folder = os.path.join(app.config['FAN_SEQUENCE_FOLDER'], name, "fan_" + id)
    # clean destination folder
    for the_file in os.listdir(dest_folder):
        print the_file
        try:
            path = os.path.join(dest_folder, the_file)
            if os.path.isfile(path):
                os.unlink(path)
        except Exception as e:
            print(e)

    
    zip_ref.extractall(dest_folder)
    zip_ref.close()

    os.remove(zipfile_path)


@app.route("/")
def main_page():
    action_list = list(action_q.queue)

    sequence_list = []
    for seq in os.listdir(app.config['FAN_SEQUENCE_FOLDER']):
        seq_path = os.path.join(app.config['FAN_SEQUENCE_FOLDER'], seq)
        if os.path.isdir(seq_path): 
            sequence_list.append(seq)

    return render_template('main.html', actions=action_list,
                                        current=current_action[0],
                                        sequences=sequence_list,
                                        playlist=playlist.list)

@app.route("/upload", methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        filename = secure_filename(file.filename)

        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        handle_new_sequence(file_path, request.form['name'])
        return redirect(url_for('upload',
                            filename=filename))

    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new sequence (!!! should be already converted !!!) </h1>
    <form method=post enctype=multipart/form-data>
      name: <input type=text name=name>
      id: <input type=number name=id>
      <br/>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''

@app.route("/playlist/add", methods=['POST'])
def playlist_add():
    playlist.add(request.form['seq'], 1, request.form['length'])
    return redirect('/')

@app.route("/action/<action>")
def do_action(action):
    action_q.put(action)
    
    return redirect(url_for('main_page'))
