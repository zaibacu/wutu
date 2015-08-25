'use strict';

describe("CRUD controller", function(){
	var controller = null, $scope = null, $httpBackend = null;
	var storage = [
			{"id": 1, "text": "#1"},
			{"id": 2, "text": "#2"},
			{"id": 3, "text": "#3"}
		];

	beforeEach(module("wutu"));
	beforeEach(inject(function($injector){
		$httpBackend = $injector.get("$httpBackend");

		$httpBackend.expectGET("/test_module/*/").respond(storage)
	}));

	beforeEach(inject(function($controller, $rootScope, _TestModuleService_){
		$scope = $rootScope.$new();
		controller = $controller("TestModuleController", {
			$scope: $scope,
			testModuleService: _TestModuleService_
		});
		$httpBackend.flush();
	}));

	it("handle basic create/list/delete", function(){
		//Creation part
		$httpBackend.expectPUT("/test_module").respond({"id": 4, "text": "#4"});

		$scope.add_note("#4");
		$httpBackend.flush();

		function check_for_item(id){
			return $scope.data.filter(function(obj){
				if(obj.id == id)
					return true;
			}).length;
		}
		expect(check_for_item(4)).toEqual(1);

		//Delete part
		$httpBackend.expectDELETE("/test_module/4/").respond({"success": true});
		$scope.delete_note(4);
		$httpBackend.flush();

		expect(check_for_item(4)).toEqual(0);
	});
});