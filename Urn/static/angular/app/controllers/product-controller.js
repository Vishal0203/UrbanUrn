angular.module('product', ['urn.services'])
    .controller('CompareProductController', ['$rootScope', '$scope',
        CompareProductController = function ($rootScope, $scope) {
            var init = function () {
            };
            init();
        }])

    .controller('GridController', ['$rootScope', '$scope', 'Skus',
        GridController = function ($rootScope, $scope, Skus) {
            $scope.sku_category = '';
            $scope.sku_name = '';
            $scope.sku_products = [];
            var init = function () {
                if ($rootScope.sku_guid) {
                    Skus.getSkuProducts({'sku_guid': $rootScope.sku_guid},
                        function (data) {
                            if (data.parent_sku_category == 'women') {
                                $scope.sku_category = 'Women';
                            } else if (data.parent_sku_category == 'men') {
                                $scope.sku_category = 'Men';
                            } else if (data.parent_sku_category == 'decor') {
                                $scope.sku_category = 'Decor';
                            }
                            $scope.sku_name = data.name;
                            $scope.sku_products = data.products;
                        },
                        function (error) {
                            console.log(error);
                        });
                }
            };

            init();
        }])

    .controller('ListController', ['$rootScope', '$scope',
        ListController = function ($rootScope, $scope) {
            var init = function () {
            };
            init();
        }])

    .controller('ProductDetailController', ['$rootScope', '$scope', '$cookies',
        ProductDetailController = function ($rootScope, $scope, $cookies) {
            var init = function () {
                if ($rootScope.selectedProduct == undefined) {
                    if ($cookies.getObject('selected-product')) {
                        $rootScope.selectedProduct = $cookies.getObject('selected-product');
                    } else {
                        $rootScope.loadRoute('/home');
                    }
                }
            };
            init();
        }])

    .controller('QuickViewController', ['$rootScope', '$scope',
        QuickViewController = function ($rootScope, $scope) {
            var init = function () {
            };
            init();
        }])
;