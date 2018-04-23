var keystone = require('keystone');
var Types = keystone.Field.Types;

/**
 * Fan Model
 * ==========
 */
var Fan = new keystone.List('Fan');

Fan.add({
	fanId: { type: String, required: false, index: true },
	address: { type: String, required: false, index: false },
	lastUpdate: { type: Types.Datetime, init: Date.now },
	state: { default: 'offline', type: Types.Select, options: ['offline', 'stopped', 'loading', 'loaded', 'drawing'] },
	asset: { type: String, required: false, index: true },
});


/**
 * Registration
 */
Fan.defaultColumns = 'fanId, address, state, asset, lastUpdate';
Fan.register();
