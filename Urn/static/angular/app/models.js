angular.module('urn.models', ['ngResource'])

    .factory('ApiUrls', function () {
        var baseUrls = {
            'products': 'products'
        };
        return angular.extend(baseUrls, {});
    })
;