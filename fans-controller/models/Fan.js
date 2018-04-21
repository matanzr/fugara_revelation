var keystone = require('keystone');
var Types = keystone.Field.Types;

/**
 * Fan Model
 * ==========
 */
var Fan = new keystone.List('Fan');

Fan.add({
	name: { type: String, required: false, index: false },
	address: { type: String, required: false, index: false },
	state: { default: 'offline', type: Types.Select, options: ['offline', 'idle', 'loading', 'loaded', 'drawing'] },
	fanId: { type: String, required: false, index: true },
});


/**
 * Registration
 */
Fan.defaultColumns = 'name, fanId, address, state';
Fan.register();
