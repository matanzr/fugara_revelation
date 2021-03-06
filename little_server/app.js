const express = require('express')
const app = express()
var fs = require('fs');

SEQ_PATH = "../led_control/incoming_images/"

var bodyParser = require('body-parser')
const exec = require('child_process').exec;


app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());
app.use('/', express.static('public'))

var max_timeout = 30;

var dir_list = fs.readdirSync(SEQ_PATH);
var sequences = [];
for (var i=0; i < dir_list.length; i++) {
  if (fs.statSync(SEQ_PATH + dir_list[i]).isDirectory()) {
    sequences.push(dir_list[i]);
  }
}

var playlist = []
fs.readFile('./playlist.json', 'utf8', function (err, data) {
    if (err) throw err;
    playlist = JSON.parse(data);
  }
);

var playlist = [
  { asset: "eagle", duration: 40 },
  { asset: "cube", duration: 40 },
  { asset: "tunnel", duration: 40 },
  { asset: "testgif1", duration: 40 },
  { asset: "testgif2", duration: 40 },
  { asset: "testgif3", duration: 40 }
];

for (var i=0; i < playlist.length; i++) {
  max_timeout = Math.max(playlist[i].duration, max_timeout);
}
max_timeout = (max_timeout + 5) * 1000;

var current_asset_index = 0;
var current_server_state = "fans_stopped"; //'fans_stopped'\'fans_loading'\'fans_drawing'
var current_animation_starting_time;

var online_fans = {
  // dummy_fan: {
  //   state: "stoped", //"stoped"/"loading"/"playing"
  //   ip: "0.0.0.0",
  //   last_ping_date: new Date(),
  //   asset: ""
  // }
}




// app.get('/', (req, res) => res.send('Server up!'))
app.post('/register', (req, res) => {
		let fanID = req.body.fanId; if (!fanID) { return res.json({ error: 'Didn\'t get a fanId' }); }

    let ip = req.ip;
    if (ip.substr(0, 7) === '::ffff:') { ip = ip.substr(7); }
    if (online_fans[fanID] === undefined) {
      console.log('Register: ' + JSON.stringify(req.body));
    } else {
      console.log('Reconnected: ' + JSON.stringify(req.body)); // TODO: Update with data that wont hurt the circle
    }

    online_fans[fanID] = {
      state: "connected",
      ip: ip,
      last_ping_date: new Date(),
      asset: ""
    }
    res.json({ status: 'success', ts: new Date().getTime() });
});

app.post('/action', (req, res) => {
    let fanID = req.body.fanId; if (!fanID) { return res.json({ error: 'Didn\'t get a fanId' }); }
    let state = req.body.state; if (!fanID) { return res.json({ error: 'Didn\'t get a state' }); }
    let asset = req.body.asset; if (!fanID) { return res.json({ error: 'Didn\'t get a asset' }); }
    if (online_fans[fanID] === undefined) { return res.json({ error: 'Couldn\'t find fan' }); }

    online_fans[fanID].asset = asset;
    online_fans[fanID].last_ping_date = new Date();
    if (online_fans[fanID].state === "connected" && current_server_state !== 'fans_stopped') {
      return res.json({ status: 'success', action: 'idle' });
    }
    online_fans[fanID].state = state;

    if (current_server_state === 'fans_stopped') {
	     if (areAllAtState('idle')) {
         if(checkIfSomeAreConnected()) {
           console.log("Waiting for new fans..")
         } else {
           current_server_state = 'fans_loading';
           current_asset_index++;
           if (current_asset_index >= playlist.length) {
               current_asset_index = 0;
           }
           console.log("Telling fans to Load", playlist[current_asset_index] )
         }
				}

				return res.json({ status: 'success', action: 'idle' });
			}
			else if (current_server_state === 'fans_loading') {
				if (areAllAtState('loaded')) {
          console.log("Telling fans to Draw", playlist[current_asset_index])
					current_server_state = 'fans_drawing';
					current_animation_starting_time = Date.now();
				}
				return res.json({ status: 'success', action: 'load', animation: playlist[current_asset_index].asset });
			}
			else if (current_server_state === 'fans_drawing') {
        if ((new Date() - current_animation_starting_time)/1000 > playlist[current_asset_index].duration) {
            console.log("Telling fans to Stop")
            current_server_state = 'fans_stopped';
        }
				return res.json({ status: 'success', action: 'draw', animation: playlist[current_asset_index].asset, length: playlist[current_asset_index].duration });
			}
});

app.get('/status', (req, res) => {
    res.json({
      current_asset_index: current_asset_index,
      current_server_state: current_server_state,
      current_animation_starting_time: current_animation_starting_time,
      playlist: playlist,
      online_fans: online_fans
    });
});

app.post('/update_playlist', (req,res) => {
  playlist = req.body['playlist'];
  for (var i =0; i< playlist.length; i++) {
    playlist[i].duration = parseInt(playlist[i].duration)
  }
  console.log(playlist);
  fs.writeFile ('./playlist.json', (JSON.stringify(playlist)), function(err) {
    if (err) throw err;
    console.log('complete');
  }
  );
});


app.get('/server_command', (req, res) => {
  var command = req.query.type;

  exec('../sync_clinets.sh '+ command, (e, stdout, stderr)=> {
    console.log('stdout ', stdout);
    console.log('stderr ', stderr);
  });

  res.json({
     msg: "launched command"
  });
});

app.get('/sequences', (req, res) => {
  res.json({
    list: sequences
  });
});

app.listen(3000, () => console.log('Listening on port 3000'))


function areAllAtState (requiredState) {
	let result = true;
  for (var fanID in online_fans) {
    const fan = online_fans[fanID];
    if (fan.state !== requiredState && fan.state !== "connected") {
			result = false;
		}
  }
	return result;
}

function checkIfSomeAreConnected () {
	let result = false;
  for (var fanID in online_fans) {
    const fan = online_fans[fanID];
    if (fan.state === "connected") {
			result = true;
		}
  }
	return result;
}


// Removing all fans that didn't send anything
setInterval(function() {
  var all_in_connected_state = true;
  for (var fanID in online_fans){
    if (online_fans[fanID].state != "connected") {
        all_in_connected_state = false;
    }
    var should_remove = false;
    if (new Date() - online_fans[fanID].last_ping_date > max_timeout) { should_remove = true; }
    if (should_remove) {
      delete online_fans[fanID];
      console.log("Removed fan with id: " + fanID);
      console.log("current_server_state: " + current_server_state);
    }
  }
  if (online_fans.length == 0 || all_in_connected_state) {
    current_asset_index = 0;
    current_server_state = "fans_stopped";
    current_animation_starting_time;
  }
}, 1000);


var reboot_interval = 2 * 60 * 1000;

setInterval(function() {
  exec('../sync_clinets.sh reboot');
}, reboot_interval);
