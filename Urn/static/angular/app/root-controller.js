angular.module('urn')
    .controller('RootController', ['$rootScope', '$scope', '$location', '$route', '$interval', '$window', 'Skus', 'Carts', 'WishList', 'UserLogout',
        RootController = function ($rootScope, $scope, $location, $route, $interval, $window, Skus, Carts, WishList, UserLogout) {
            $rootScope.cartData = [];
            $rootScope.total = 0;
            $rootScope.selectedProduct = {};

            $rootScope.getCartDetails = function () {
                    Carts.getCartDetails({},
                        function (data) {
                            $rootScope.total = 0;
                            $rootScope.cartData = data;
                            angular.forEach($rootScope.cartData, function (cart) {
                                $rootScope.total += parseInt(cart.product_data.quantity * cart.product_info[0].price);
                            });
                        },
                        function (error) {
                            console.log(error);
                        });
            };
            var init = function () {
                if ($window.localStorage.getItem('user-data')) {
                    $rootScope.user = JSON.parse($window.localStorage.getItem('user-data'));
                    $rootScope.is_loggedin = true;
                } else {
                    $rootScope.user = null;
                }
                Skus.getSkus({},
                    function (data) {
                        $rootScope.womenSkus = [];
                        $rootScope.menSkus = [];
                        $rootScope.decorSkus = [];
                        $rootScope.womenSkusGuid = '';
                        $rootScope.menSkusGuid = '';
                        $rootScope.decorSkusGuid = '';
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
                $rootScope.getCartDetails();
            };

            $rootScope.editItemInCart = function (cart) {
                $rootScope.selectedProduct = cart.product_info[0];
                $window.localStorage.setItem('selected-product', JSON.stringify($rootScope.selectedProduct));
                $rootScope.loadRoute('/product_detail/' + cart.product_info[0].name);
            };

             $rootScope.goToProduct = function (product) {
                $rootScope.selectedProduct = product;
                 $window.localStorage.setItem('selected-product', JSON.stringify($rootScope.selectedProduct));
                $rootScope.loadRoute('/product_detail/' + product.name);
            };

            $rootScope.deleteItemFromCart = function (cart) {
                var payload = {};
                payload.cart_item_guid = cart.cart_item_guid;
                Carts.deleteItem(payload, function (data) {
                    $rootScope.getCartDetails();
                }, function (error) {
                    console.log(error);
                })
            };

            $rootScope.addToWishlist = function (product) {
                var payload = {};
                payload.product_guid = product.product_guid;
                payload.product_data = product.product_data;
                WishList.addToWishlist(JSON.stringify(payload), function (data) {

                }, function (error) {
                    console.log(error);
                })
            };

            $rootScope.getSkuProducts = function (sku_guid) {
                $rootScope.search_query = undefined;
                $rootScope.sku_guid = sku_guid;
                $rootScope.loadRoute('/grid');
            };

            $rootScope.routeToCheckout = function() {
                if($rootScope.user){
                    $rootScope.loadRoute('/checkout');
                }
                else {
                    $rootScope.loadRoute('/login');
                }
            };

            $rootScope.loadRoute = function (path) {
                path == $location.path() ? $route.reload() : $location.path(path);
            };

            $rootScope.getUrl = function(name) {
                return "#/product_detail/"+ name;
            };

            $scope.logoutUser = function () {
                UserLogout.logout({},
                    function (data) {
                        $rootScope.is_loggedin = false;
                        $window.localStorage.clear();
                        $rootScope.loadRoute('/home');
                    },
                    function (error) {
                        console.log(error);
                    }
                )
            };

            $scope.searchProduct = function () {
                $rootScope.sku_guid = undefined;
                $rootScope.search_query = this.searchQuery;
                $rootScope.loadRoute('/grid');
            };

            init();
        }])
;