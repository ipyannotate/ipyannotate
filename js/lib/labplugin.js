var ipyannotate = require('./index');
var base = require('@jupyter-widgets/base');

module.exports = {
  id: 'ipyannotate',
  requires: [base.IJupyterWidgetRegistry],
  activate: function(app, widgets) {
      widgets.registerWidget({
          name: 'ipyannotate',
          version: ipyannotate.version,
          exports: ipyannotate
      });
  },
  autoStart: true
};

