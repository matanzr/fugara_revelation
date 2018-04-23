var keystone = require('keystone');
var Fan = keystone.list('Fan');
var ServerSettings = keystone.list('ServerSettings');

ServerSettings.model.findOne({ }, (err, serverSettings) => {
	if (!serverSettings) {
		var settings = new ServerSettings.model();
		settings.save();	
	}
});

setInterval(CheckIfAllFansAreOnline, 5000);
setInterval(CheckIfShouldChangeAnimation, 1000);

function CheckIfAllFansAreOnline () {
	Fan.model.find({}, (err, fans) => {
		const MINUTE = 1000 * 60;
		let oneMinuteAgo = Date.now() - MINUTE;
		var allOffline = true;
		fans.forEach(fan => {
			if (fan.lastUpdate < oneMinuteAgo) {
				fan.state = 'offline';
				fan.asset = '';
				fan.save();
			}
			if (fan.state !== 'offline') {
				allOffline = false;
			}
		});
		if (allOffline) {
			ServerSettings.model.findOne({ }, (err, serverSettings) => {
				if (serverSettings.currentState !== 'fans_stopped' && serverSettings.nextAnimation !== serverSettings.animations[0]) {
					serverSettings.currentAnimation = '';
					serverSettings.nextAnimation = '';
					serverSettings.save();
				}
			});
		}
	});
}

function CheckIfShouldChangeAnimation () {
	ServerSettings.model.findOne({ }, (err, serverSettings) => {
		if (serverSettings.currentAnimation === '' && serverSettings.nextAnimation === '') {
			console.log('Restarting 1 ');
			serverSettings.currentState = 'fans_stopped';
			serverSettings.nextAnimation = serverSettings.animations[0];
			serverSettings.save();
		} else if (serverSettings.currentState === 'fans_drawing') {
			if (serverSettings.currentAnimation === '') {
				console.log('Restarting 2');
				console.log(serverSettings);
				serverSettings.currentState = 'fans_stopped';
				serverSettings.nextAnimation = serverSettings.animations[0];
				serverSettings.save();
			} else {
				let x = 1000 * serverSettings.currentAnimationDuration;
				let xMSecondsAgo = Date.now() - x;
				if (serverSettings.currentAnimationStartingTime.getTime() < xMSecondsAgo) {
					console.log('Switching');
					var nextAnimationIndex = serverSettings.animations.indexOf(serverSettings.currentAnimation) + 1;		
					if (nextAnimationIndex === -1) {
						nextAnimationIndex = 0;
					}
					if (nextAnimationIndex >= serverSettings.animations.length) {
						nextAnimationIndex = 0;
					}
					serverSettings.currentState = 'fans_stopped';
					serverSettings.currentAnimation = '';
					serverSettings.nextAnimation = serverSettings.animations[nextAnimationIndex];
					serverSettings.save();
				}
			}
		}
	});
};
