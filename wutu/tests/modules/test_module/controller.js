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

	$scope.delete_note = function(id){
		TestModuleService.delete(id).then(function(response){
			$scope.data = $scope.data.filter(function(obj){
				if(obj.id != id)
					return true;
			});
		});
	}
});