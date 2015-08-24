wutu.controller("TestModuleController", function($scope, TestModuleService){
	$scope.data = {};
	TestModuleService.get("*").then(function(response){
		$scope.data = response.data;
	});

	$scope.add_note = function(text){
		TestModuleService.put({"text": text}).then(function(response){
			$scope.data.push({"id": response.data.id, "text": text})
		});
	}
});