var widgets = require('@jupyter-widgets/base');
var _ = require('lodash');


var DOMWidgetModel = widgets.DOMWidgetModel.extend({
    defaults: function() {
	return _.extend(widgets.DOMWidgetModel.prototype.defaults(), {
	    _model_module: 'ipyannotate',
	    _view_module: 'ipyannotate',
	    _model_module_version: '0.1.1',
	    _view_module_version: '0.1.1',
	});
    }
});


var ButtonModel = DOMWidgetModel.extend({
    defaults: _.extend(DOMWidgetModel.prototype.defaults(), {
        _model_name: 'ButtonModel',
        _view_name: 'ButtonView',

	color: undefined,
	icon: undefined,
	label: undefined,
	shortcut: undefined,
    })
});


var ButtonView = widgets.DOMWidgetView.extend({
    initialize: function() {
        ButtonView.__super__.initialize.apply(this, arguments);
    	this.model.on('change:color', this.update_color, this);
    	this.model.on('change:icon', this.update_icon, this);
    	this.model.on('change:label', this.update_label, this);
    	this.model.on('change:shortcut', this.update_shortcut, this);
    	this.model.on('change:active', this.update_active, this);
	this.model.on('msg:custom', this.handle_message, this);
    },

    render: function() {
    	this.button = document.createElement('button');
    	this.button.classList.add('annotate');
    	this.el.appendChild(this.button);

    	this.icon = document.createElement('span');
    	this.icon.classList.add('icon');
    	this.button.appendChild(this.icon);

    	this.label = document.createElement('span');
    	this.label.classList.add('label');
    	this.button.appendChild(this.label);

    	this.shortcut = document.createElement('kbd');
    	this.button.appendChild(this.shortcut);

    	this.update_color();
    	this.update_icon();
    	this.update_label();
    	this.update_shortcut();
	this.update_active();

    	var that = this;
    	this.button.addEventListener('click', function(event) {
            that.click();
    	});
    },

    handle_message: function(content) {
	var event = content.event;
	if (event == 'click') {
	    this.click();
	}
    },

    click: function() {
	this.send({'event': 'click'});
    },

    update_color: function() {
    	var previous = this.model.previous('color');
    	this.button.classList.remove(previous);
    	var color = this.model.get('color');
    	this.button.classList.add(color);
    },

    update_icon: function() {
    	this.icon.textContent = this.model.get('icon')
    },

    update_label: function() {
    	this.label.textContent = this.model.get('label')
    },

    update_shortcut: function() {
    	this.shortcut.textContent = this.model.get('shortcut');
    },

    update_active: function() {
	var active = this.model.get('active');
	this.button.classList.toggle('active', active);
    }
});


var ToolbarModel = DOMWidgetModel.extend({
    defaults: _.extend(DOMWidgetModel.prototype.defaults(), {
        _model_name: 'ToolbarModel',
        _view_name: 'ToolbarView',

	buttons: [],
    })
}, {
    serializers: _.extend({
        buttons: {deserialize: widgets.unpack_models},
    }, DOMWidgetModel.serializers)
});


var ToolbarView = widgets.DOMWidgetView.extend({
    initialize: function() {
        ToolbarView.__super__.initialize.apply(this, arguments);
	this.button_views = new widgets.ViewList(
	    this.create_button_view,
	    this.remove_button_view,
	    this
	);
	this.model.on('change:buttons', this.update_buttons, this);
    },

    render: function() {
    	this.buttons = document.createElement('div');
    	this.el.appendChild(this.buttons);

    	this.update_buttons();
    },

    create_button_view: function(model) {
    	var that = this;
    	return this.create_child_view(model).then(function (view) {
            that.buttons.appendChild(view.button);
            return view;
        });
    },

    remove_button_view: function(view) {
    	this.buttons.removeChild(view.button);
    	view.remove();
    },

    update_buttons: function() {
    	var buttons = this.model.get('buttons');
    	this.button_views.update(buttons);
    },
})


var ProgressModel = DOMWidgetModel.extend({
    defaults: _.extend(DOMWidgetModel.prototype.defaults(), {
        _model_name: 'ProgressModel',
        _view_name: 'ProgressView',

	atoms: [],
    })
});


var ProgressView = widgets.DOMWidgetView.extend({
    initialize: function() {
        ProgressView.__super__.initialize.apply(this, arguments);
	this.model.on('change:atoms', this.update_atoms, this);
    },

    render: function() {
    	this.atoms = document.createElement('div');
	this.atoms.classList.add('atoms');
    	this.el.appendChild(this.atoms);

    	this.update_atoms();
    },

    update_atoms: function() {
	var atom = this.atoms.firstChild
	while (atom) {
	    this.atoms.removeChild(atom);
	    atom = this.atoms.firstChild;
	}

    	var atoms = this.model.get('atoms');
	var that = this;
	atoms.forEach(function(item) {
	    var atom = document.createElement('div');
	    atom.classList.add('atom');
	    if (item.defined) {
		atom.classList.add(item.color);
	    }
	    if (item.active) {
		atom.classList.add('active')
	    }
	    that.atoms.appendChild(atom);
	});
    },
})


var AnnotationModel = DOMWidgetModel.extend({
    defaults: _.extend(DOMWidgetModel.prototype.defaults(), {
        _model_name: 'AnnotationModel',
        _view_name: 'AnnotationView',

	toolbar: undefined,
	progress: undefined,
	canvas: undefined
    })
}, {
    serializers: _.extend({
        toolbar: {deserialize: widgets.unpack_models},
        progress: {deserialize: widgets.unpack_models},
        canvas: {deserialize: widgets.unpack_models},
    }, DOMWidgetModel.serializers)
});


var AnnotationView = widgets.DOMWidgetView.extend({
    initialize: function() {
        AnnotationView.__super__.initialize.apply(this, arguments);
	this.toolbar_view = undefined;
	this.progress_view = undefined;
	this.canvas_view = undefined;
	this.model.on('change:toolbar', this.update_toolbar, this);
	this.model.on('change:progress', this.update_progress, this);
	this.model.on('change:canvas', this.update_canvas, this);
    },

    render: function() {
    	this.panel = document.createElement('div');
    	this.panel.setAttribute('id', 'panel');
    	this.panel.setAttribute('tabindex', '1');
    	this.panel.classList.add('annotate');
    	this.el.appendChild(this.panel);

	this.capture = document.createElement('div');
	this.capture.classList.add('capture');
	this.capture.textContent = '●';
	this.panel.appendChild(this.capture);

    	this.toolbar = document.createElement('div');
	this.toolbar.setAttribute('id', 'toolbar');
    	this.panel.appendChild(this.toolbar);
	
    	this.progress = document.createElement('div');
	this.progress.setAttribute('id', 'progress');
    	this.panel.appendChild(this.progress);
	
	this.canvas = document.createElement('div');
	this.panel.appendChild(this.canvas);

    	this.update_toolbar();
    	this.update_progress();
	this.update_canvas();

	var that = this;
	this.panel.addEventListener('keypress', function(event) {
	    that.handle_keypress(event);
	});
    },

    handle_keypress: function(event) {
	this.blink_capture();
	this.send({
	    event: 'keypress',
	    code: event.which,
	})
    },

    blink_capture: function() {
	this.capture.classList.toggle('active', true);
	var that = this;
	setTimeout(function() {
	    that.capture.classList.toggle('active', false);
	}, 200);
    },

    create_toolbar_view: function(model) {
	var that = this;
	return this.create_child_view(model).then(function(view) {
	    that.toolbar.appendChild(view.buttons);
	    return view
	});
    },

    remove_toolbar_view: function(view) {
	this.toolbar.removeChild(view.buttons);
	view.remove();
    },

    update_toolbar: function() {
	if (this.toolbar_view) {
	    this.remove_toolbar_view(this.toolbar_view);
	}
	var model = this.model.get('toolbar');
	var that = this;
	this.create_toolbar_view(model).then(function(view) {
	    that.toolbar_view = view;
	});
    },

    create_progress_view: function(model) {
	var that = this;
	return this.create_child_view(model).then(function(view) {
	    that.progress.appendChild(view.atoms);
	    return view
	});
    },

    remove_progress_view: function(view) {
	this.progress.removeChild(view.atoms);
	view.remove();
    },

    update_progress: function() {
	if (this.progress_view) {
	    this.remove_progress_view(this.progress_view);
	}
	var model = this.model.get('progress');
	var that = this;
	this.create_progress_view(model).then(function(view) {
	    that.progress_view = view;
	});
    },

    create_canvas_view: function(model) {
	var that = this;
	return this.create_child_view(model).then(function(view) {
	    that.canvas.appendChild(view.el);
	    return view
	});
    },

    remove_canvas_view: function(view) {
	this.canvas.removeChild(view.el);
	view.remove();
    },

    update_canvas: function() {
	if (this.canvas_view) {
	    this.remove_canvas_view(this.canvas_view);
	}
	var model = this.model.get('canvas');
	var that = this;
	this.create_canvas_view(model).then(function(view) {
	    that.canvas_view = view;
	});
    },
})


module.exports = {
    ButtonModel: ButtonModel,
    ButtonView: ButtonView,

    ToolbarModel: ToolbarModel,
    ToolbarView: ToolbarView,

    ProgressModel: ProgressModel,
    ProgressView: ProgressView,

    AnnotationModel: AnnotationModel,
    AnnotationView: AnnotationView,
};
