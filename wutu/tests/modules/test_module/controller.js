wutu.controller("TestModuleController", function($scope, TestModuleService){
	$scope.data = {};
	TestModuleService.get("*").then(function(response){
		$scope.data = response.data;
	});

	$scope.add_note = function(id, text){
		TestModuleService.put(id, {"text": text})
	}
});