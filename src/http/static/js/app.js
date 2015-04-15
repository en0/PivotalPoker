var app = angular.module('theApp', ['ngRoute','ui.bootstrap']);

app.config(['$routeProvider', '$interpolateProvider', function($routeProvider, $interpolateProvider) {
    $routeProvider
        .when("/", {templateUrl: "partials/home.html", controller: "homeCtrl"})
        .when("/home/", {templateUrl: "partials/home.html", controller: "homeCtrl"})
        .when("/play/:gameId", {templateUrl: "partials/play.html", controller: "playCtrl"})
        .when("/about", {templateUrl: "partials/about.html", controller: "aboutCtrl"})
        .when("/404", {templateUrl: "partials/404.html", controller: "404Ctrl"})
        .otherwise({ redirectTo: '/404' });

    $interpolateProvider
        .startSymbol('[[')
        .endSymbol(']]');
}]);

app.filter('reverse', function() {
    return function(items) {
        return items.slice().reverse();
    };
});

app.filter('truncate', function () {
    return function (text, length, end) {
        if (isNaN(length))
            length = 10;

        if (end === undefined)
            end = "...";

        if (text.length <= length || text.length - end.length <= length) {
            return text;
        }
        else {
            return String(text).substring(0, length-end.length) + end;
        }

    };
});
