require('./annotate.css')

// Export widget models and views, and the npm package version number.
module.exports = require('./annotate.js');
module.exports['version'] = require('../package.json').version;
