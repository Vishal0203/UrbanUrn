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
    .factory('UserRegister', function ( $resource, ApiUrls) {
        return $resource(ApiUrls.register, {},
            {
                register : {method : "POST"}
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
                getSkus: {method: "GET", isArray: true},
                getSkuProducts: {method: "GET"}
            })
    })
    .factory('Carts', function ($resource, ApiUrls) {
        return $resource(ApiUrls.carts, {},
            {
                getCartDetails: {method: "GET", isArray: true},
                deleteItem: {method: "DELETE"}
            })
    })
    .factory('WishList', function ($resource, ApiUrls) {
        return $resource(ApiUrls.wishlist, {},
            {
                getWishlist : {method: "GET", isArray: true}
            })
    });