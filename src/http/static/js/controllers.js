'use strict'

app.controller('rootCtrl', ['$rootScope', '$location', function($rootScope, $location) {
    $rootScope.go = function(path) {
        $location.path(path);
    };
}]);

app.controller('homeCtrl', ['$scope', '$modal', function($scope, $modal) {
    document.title = 'Dashboard';
    var modalinst = $modal.open({
        templateUrl: 'partials/login.html',
        controller: 'loginCtrl',
    });
}]);

app.controller('aboutCtrl', ['$scope', function($scope) {
    document.title = 'About';
}]);

app.controller('404Ctrl', ['$scope', function($scope) {
    document.title = 'Not Found';
}]);

app.controller('loginCtrl', ['$scope', '$modalInstance', function($scope, $modalInstance) {

}]);
