'use strict'

function isPrime(n) {
    if (n <= 3) { return n > 1; }
    if (n % 2 == 0 || n % 3 == 0) { return false; }
    for (var  i = 5; i * i <= n; i += 6) {
        if (n % i == 0 || n % (i + 2) == 0) { return false; }
    }
    return true;
}

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

        var prev = 2;
        var curr = 1;
        var _ret = [];

        for(var i = 0; i < count; ) {
            if(isPrime(curr)) {
                _ret[i] = curr;
                i+=1;
            }
            curr += prev;
            prev = curr - prev;

            // Limit to 10 entries to avoid blocking
            if(i > 9)
                i = count;
        }

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

function createCustomPointScale(alias, name, gen) {
    POINTSCALES[alias] = {
        name: name,
        gen: gen
    };
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


