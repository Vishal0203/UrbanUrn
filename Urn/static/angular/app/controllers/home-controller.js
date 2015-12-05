angular.module('home', ['urn.services'])
    .controller('HomeController', ['$rootScope', '$scope', 'Products',
        HomeController = function ($rootScope, $scope, Products) {
            var init = function () {
                Products.getProducts({},
                    function (data) {
                        angular.forEach(data, function (item, key) {
                        });
                    },
                    function (error) {
                        console.log(error);
                    });
            };
            init();
        }])
;