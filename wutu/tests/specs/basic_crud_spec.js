'use strict';

describe("CRUD service", function(){

	beforeEach(module("wutu"));

	var service;
	beforeEach(inject(function(_TestModuleService_){
		service = _TestModuleService_;
	}));

	it("handle create operation", function(done){
		var promise = service.get(1);
		promise.then(
			function(response){
				done();
			},
			function(error){
				expect("received error: " + error).toFail();
			});
		//var expected = "1";
		//expect(result).to.equal(expected);
	});
});