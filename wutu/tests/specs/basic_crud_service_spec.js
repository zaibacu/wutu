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
		service.post(1, {"text": "#1"}).then(function(response){
			expect(response.data.id).toBe(1);
		}).finally(done);

		$httpBackend.expectPOST("/test_module/1/", {"text": "#1"}).respond({id: 1})
		$httpBackend.flush();
	});

	it("handle read operation", function(done){
		service.get(1).then(function(response){
			expect(response.data).toEqual({"text": "#1"});
		}).finally(done);

		$httpBackend.expectGET("/test_module/1/").respond({"text": "#1"})
		$httpBackend.flush();
	});

	it("handle update operation", function(done){
		service.put({"text": "#2"}).then(function(response){
			expect(response.data).toEqual({"id": "1"});
		}).finally(done);

		$httpBackend.expectPUT("/test_module", {"text": "#2"}).respond({"id": "1"})
		$httpBackend.flush();
	});

	it("handle delete operation", function(done){
		service.delete(1).then(function(response){
			expect(response.data).toBe(true);
		}).finally(done);

		$httpBackend.expectDELETE("/test_module/1/").respond(true)
		$httpBackend.flush();
	});
});