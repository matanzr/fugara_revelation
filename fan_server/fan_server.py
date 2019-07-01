import Queue, threading, time, os, sys
is_running_on_pi = os.uname()[4][:3] == 'arm'

if is_running_on_pi:
    os.chdir("/home/pi/dev/fugara_revelation/fan_server")

from flask import Flask, render_template, redirect, url_for, request
from werkzeug.utils import secure_filename
import zipfile
import playlist
import scheduler
sys.path.insert(0, '../led_control')

from pov_fan import PovFan
from pov_fan_cyclic import PovFan as PovFanCyclic
if is_running_on_pi:
    from motor_controller import MotorController

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = "./uploads"
app.config['FAN_PARENT_FOLDER'] = "../led_control/"
app.config['FAN_SEQUENCE_FOLDER'] = "../led_control/incoming_images"
app.config['PLAYLIST_FILE'] = 'playlist.json'
app.config['SCHEDULER_FILE'] = 'scheduler.json'


action_q = Queue.Queue()
response_q = Queue.Queue()
current_action = ["stop"] # used to communicate main thraed what is worker currently doing

playlist = playlist.Playlist()
playlist.load(app.config['PLAYLIST_FILE'])

schedule = scheduler.Scheduler()
schedule.load(app.config['SCHEDULER_FILE'])

def start_motor():
    mc = MotorController()

    if mc.connect():
        print "in connect"
        mc.set_motor_speed(1700)
        mc.sync_speed(5)
        return mc
    else:
        return None

def stop_motor(mc):
    if (mc):
        mc.set_motor_speed(1500)
    else:
        mc = MotorController()
        mc.connect()


def worker():
    last_action = None
    
    while True:        
        time.sleep(1)

        scheduled_task = schedule.isActive() 
        if scheduled_task:
            action_q.put(scheduled_task)
        try:
            last_action = action_q.get(False, 1)
            current_action[0] = last_action
            print "Got new action: ", last_action
        except Queue.Empty:
            pass
        
        if last_action is None: continue

        if not is_running_on_pi: continue
            
        elif last_action == "play":
            current_track = playlist.getTrack()
            mc = start_motor()
            if mc is not None:
                pov_fan = PovFan()
                pov_fan.images_folder = app.config['FAN_PARENT_FOLDER']        
                print "load sequence ", current_track[0]                
                pov_fan.load_sequence(current_track[0], 1)
                print "play sequence ", current_track[2]
                pov_fan.play(float(current_track[2]))
                
                stop_motor(mc)
                playlist.nextTrack()
        
        elif last_action == "play_cyclic":
            current_track = ["endless", "", 400]
            mc = start_motor()
            if mc is not None:
                pov_fan = PovFanCyclic()
                pov_fan.images_folder = app.config['FAN_PARENT_FOLDER']        
                print "load sequence ", current_track[0]                
                pov_fan.load_sequence(current_track[0], 1)
                print "play sequence ", current_track[2]
                pov_fan.play(float(current_track[2]))
                
                stop_motor(mc)
                playlist.nextTrack()
            else:
                print "No motor connect.... check USB connection"
                action_q.put("stop")
                response_q.put("USB ERROR")                

t = threading.Thread(target=worker)
t.daemon = True
t.start()

action_q.join()

def handle_new_sequence(zipfile_path, name, id="1"):
    zip_ref = zipfile.ZipFile(zipfile_path, 'r')

    dest_folder = os.path.join(app.config['FAN_SEQUENCE_FOLDER'], name, "fan_" + id)
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)

    # clean destination folder
    for the_file in os.listdir(dest_folder):
        print the_file
        try:
            path = os.path.join(dest_folder, the_file)
            if os.path.isfile(path):
                os.unlink(path)
        except Exception as e:
            print(e)

    print("Got a new sequece! extracting to ", dest_folder)
    zip_ref.extractall(dest_folder)
    zip_ref.close()

    os.remove(zipfile_path)


@app.route("/")
def main_page():
    action_list = list(action_q.queue)
    resoponse_list = list(response_q.queue)

    sequence_list = []
    for seq in os.listdir(app.config['FAN_SEQUENCE_FOLDER']):
        seq_path = os.path.join(app.config['FAN_SEQUENCE_FOLDER'], seq)
        if os.path.isdir(seq_path): 
            sequence_list.append(seq)

    return render_template('main.html', actions=action_list,
                                        current_action=current_action[0],
                                        sequences=sequence_list,
                                        playlist=playlist,
                                        responses=resoponse_list,
                                        schedule=schedule)

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
    playlist.save(app.config['PLAYLIST_FILE'])
    return redirect('/')
    
@app.route("/playlist/remove/<index>")
def playlist_remove(index):
    playlist.remove(int(index))
    playlist.save(app.config['PLAYLIST_FILE'])
    return redirect('/')


@app.route("/schedule/remove/<index>")
def schedule_remove(index):
    schedule.remove(int(index))
    schedule.save(app.config['SCHEDULER_FILE'])
    return redirect('/')

@app.route("/schedule/add", methods=['POST'])
def schedule_add():
    schedule.add(request.form['schedule'], int(request.form['length']))
    schedule.save(app.config['SCHEDULER_FILE'])
    return redirect('/')

@app.route("/action/<action>")
def do_action(action):
    action_q.put(action)
    
    return redirect(url_for('main_page'))
