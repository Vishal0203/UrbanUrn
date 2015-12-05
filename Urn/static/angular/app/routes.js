angular.module('urn')
    .config(function ($routeProvider) {
        $routeProvider
            .when('/home', {
                controller : 'rootController',
                templateUrl : '/static/angular/app/views/home.html'
            })
            .when('/not_found', {
                controller : 'rootController',
                templateUrl : '/static/angular/app/views/404error.html'
            })
            .when('/about_us', {
                controller : 'rootController',
                templateUrl : '/static/angular/app/views/about_us.html'
            })
            .when('/blog', {
                controller : 'rootController',
                templateUrl : '/static/angular/app/views/blog.html'
            })
            .when('/blog_detail', {
                controller : 'rootController',
                templateUrl : '/static/angular/app/views/blog_detail.html'
            })
            .when('/checkout', {
                controller : 'rootController',
                templateUrl : '/static/angular/app/views/checkout.html'
            })
            .when('/compare', {
                controller : 'rootController',
                templateUrl : '/static/angular/app/views/compare.html'
            })
            .when('/contact_us', {
                controller : 'rootController',
                templateUrl : '/static/angular/app/views/contact_us.html'
            })
            .when('/dashboard', {
                controller : 'rootController',
                templateUrl : '/static/angular/app/views/dashboard.html'
            })
            .when('/faq', {
                controller : 'rootController',
                templateUrl : '/static/angular/app/views/faq.html'
            })
            .when('/grid', {
                controller : 'rootController',
                templateUrl : '/static/angular/app/views/grid.html'
            })
            .when('/list', {
                controller : 'rootController',
                templateUrl : '/static/angular/app/views/list.html'
            })
            .when('/login', {
                controller : 'rootController',
                templateUrl : '/static/angular/app/views/login.html'
            })
            .when('/multiple_addresses', {
                controller : 'rootController',
                templateUrl : '/static/angular/app/views/multiple_addresses.html'
            })
            .when('/product_detail', {
                controller : 'rootController',
                templateUrl : '/static/angular/app/views/product_detail.html'
            })
            .when('/quick_view', {
                controller : 'rootController',
                templateUrl : '/static/angular/app/views/quick_view.html'
            })
            .when('/shopping_cart', {
                controller : 'rootController',
                templateUrl : '/static/angular/app/views/shopping_cart.html'
            })
            .when('/wishlist', {
                controller : 'rootController',
                templateUrl : '/static/angular/app/views/wishlist.html'
            })
           .otherwise('/home');
    })
;