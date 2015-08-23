wutu.controller("TestModuleController", function($scope, TestModuleService){
	$scope.data = {};
	TestModuleService.get(1).then(function(response){
		$scope.data = response.data;
	});
});