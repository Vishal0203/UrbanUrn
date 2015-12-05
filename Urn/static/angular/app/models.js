angular.module('urn.models', ['ngResource'])
    .factory('ApiUrls', function () {
        var apiBaseUrl = 'api/v1_0/';
        var baseUrls = {
            'products': apiBaseUrl + 'products'
        };
        return angular.extend(baseUrls, {});
    })
;