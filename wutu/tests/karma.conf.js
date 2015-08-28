// karma.conf.js
module.exports = function(config) {
  config.set({
    frameworks: ["jasmine"],
    files: [
      "node_modules/angular/angular.js",
      "node_modules/angular-mocks/angular-mocks.js",
      "http://localhost:5555/init.js",
      "http://localhost:5555/test_module/service.js",
      "http://localhost:5555/test_module/controller.js",

      "specs/*.js"
    ],
    exclude: [
      "specs/*_e2e_spec.js"
    ],
    logLevel: "LOG_DEBUG",
    browsers: ["PhantomJS"],
    autoWatch: false,
    singleRun: true
  });
};