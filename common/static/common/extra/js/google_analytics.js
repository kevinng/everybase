let setGAUserType = (function() {

    function findGetParameter(parameterName) {
        var result = null,
            tmp = [];
        location.search
            .substr(1)
            .split("&")
            .forEach(function (item) {
              tmp = item.split("=");
              if (tmp[0] === parameterName) result = decodeURIComponent(tmp[1]);
            });
        return result;
    }

    let setUserType = function() {
        let userType = findGetParameter('t');
        if (userType == 'i') {
            // This is an internal user
            var dimensionValue = 'Internal User';
            ga('set', 'dimension1', dimensionValue);
        }
    };

    return setGAUserType;
})();

setGAUserType.setUserType();