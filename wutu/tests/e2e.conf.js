exports.config = {
  seleniumAddress: "http://localhost:4444/wd/hub",
  specs: ["specs/*_e2e_spec.js"],
  framework: "jasmine2",
  capabilities: {
    browserName: "firefox"
  }
};