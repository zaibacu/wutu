'use strict';

describe("CRUD service", function(){
	var service, $httpBackend;

	beforeEach(module("wutu"));

	beforeEach(inject(function($injector){
		$httpBackend = $injector.get("$httpBackend");
	}));

	beforeEach(inject(function(_TestModuleService_){
		service = _TestModuleService_;
	}));

	it("handle create operation", function(done){
		service.get(1).then(function(response){
			expect(response.data.result).toBe(1);
		}).finally(done);

		$httpBackend.expectGET("/test_module/1").respond({result: 1})
		$httpBackend.flush();
	});
});