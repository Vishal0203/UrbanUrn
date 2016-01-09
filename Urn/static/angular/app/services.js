angular.module('urn.services', ['urn.models'])
    .factory('Products', function ($resource, ApiUrls) {
        return $resource(ApiUrls.products, {},
            {
                getProducts: {method: "GET", isArray: true}
            })
    })
    .factory('ProductsSearch', function ($resource, ApiUrls) {
        return $resource(ApiUrls.search, {},
            {
                search: {method: "GET"}
            })
    })
    .factory('UserLogin', function ($resource, ApiUrls) {
        return $resource(ApiUrls.login, {},
            {
                login: {method: "POST"}
            })
    })
    .factory('UserRegister', function ($resource, ApiUrls) {
        return $resource(ApiUrls.register, {},
            {
                register: {method: "POST"}
            })
    })
    .factory('UserLogout', function ($resource, ApiUrls) {
        return $resource(ApiUrls.logout, {},
            {
                logout: {method: "GET"}
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
                deleteItem: {method: "DELETE"},
                updateCart: {method: "PUT"},
                addItemsToCart: {method: "POST"}
            })
    })
    .factory('WishList', function ($resource, ApiUrls) {
        return $resource(ApiUrls.wishlist, {},
            {
                getWishlist: {method: "GET", isArray: true},
                deleteWishlist: {method: "DELETE"},
                addToWishlist: {method: "POST"}
            })
    })
    .factory('Address', function ($resource, ApiUrls) {
        return $resource(ApiUrls.addresses, {},
            {
                add: {method: "POST", isArray: true}
            })
    })
    .factory('Orders', function ($resource, ApiUrls) {
        return $resource(ApiUrls.orders, {},
            {
                place: {method: "POST", isArray: true}
            })
    });