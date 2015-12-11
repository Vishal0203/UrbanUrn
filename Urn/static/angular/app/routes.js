angular.module('urn')
    .config(function ($routeProvider) {
        $routeProvider
            .when('/home', {
                controller : 'HomeController',
                templateUrl : '/static/angular/app/views/home.html'
            })
            .when('/not_found', {
                controller : 'RootController',
                templateUrl : '/static/angular/app/views/404error.html'
            })
            .when('/about_us', {
                controller : 'MiscController',
                templateUrl : '/static/angular/app/views/about_us.html'
            })
            .when('/blog', {
                controller : 'BlogController',
                templateUrl : '/static/angular/app/views/blog.html'
            })
            .when('/blog_detail', {
                controller : 'BlogDetailController',
                templateUrl : '/static/angular/app/views/blog_detail.html'
            })
            .when('/checkout', {
                controller : 'CheckoutController',
                templateUrl : '/static/angular/app/views/checkout.html'
            })
            .when('/compare', {
                controller : 'CompareProductController',
                templateUrl : '/static/angular/app/views/compare.html'
            })
            .when('/contact_us', {
                controller : 'MiscController',
                templateUrl : '/static/angular/app/views/contact_us.html'
            })
            .when('/dashboard', {
                controller : 'DashboardController',
                templateUrl : '/static/angular/app/views/dashboard.html'
            })
            .when('/faq', {
                controller : 'MiscController',
                templateUrl : '/static/angular/app/views/faq.html'
            })
            .when('/grid', {
                controller : 'GridController',
                templateUrl : '/static/angular/app/views/grid.html'
            })
            .when('/list', {
                controller : 'ListController',
                templateUrl : '/static/angular/app/views/list.html'
            })
            .when('/login', {
                controller : 'LoginController',
                templateUrl : '/static/angular/app/views/login.html'
            })
            .when('/multiple_addresses', {
                controller : 'AddressController',
                templateUrl : '/static/angular/app/views/multiple_addresses.html'
            })
            .when('/product_detail', {
                controller : 'ProductDetailController',
                templateUrl : '/static/angular/app/views/product_detail.html'
            })
            .when('/quick_view', {
                controller : 'QuickViewController',
                templateUrl : '/static/angular/app/views/quick_view.html'
            })
            .when('/shopping_cart', {
                controller : 'CartController',
                templateUrl : '/static/angular/app/views/shopping_cart.html'
            })
            .when('/wishlist', {
                controller : 'WishlistController',
                templateUrl : '/static/angular/app/views/wishlist.html'
            })
           .otherwise('/home');
    })
;