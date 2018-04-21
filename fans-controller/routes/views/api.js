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

			fan.state = 'idle';
			fan.address = ip;
			fan.save((err, saveResult) => {
				if (err) {
					return res.json({ error: err });
				}
				res.json({ status: 'success', ts: new Date().getTime() });
			});
		});
	},

	GetAction: function (req, res) {
		console.log('Get Action: ' + JSON.stringify(req.body));	
		let fanId = req.body.fanId;
		let state = req.body.state;
		if (!fanId || !state) {
			return res.json({ error: 'Didn\'t get a fanId and state' });
		}
		Fan.model.findOne({ fanId }, (err, fan) => {
			if (err) {
				console.log(err);
				return res.json({ error: err });
			}
			if (!fan) {
				return res.json({ error: 'Couldn\'t find fan' });
			}

			fan.state = state; //'offline', 'idle', 'loading', 'loaded', 'drawing'
			fan.save((err, saveResult) => {

				ServerSettings.model.findOne({ }, (err, serverSettings) => {
					Fan.model.find({}, (err, fans) => {
						if (serverSettings.state === 'fans_idle') {
							console.log(JSON.stringify(fans, null, 4));
							if (areAllAtState(fans, 'idle')) {
								serverSettings.state = 'fans_loading';
								serverSettings.save();
							}
							return res.json({ status: 'success', action: 'idle' });
						}
						else if (serverSettings.state === 'fans_loading') {
							if (areAllAtState(fans, 'loaded')) {
								serverSettings.state = 'fans_drawing';
								serverSettings.save();
							}
							return res.json({ status: 'success', action: 'load', animation: serverSettings.animation });
						}
						else if (serverSettings.state === 'fans_drawing') {
							return res.json({ status: 'success', action: 'draw', animation: serverSettings.animation });
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
