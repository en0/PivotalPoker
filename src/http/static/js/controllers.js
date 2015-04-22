'use strict'

app.controller('rootCtrl', ['$rootScope', '$location', '$modal', 'poker-api', function($rootScope, $location, $modal, api) {

    // Array to hold site level alerts.
    $rootScope.alerts = [];

    $rootScope.go = function(path) {
        /* Short, global function change pages
         *
         * Arguments:
         *  path - The path to navigate to.
         */
        $location.path(path);
    };

    $rootScope.showStatusModal = function(jobId, message) {
        /* Show the status modal for a specific job id.
         *
         * Arguments:
         *  jobId - the job to show the status for.
         *  message - The initial message to show on the modal.
         */
        var inst = $modal.open({
            templateUrl: 'partials/jobStatus_modal.html',
            controller: 'jobStatusCtrl',
            size: 'sm',
            resolve: {
                message: function () { return message; },
                jobId: function() { return jobId; }
            }
        });

        return inst;
    };

    $rootScope.addAlert = function(prefix, text) {
        /* Add a alert to the global alerts area
         *
         * Arguments:
         *  text - The text for the alert.
         */
        $rootScope.alerts.push(prefix + ": " + text);
    };

    $rootScope.clearAlerts = function() {
        /* Clear all alerts from global alerts array. */
        $rootScope.alerts = [];
    };

    $rootScope.clearAlert = function(index) {
        $rootScope.alerts.splice(index,1);
    };

    var getPlayerName = function() {
        /* Get the player's name either from the active session or prompt the user.
         * If we need to prompt the user, the Register modal will be used to create
         * a new session with the server. */

        // Try to get the current session from the server.
        api.me()

        // If the session exists, set the name
        .then(function(data) {
            $rootScope.playerId = data.player_id;
            $rootScope.displayName = data.name;
            console.log(data);
        })

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
                $scope.addAlert("ERROR", "Something when seriously wrong here.")
                console.log(error);
            }
        });
    };

    // Sets player name in $rootScope.displayName
    getPlayerName();

}]);

app.controller('homeCtrl', ['$scope', '$modal', 'poker-api', function($scope, $modal, api) {
    document.title = 'Planning Poker';

    function _loadGames() {
        // Make sure that this controller is still active
        if($scope.$$destroyed === true) return;

        api.listGames().then(function(games) {
            $scope.games = games.games;
            window.setTimeout(_loadGames, 10000);
        })
        .catch(function(error) {
            $scope.addAlert("ERROR", "Failed to retrieve game list.");
            console.log(error);
            window.setTimeout(_loadGames, 30000);
        });
    }

    function _joinGame(gameId, password) {
        /* Join the game, gameId, with the supplied password
         * We will submit the join request to the player route
         * we expect a queued job id in response.
         * After that we will use the job status modal to wait for the job to complete.
         * then we need to dispatch to the playing route.
         */
        console.log("Joining game: " + gameId);
        console.log("With password: " + password);

        api.joinGame(gameId, password)
        .then(function(job) {
            // Expect a queued Job in response.
            console.log("Jobid: ");
            console.log(job);

            // Show the job status in the jobStatus modal.
            $scope.showStatusModal(job.job_id, "Joining Game...")
            .result.then(function(data) {
                $scope.go('/play/'+gameId);
            });

        })
        .catch(function(error) {
            $scope.addAlert("ERROR", "Failed to join game.");
            console.log(error);
        });

    }

    $scope.joinGame = function(gameId, hasPassword) {
        console.log(gameId);
        console.log(hasPassword);

        // Some games require a joiner password. If so, prompt the user to enter it.
        if(hasPassword) {
            $modal.open({
                templateUrl: 'partials/passwordPrompt_modal.html',
                controller: 'promptCtrl',
                size: 'sm'
            })
            .result.then(function(pass) {
                _joinGame(gameId, pass);
            });
        } else {
            _joinGame(gameId, null);
        }
    };

    $scope.showCreateGameModal = function() {

        // Create a new game using the NewGame modal.
        // We will prompt for all the data from NewGame modal then create the game in this method.

        var modalInst = $modal.open({
            templateUrl: 'partials/createGame_modal.html',
            controller: 'createGameCtrl',
        }).result.then(function(game) {
            // Create the game using the provided details.
            // On success, add the game to the list of available games.
            api.createGame(game)
            .then(function(data) {
                $scope.games.push(data);
                console.log(data);
                console.log("This should probably just go to the game control window.")
            })
            .catch(function(error) {
                $scope.addAlert("ERROR", "Failed to create game.");
                console.log(error);
            });
        });
    };

    _loadGames();
}]);

app.controller('playCtrl', ['$scope', '$routeParams', 'poker-api', function($scope, $routeParams, api) {
    console.log($routeParams.gameId);
    $scope.gameId = $routeParams.gameId;
    $scope.handVisibleIndex = -1;

    $scope.setVisibleHand = function(index) {
        if(!$scope.isVisibleHand(index))
            $scope.handVisibleIndex = index;
        else
            $scope.handVisibleIndex = -1;
    };

    $scope.isVisibleHand = function(index) {
        return $scope.handVisibleIndex == index;
    };

    $scope.leaveGame = function(playerId) {
        api.leaveGame($scope.gameId, playerId).then(function(job) {
            // Show the job status in the jobStatus modal.
            $scope.showStatusModal(job.job_id, "Leaving game...")
            .result.then(function(data) {
                if(playerId == $scope.playerId)
                    $scope.go('/');
            });
        })
        .catch(function(error) {
            $scope.addAlert("ERROR", "Failed to leave game.")
            console.log(error);
        });
    };

    $scope.cancelHand = function() {
        api.cancelHand($scope.gameId).then(function(job) {
            $scope.showStatusModal(job.job_id, "Canceling hand...");
        })
        .catch(function(error) {
            $scope.addAlert("ERROR", "Failed to cancel hand.")
            console.log(error);
        });
    }

    $scope.applyVote = function(action) {
        console.log($scope.voteResult);
        api.applyVote($scope.gameId, action, $scope.voteResult).then(function(job) {
            $scope.showStatusModal(job.job_id, "Finalizing vote...")
            .result.finally(function(data) {
                $scope.voteResult = null;
            });
        })
        .catch(function(error) {
            $scope.addAlert("ERROR", "Failed to apply vote.")
            console.log(error);
        });
    }

    $scope.closeGame = function() {
        console.log("Ok");
        api.closeGame($scope.gameId)
        .then(function(job) {
            $scope.showStatusModal(job.job_id, "Closing the game...")
            .result.then(function(data) {
                $scope.go('/');
            });
        })
        .catch(function(error) {
            $scope.addAlert("ERROR", "Failed to close game.")
            console.log(error);
        });
    };

    $scope.dealHand = function() {
        //var a = $('#txtNewStory').value;
        api.dealHand($scope.gameId, $scope.newStory)
        .then(function(job) {
            $scope.showStatusModal(job.job_id, "Dealing new hand...")
            .result.then(function(data) {
                $scope.newStory = "";
            });
        })
        .catch(function(error) {
            $scope.addAlert("ERROR", "Failed to deal hand.")
            console.log(error);
        });
    };

    $scope.castVote = function(value) {
        console.log(value);
        api.castVote($scope.gameId, value)
        .then(function(job) {
            $scope.showStatusModal(job.job_id, "Casting vote...");
        })
        .catch(function(error) {
            $scope.addAlert("ERROR", "Failed to cast vote.")
            console.log(error);
        });
    };

    function _updateGame() {
        // Make sure that this controller is still active
        if($scope.$$destroyed === true) return;

        api.getGame($scope.gameId)
        .then(function(game) {
            $scope.game = game;
            $scope.isOwner = game.owner_id == $scope.playerId
            $scope.debug = JSON.stringify(game);
            console.log(game);
            window.setTimeout(_updateGame, 3000);
        })
        .catch(function(error) {
            $scope.addAlert("ERROR", "Failed to pull game state.")
            console.log(error);

            // Slow down retry.
            window.setTimeout(_updateGame, 30000);
        });
    }

    _updateGame();
    $scope.fakeState = function(state) {
        $scope.addAlert("This is a test alert")
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
        })
        .catch(function(error) {
            $scope.error_message = error;
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

app.controller('promptCtrl', ['$scope', '$modalInstance', function($scope, $modalInstance) {
    $scope.ok = function() { $modalInstance.close($scope.value); };
    $scope.cancel = function() { $modalInstance.dismiss('cancel'); };
}]);

app.controller('jobStatusCtrl', ['$scope', '$modalInstance', 'poker-api', 'message', 'jobId', function($scope, $modalInstance, api, message, jobId) {
    // Display the message on the status page.
    $scope.message = message;

    // This is used so timeout can close the modal.
    function complete() {
        $modalInstance.close("success");
    }

    function fail() {
        $modalInstance.dismiss("Failed");
    }

    function long_pull() {

        // Make sure that the modal is still open.
        if($scope.$$destroyed === true) return;

        // Get the current statue of the job we are waiting for.
        api.getJobStatus(jobId)
        .then(function(result) {
            // All jobs are "done" when status code is 200.
            // Otherwise they are still pending.
            if(result.status == 200) {
                $scope.message = result.message
                window.setTimeout(complete, 3000);
            } else if(result.status == 202) {
                // Update the message if one is available.
                if(result.message !== null)
                    $scope.message = result.message;

                // Wait 1 second and check again.
                window.setTimeout(long_pull, 1000);
                console.log(result);
            } else {
                // Status changed but not in a good way
                $scope.message = result.message;

                // Add error message to alerts
                $scope.addAlert("WARNING", result.message);

                // Close modal after 2 seconds
                window.setTimeout(fail, 2000);
            }
        })
        .catch(function(error) {
            console.log(error);
            $scope.message = "Something went very wrong here.";
            $scope.addAlert("ERROR", "Failed to get job state.");

            // Close modal after 2 seconds
            window.setTimeout(fail, 2000);
        });
    }

    // Start checking the job's status.
    long_pull();
}]);
