var keystone = require('keystone');
var Fan = keystone.list('Fan');
var ServerSettings = keystone.list('ServerSettings');

exports = module.exports = {
	Register: function (req, res) {
		console.log('Register: ' + JSON.stringify(req.body));
		let fanId = req.body.fanId;
		if (!fanId) {
			return res.json({ error: 'Didn\'t get a fanId' });
		}

		Fan.model.findOne({ fanId: fanId }, (err, fan) => {
			if (err) {
				return res.json({ error: err });
			}

			if (!fan) {
				fan = new Fan.model({
					fanId: fanId,
				});
			}
			let ip = req.ip;
			if (ip.substr(0, 7) === '::ffff:') {
				ip = ip.substr(7);
			}
			fan.state = 'stopped';
			fan.address = ip;
			fan.lastUpdate = Date.now();
			fan.save((err, saveResult) => {
				if (err) {
					return res.json({ error: err });
				}
				res.json({ status: 'success', ts: new Date().getTime() });
			});
		});
	},

	GetAction: function (req, res) {
		// console.log('Get Action: ' + JSON.stringify(req.body));	
		let fanId = req.body.fanId;
		let state = req.body.state;
		let asset = req.body.asset;
		if (!fanId || !state) {
			return res.json({ error: 'Didn\'t get a fanId, state' });
		}
		Fan.model.findOne({ fanId }, (err, fan) => {
			if (err) {
				return res.json({ error: err });
			}
			if (!fan) {
				return res.json({ error: 'Couldn\'t find fan' });
			}

			fan.state = state; //'offline', 'stopped', 'loading', 'loaded', 'drawing'
			fan.asset = asset;
			fan.lastUpdate = Date.now();
			fan.save((err, saveResult) => {
				ServerSettings.model.findOne({ }, (err, serverSettings) => {
					Fan.model.find({ state: { $ne: 'offline' } }, (err, fans) => {
						if (serverSettings.currentState === 'fans_stopped') {
							if (areAllAtState(fans, 'stopped')) {
								serverSettings.currentState = 'fans_loading';
								serverSettings.save();
							}
							return res.json({ status: 'success', action: 'stop' });
						}
						else if (serverSettings.currentState === 'fans_loading') {
							if (areAllAtState(fans, 'loaded')) {
								serverSettings.currentState = 'fans_drawing';
								serverSettings.currentAnimation = serverSettings.nextAnimation;
								serverSettings.currentAnimationDuration = serverSettings.durations[serverSettings.animations.indexOf(serverSettings.currentAnimation)];
								serverSettings.currentAnimationStartingTime = Date.now();
								serverSettings.save();
							}
							return res.json({ status: 'success', action: 'load', animation: serverSettings.nextAnimation });
						}
						else if (serverSettings.currentState === 'fans_drawing') {
							return res.json({ status: 'success', action: 'draw', animation: serverSettings.currentAnimation });
						}
					});
				});
			});
		});
	},
};

function areAllAtState (fans, requiredState) {
	let result = true;
	fans.forEach(fan => {
		if (fan.state !== requiredState) {
			result = false;
		}
	});
	return result;
}
