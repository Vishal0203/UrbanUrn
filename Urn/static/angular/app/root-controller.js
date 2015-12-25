angular.module('urn')
    .controller('RootController', ['$rootScope', '$scope', '$location', '$route', '$interval', 'Skus','Carts',
        RootController = function ($rootScope, $scope, $location, $route, $interval, Skus, Carts) {
            $rootScope.womenSkus = [];
            $rootScope.menSkus = [];
            $rootScope.decorSkus = [];
            $rootScope.user = [];
            $scope.cartData = [];
            $scope.total = 0;
            var getCartDetails = function(){
                Carts.getCartDetails({},
                    function(data){
                        $scope.cartData = data;
                        angular.forEach($scope.cartData, function(cart){
                            $scope.total += parseInt(cart.product_data.quantity * cart.product_info[0].price);
                        });
                    },
                    function (error) {
                        console.log(error);
                    });
            };
            var init = function () {
                Skus.getSkus({},
                    function (data) {
                        angular.forEach(data, function (item, key) {
                            if (item.parent_sku_category == 'women') {
                                $rootScope.womenSkus.push(item);
                            } else if ((item.parent_sku_category == 'men')) {
                                $rootScope.menSkus.push(item);
                            } else if (item.parent_sku_category == 'decor') {
                                $rootScope.decorSkus.push(item);
                            }
                        });
                    },
                    function (error) {
                        console.log(error);
                    });
                getCartDetails();

            };
            $scope.deleteItemFromCart =  function(cart) {
                var payload = {};
                payload.cart_item_guid = cart.cart_item_guid;
                Carts.deleteItem(payload, function(data){
                    getCartDetails();
                })
            };

            $scope.editItemInCart =  function(cart) {
                $scope.loadRoute('/shopping_cart');
            };

            $scope.getSkuProducts = function (sku_guid) {
                $rootScope.sku_guid = sku_guid;
                $scope.loadRoute('/grid');
            };

            $scope.loadRoute = function (path) {
                path == $location.path() ? $route.reload() : $location.path(path);
            };

            init();
        }])
;