'use strict'

app.controller('rootCtrl', ['$rootScope', '$location', '$modal', 'poker-api', function($rootScope, $location, $modal, api) {

    $rootScope.go = function(path) {
        /* Short, global function change pages */
        $location.path(path);
    };

    var getPlayerName = function() {
        /* Get the player's name either from the active session or prompt the user.
         * If we need to prompt the user, the Register modal will be used to create
         * a new session with the server. */

        // Try to get the current session from the server.
        api.me()

        // If the session exists, set the name
        .then(function(data) {  $rootScope.displayName = data.name; })

        // Some error occurred. Possibly no session.
        .catch(function(error) {
            // The api will throw a 404 if no session exists. We need to create one.
            // If not a 404, something went very wrong, abort
            if (error.status_code == 404) {
                // Prompt user for Player Name.
                var modalInst = $modal.open({
                    templateUrl: 'partials/register_modal.html',
                    controller: 'registerCtrl',
                }).result.finally(function(name) {
                    // Ask server if it worked.
                    getPlayerName();
                });
            } else {
                console.log("Oops! My Bad.");
                console.log(error);
                alert("this should pop a error.")
            }
        });
    };

    // Sets player name in $rootScope.displayName
    getPlayerName();

}]);

app.controller('homeCtrl', ['$scope', 'poker-api', function($scope, api) {
    document.title = 'Dashboard';
    api.listGames().then(function(games) {
        $scope.games = games.games;
        console.log(games.games);
    });

    $scope.joinGame = function(game_id) {
        // remember to check for password
        console.log(game_id);
    };

    $scope.createGame = function() {
        console.log($scope.game)
    };
}]);

app.controller('aboutCtrl', ['$scope', function($scope) {
    document.title = 'About';
}]);

app.controller('404Ctrl', ['$scope', function($scope) {
    document.title = 'Not Found';
}]);

app.controller('loginCtl', ['$scope', '$modalInstance', 'poker-api', function($scope, $modalInstance, api) {
    // Get pivotal api key
}]);

app.controller('registerCtrl', ['$scope', '$modalInstance', 'poker-api', function($scope, $modalInstance, api) {

    // This will send up the player's name and create a session with the API
    $scope.register = function() {
        api.register($scope.name)
        .then(function() {
            // Success
            $modalInstance.close($scope.name)
        }, function(error) {
            // Error registering session.
            // Probably should pop a error message here.
        });
    };

}]);

