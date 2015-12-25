angular.module('urn.models', ['ngResource'])
    .factory('ApiUrls', function () {
        var apiBaseUrl = 'api/v1_0/';
        var baseUrls = {
            'products': apiBaseUrl + 'products',
            'register': apiBaseUrl + 'registration',
            'login': apiBaseUrl + 'login',
            'whoami': apiBaseUrl + 'whoami',
            'skus': apiBaseUrl + 'skus',
            'carts': apiBaseUrl + 'carts',
            'wishlist': apiBaseUrl + 'wishlists',
            'addresses': apiBaseUrl + 'addresses'
        };
        return angular.extend(baseUrls, {});
    })

    .factory('requestInterceptor', ['$cookies', function ($cookies) {
        return {
            request: function (config) {
                if (!config.url.match(/api/)) {
                    return config;
                }
                var authToken = $cookies.get('auth-token');
                if (authToken != undefined) {
                    angular.extend((config.headers = config.headers || {}), {
                        'X-Urbanurn-Auth': authToken
                    });
                }
                return config;
            }
        }
    }])
    .config(['$httpProvider', function ($httpProvider) {
        $httpProvider.interceptors.push('requestInterceptor');
    }])
;