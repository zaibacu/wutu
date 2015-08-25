exports.config = {
  seleniumAddress: "http://localhost:4444/wd/hub",
  specs: ["specs/*_e2e_spec.js"],
  capabilities: {
    browserName: "phantomjs"
  }
};