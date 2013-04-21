function MainCtrl($scope, $http){

	$scope.results = [];
	$scope.searching = false;

	$scope.search = function(text){
		$scope.searching = true;
		$scope.results = [];
		var params = {q: text};
		$http({ method: "GET", url: "/search", params: params }). success(function(data){
			
			data = angular.fromJson(data);
			console.log(data);
			data.forEach(function(item){
				$scope.results.push({url: item});
			});

			$scope.results.forEach(function(item) {
				var params = {q: item.url};
				$http({ method: "GET", url: "/get", params: params }).success(function(data){
					item.html = data;
					item.downloaded = true;
					
					$("#" + $scope.results.indexOf(item)).append(item.html.content);

					$scope.searching = searchEnded();
				});
			});
		});
	};

	var searchEnded = function () {
		var downloaded = _.select($scope.results, function (item) {
			return item.downloaded;
		});

		return ! (downloaded.length == $scope.results.length);
	};


	$scope.open = function (result) {
		window.open(result.url);
	};
};

