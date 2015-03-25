'use strict'

angular.module('theApp')

    .factory('pivotal-api', ['$http', '$q', '$modal', function($http, $q, $modal) {
        var urlBase = '//www.pivotaltracker.com/services/v5';
        var _ret = {};

        _ret.login = function(username, password) {
            var def = $q.defer();

            $http.get(urlBase + "/me")
            .success(function(data) {
                def.resolve(data);
            })
            .error(function(response, code) {
                def.reject(data);
            });

            return def.promise;
        }

        return _ret;
    }])