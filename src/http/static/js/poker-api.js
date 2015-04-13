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

        _ret.getGame = function(gameId) {
            /* GET /api/v0.1/game/:gameId : Retrieve the details of game, gameId
             *
             * Arguments:
             *  gameId : The unique identifier for the game.
             *
             * Returns: (as promise)
             *  On success, Game Entity { ... }
             *  On error, { message: MESSAGE, status_code: STATUS_CODE }
             */
             var def = $q.defer();
             $http.get(urlBase+'/game/'+gameId)
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
        };

        _ret.joinGame = function(gameId, password) {
            /* POST /api/v0.1/player/:gameId : Join the game, gameId.
             *
             * Arguments:
             *  gameId : The game to join.
             *  password : (If Required) A password to join the game.
             *
             * Returns: (as promise)
             *  On success, Enqueue Job Entity { ... }
             *  On error, { message: MESSAGE, status_code: STATUS_CODE }
             */
             var def = $q.defer();
             $http.post(urlBase+'/player/'+gameId+"/", { 'password': password })
            .success(function(data) { def.resolve(data); })
            .error(function(response, code) { def.reject(response); });
            return def.promise;
        };

        _ret.leaveGame = function(gameId, playerId) {
            /* DELETE /api/v0.1/player/:gameId/:playerId : Remove a player from the game.
             *
             * Arguments:
             *  gameId : The game in question.
             *  playerId : The player to remove from the game.
             *
             * Returns: (as promise)
             *  On success, Enqueue Job Entity { ... }
             *  On error, { message: MESSAGE, status_code: STATUS_CODE }
             */
             var def = $q.defer();
             $http.delete(urlBase+'/player/'+gameId+"/"+playerId)
            .success(function(data) { def.resolve(data); })
            .error(function(response, code) { def.reject(response); });
            return def.promise;
        };

        _ret.getJobStatus = function(jobId) {
            /* GET /api/v0.1/jobs/:jobId : Retrieve queued item, jobId
             *
             * Arguments:
             *  jobId : The job id.
             *
             * Returns: (as promise)
             *  On success, Enqueue Job Entity { ... }
             *  On error, { message: MESSAGE, status_code: STATUS_CODE }
             */
             var def = $q.defer();
             $http.get(urlBase+'/jobs/'+jobId)
            .success(function(data) { def.resolve(data); })
            .error(function(response, code) { def.reject(response); });
            return def.promise;
        };

        _ret.dealHand = function(gameId, story) {
            /* PUT /api/v0.1/hand/:gameId : Deal the hand for game, gameId
             *
             * Arguments:
             *  gameId : The game to deal the hand to.
             *  story : The user story for the hand.
             *
             * Returns: (as promise)
             *  On success, Enqueue Job Entity { ... }
             *  On error, { message: MESSAGE, status_code: STATUS_CODE }
             */
             var def = $q.defer();
             $http.put(urlBase+'/hand/'+gameId, { body: story })
            .success(function(data) { def.resolve(data); })
            .error(function(response, code) { def.reject(response); });
            return def.promise;
        };

        return _ret;

    }]);
