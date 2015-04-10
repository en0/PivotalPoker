'use strict'

var POINTSCALES = {}

POINTSCALES.count = {
    name: "Counting",
    gen: function(count) {
        var _ret = [];
        for(var i = 0; i < count; i++)
            _ret[i] = i+1;
        return _ret;
    }
};

POINTSCALES.fibonacci = {
    name: "Fibonacci",
    gen: function(count) {

        var prev = 1;
        var curr = 1;
        var _ret = [];

        for(var i = 0; i < count; i++) {
            _ret[i] = curr;
            curr += prev;
            prev = curr - prev;
        }

        return _ret;
    }
};

POINTSCALES.lp = {
    name: "Lucas Primes",
    gen: function(count) {
        var _ret = [];
        for(var i = 0; i < count; i++)
            /* someting */
            _ret = _ret;
        return _ret;
    }
};

POINTSCALES.powers = {
    name: "Powers of Two",
    gen: function(count) {
        var _ret = [];
        var curr = 1;
        for(var i = 0; i < count; i++) {
            _ret[i] = curr;
            curr+=curr;
        }
        return _ret;
    }
};

var PointScale = function(algo, count) {
    Object.defineProperty(this, "name", {
        get: function() {
            return algo.name;
        },
    });

    Object.defineProperty(this, "count", {
        get: function() {
            return count;
        },
    });

    Object.defineProperty(this, "sequence", {
        get: function() {
            return algo.gen(count);
        },
    });
};


