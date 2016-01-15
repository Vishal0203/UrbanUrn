angular.module('product', ['urn.services'])
    .controller('CompareProductController', ['$rootScope', '$scope',
        CompareProductController = function ($rootScope, $scope) {
            var init = function () {
            };
            init();
        }])

    .controller('GridController', ['$rootScope', '$scope', 'Skus', 'ProductsSearch',
        GridController = function ($rootScope, $scope, Skus, ProductsSearch) {
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

                if ($rootScope.search_query) {
                    ProductsSearch.search({'filter': $rootScope.search_query},
                        function (data) {
                            $scope.sku_category = "Search";
                            $scope.sku_name = $rootScope.search_query;
                            $scope.sku_products = data.products;
                        },
                        function (error) {
                            console.log(error);
                        }
                    )
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

    .controller('ProductDetailController', ['$rootScope', '$scope', '$window','Carts',
        ProductDetailController = function ($rootScope, $scope, $window, Carts) {
            $scope.quantitySelected="1";
            var init = function () {
                if ($window.localStorage.getItem('selected-product')) {
                        $rootScope.selectedProduct = JSON.parse($window.localStorage.getItem('selected-product'));
                    } else {
                        $rootScope.loadRoute('/home');
                    }
                var skusList = [$rootScope.womenSkus, $rootScope.menSkus, $rootScope.decorSkus];
                angular.forEach(skusList, function(parentSku) {
                    angular.forEach(parentSku, function (childSku) {
                        if($rootScope.selectedProduct.parent_sku_guid == childSku.parent_sku_guid){
                        $scope.getSkuDetails(childSku.children);
                        }
                    })
                })
                };

            $scope.getSkuDetails = function(skus){
                angular.forEach(skus, function(sku) {
                   if(sku.sku_guid == $rootScope.selectedProduct.sku_guid){
                       $scope.selectedSku = sku.name;
                   }
                });
            };

            $scope.add = function() {
              var number = parseInt($scope.quantitySelected);
              if(number <= $rootScope.selectedProduct.product_data.quantity-1){
                  number++;
              }
              $scope.quantitySelected = number.toString();

            };
            $scope.negate = function() {
              if($scope.quantitySelected > 0 ){
                  $scope.quantitySelected--;
              }
            };
            $scope.addItemToCart = function () {
                var payload = {};
                payload.product_guid = $rootScope.selectedProduct.product_guid;
                var product_info = {};
                product_info.quantity = $scope.quantitySelected;
                payload.product_data = JSON.stringify(product_info);
                Carts.addItemsToCart(JSON.stringify(payload), function (data) {
                     console.log(data);
                     $rootScope.getCartDetails();
                }, function (error) {
                    console.log(error);
                })
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