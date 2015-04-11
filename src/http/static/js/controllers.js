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

app.controller('homeCtrl', ['$scope', '$modal', 'poker-api', function($scope, $modal, api) {
    document.title = 'Dashboard';
    api.listGames().then(function(games) {
        $scope.games = games.games;
        console.log(games.games);
    });

    $scope.joinGame = function(game_id) {
        // remember to check for password
        console.log(game_id);
    };

    $scope.showCreateGameModal = function() {

        var modalInst = $modal.open({
            templateUrl: 'partials/createGame_modal.html',
            controller: 'createGameCtrl',
        }).result.then(function(game) {
            api.createGame(game)
            .then(function(data) {
                $scope.games.push(data);
                console.log(data);
            })
            .catch(function(error) {
                // Notify an error
            });
        });
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

app.controller('createGameCtrl', ['$scope', '$modalInstance', function($scope, $modalInstance) {
    $scope.form_alerts = [];
    $scope.ok = function() {

        // Needs form validation.
        var game = {
            title: $scope.game.title,
            desc: $scope.game.desc,
            pts_scale: POINTSCALES[$scope.game.pts_scale_select].gen($scope.game.pts_scale_len),
        }

        // Add the password if it was set.
        if($scope.game.password) {
            game.password = $scope.game.password;
        }

        $modalInstance.close(game);
    };

    $scope.cancel = function() {
        $modalInstance.dismiss('cancel');
    };

    // Create a custom sequence using the custom sequence input box.
    createCustomPointScale("__custom__", "Custom Sequence", function(count) {

        // Convert custom set to a list. Strip whitespace and split on comma
        var _set = $scope.game.custom_pts_scale.replace(/ /g,'').split(',');
        var _ret = [];

        // We are ignoring "count" on custom lists so just go through every element.
        for(var i = 0; i < _set.length; i++) {
            // Convert the value to a number. this will support ints, floats, and doubles
            _ret[i] = Number(_set[i]);

            // Validate the element was a number.
            // If it is not, add a form validation alert.
            if(isNaN(_ret[i])) {
                _ret = [];
                console.log('Add alert to form');
                break;
            }
        }

        return _ret;
    });

    // Add the canned sequences to the point scale selection list.
    var i = 0;
    $scope.PointScaleOptions = []
    for(var s in POINTSCALES) {
        $scope.PointScaleOptions[i++] = {
            name: POINTSCALES[s].name,
            value: s
        };
    }

    // Create Game Presets
    $scope.game = {
        pts_scale_select: "count",
        pts_scale_len: 5
    };
}]);
