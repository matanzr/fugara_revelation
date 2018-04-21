var keystone = require('keystone');
var Types = keystone.Field.Types;

/**
 * ServerSettings Model
 * ==========
 */
var ServerSettings = new keystone.List('ServerSettings');

ServerSettings.add({
	animation: { type: String, required: false, index: false },
	state: { default: 'fans_idle', type: Types.Select, options: ['fans_idle', 'fans_loading', 'fans_drawing'] },
});

// ServerSettings.schema.pre('update', next => {
// 	var modified_paths = this.modifiedPaths();
// 	console.log(modified_paths);
// 	next();
// });


/**
 * Registration
 */
ServerSettings.defaultColumns = 'animation, state';
ServerSettings.register();
