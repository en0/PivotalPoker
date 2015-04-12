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

