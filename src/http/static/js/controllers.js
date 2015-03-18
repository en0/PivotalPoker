'use strict'

app.controller('rootCtrl', ['$rootScope', '$location', function($rootScope, $location) {
    $rootScope.go = function(path) {
        $location.path(path);
    };
}]);

app.controller('homeCtrl', ['$scope', function($scope) {
    document.title = 'Dashboard';
}]);

app.controller('aboutCtrl', ['$scope', function($scope) {
    document.title = 'About';
}]);

app.controller('404Ctrl', ['$scope', function($scope) {
    document.title = 'Not Found';
}]);

