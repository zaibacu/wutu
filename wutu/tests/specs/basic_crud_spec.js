'use strict';

describe("CRUD service", function(){

	beforeEach(module("wutu"));
	beforeEach(function(){
		base_url = function(){ return "http://localhost:5555/"; };
	});
	var service;
	beforeEach(inject(function(_TestModuleService_){
		service = _TestModuleService_;
	}));

	afterEach(inject(function($rootScope) {
	  $rootScope.$apply();
	}));

	it("handle create operation", function(done){
		service.get(1).then(function(response){
			expect(response).toBe(1);
		}).finally(done);
	});
});