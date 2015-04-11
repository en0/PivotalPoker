'use strict'

angular.module('theApp')

    .factory('poker-api', ['$http', '$q', function($http, $q) {
        var urlBase = '/api/v0.1';
        var _ret = {};

        _ret.me = function() {
            /* GET /api/v0.1/session : Retrieve user session.
             *
             * Returns: (as promise)
             *  On success, returns { name: PLAYER_NAME }
             *  On error, { message: MESSAGE, status_code: STATUS_CODE }
             */
            var def = $q.defer();

            $http.get(urlBase+"/session")
            .success(function(data) { def.resolve(data); })
            .error(function(response, code) { def.reject(response); });

            return def.promise;
        };

        _ret.register = function(name) {
            /* PUT /api/v0.1/session : Start user sessions.
             *
             * Arguments:
             *  name - The Player Name to register with.
             *
             * Returns: (as promise)
             *  On success, NO CONTENT
             *  On error, { message: MESSAGE, status_code: STATUS_CODE }
             */
            var def = $q.defer();
            var _data = { "name": name };

            $http.put(urlBase+"/session", _data)
            .success(function(data) { def.resolve(data); })
            .error(function(response, code) { def.reject(data); });

            return def.promise;
        };

        _ret.listGames = function() {
            /* GET /api/v0.1/game/ : List open games.
             *
             * Returns: (as promise)
             *  On success, { games: [ ... ] }
             *  On error, { message: MESSAGE, status_code: STATUS_CODE }
             */
            var def = $q.defer();
            $http.get(urlBase+"/game/")
            .success(function(data) { def.resolve(data); })
            .error(function(response, code) { def.reject(response); });
            return def.promise;
        };

        _ret.createGame = function(game) {
            /* POST /api/v0.1/game/ : Create a new game.
             *
             * Arguments: (as obj)
             *  title : The title of the game.
             *  desc : The description for the game.
             *  pts_scale : An array of values used as the point scales for the game.
             *  password : (Optional) A password used to join the game.
             *
             * Returns: (as promise)
             *  On success, Game Entity { ... }
             *  On error, { message: MESSAGE, status_code: STATUS_CODE }
             */
             var def = $q.defer();
             $http.post(urlBase+'/game/', game)
            .success(function(data) { def.resolve(data); })
            .error(function(response, code) { def.reject(response); });
            return def.promise;
        }

        return _ret;

    }]);