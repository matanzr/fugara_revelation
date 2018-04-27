var keystone = require('keystone');
var Types = keystone.Field.Types;

/**
 * ServerSettings Model
 * ==========
 */
var ServerSettings = new keystone.List('ServerSettings');

ServerSettings.add({
	currentState: { init: 'fans_stopped', type: Types.Select, options: ['fans_stopped', 'fans_loading', 'fans_drawing'] },
	currentAnimation: { type: String, required: false, index: false },
	currentAnimationDuration: { type: Number, required: false, index: false },
	currentAnimationStartingTime: { type: Types.Datetime, init: Date.now },
	nextAnimation: { type: String, required: false, index: false },
	animations: { type: Types.TextArray },
	durations: { type: Types.NumberArray },
});

ServerSettings.schema.pre('validate', function (next) {
	if (this.animations.length !== this.durations.length) {
		return next(new Error('Animations and durations array aren\'t the same size'));
	}
	next();
  });

/**
 * Registration
 */
ServerSettings.defaultColumns = 'animation, state';
ServerSettings.register();
