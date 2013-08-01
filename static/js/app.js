function Controller($scope, $http) {
  $scope.master= {};
  $scope.urls = {};

  $scope.saved = function(data, status, header, config) {
    $scope.saved_shortened = data.shortened;
    $scope.saved_url = data.url;
    $scope.event = {};
    $scope.event.url = "url here";
  };

  $scope.save = function(_event) {
    $scope.master = angular.copy(_event);
    $http.post('/add_url/', $scope.master).success($scope.saved);
  };

  $scope.reset = function() {
    $scope._event = angular.copy($scope.master);
    $scope.master= {};
    $http.get('/urls/').success(function (data, status, header, config) {
        $scope.urls = data;
    });
  };
}
