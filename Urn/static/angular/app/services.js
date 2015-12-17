angular.module('urn.services', ['urn.models'])
    .factory('Products', function ($resource, ApiUrls) {
        return $resource(ApiUrls.products, {},
            {
                getProducts: {method: "GET", isArray: true}
            })
    })
    .factory('UserLogin', function ($resource, ApiUrls) {
        return $resource(ApiUrls.login, {},
            {
                login: {method: "POST"}
            })
    })
    .factory('Whoami', function ($resource, ApiUrls) {
        return $resource(ApiUrls.whoami, {},
            {
                getUserDetails: {method: "GET"}
            })
    })
    .factory('Skus', function ($resource, ApiUrls) {
        return $resource(ApiUrls.skus, {},
            {
                getSkus: {method: "GET", isArray: true}
            })
    })
;