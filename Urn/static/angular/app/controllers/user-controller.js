angular.module('user', ['urn.services'])
    .controller('DashboardController', ['$rootScope', '$scope','Orders',
        DashboardController = function ($rootScope, $scope, Orders) {
            $scope.orderData = '';
            var init = function () {
                Orders.get({}, function(data) {
                    $scope.orderData = data;
                })
            };
            init();
        }])

    .controller('LoginController', ['$rootScope', '$scope', '$window', '$location', 'UserLogin', 'Whoami', 'UserRegister',
        LoginController = function ($rootScope, $scope, $window, $location, UserLogin, Whoami, UserRegister) {
            var init = function () {
            };
            $scope.submit = function () {
                $scope.error = false;
                if ($scope.username == undefined || $scope.username == '') {
                    $scope.error = 'Please enter username of the registered user';
                    return;
                }
                if ($scope.password == undefined || $scope.password == '') {
                    $scope.error = 'Please enter password of the registered user';
                    return;
                }
                var payload = {};
                payload.username = $scope.username;
                payload.password = $scope.password;
                UserLogin.login(payload,
                    function (data) {
                        $window.localStorage.setItem('auth-token', data.token);
                        $rootScope.user_guid = data.user_guid;
                        Whoami.getUserDetails({},
                            function (data) {
                                $rootScope.user = data;
                                $window.localStorage.setItem('user-data', JSON.stringify(data));
                                $rootScope.is_loggedin = true;
                                $location.path('/home');
                            },
                            function (error) {
                                console.log(error);
                            });
                        $rootScope.getCartDetails();
                    },
                    function (error) {
                        $scope.error = error.data;
                    });
            };

            $scope.reg_submit = function () {
                $scope.reg_error = false;

                var payload = {};
                payload.username = $scope.reg_username;
                payload.email = $scope.reg_email;
                payload.password = $scope.reg_password;
                payload.confirm_password = $scope.reg_confirm_password;
                payload.first_name = $scope.reg_first_name;
                payload.last_name = $scope.reg_last_name;
                payload.phone = $scope.reg_phone;

                UserRegister.register(payload,
                    function (data) {
                        $window.localStorage.setItem('auth-token', data.token);
                        $rootScope.user_guid = data.user_guid;
                        Whoami.getUserDetails({},
                            function (data) {
                                $rootScope.user = data;
                                $window.localStorage.setItem('user-data', JSON.stringify(data));
                                $rootScope.is_loggedin = true;
                                $scope.dismiss();
                                $location.path('/home');
                            },
                            function (error) {
                                console.log(error);
                            });
                    },
                    function (error) {
                        $scope.reg_error = error.data;
                    });
            };

            init();
        }])

    .controller('AddressController', ['$rootScope', '$scope',
        AddressController = function ($rootScope, $scope) {
            var init = function () {
            };
            init();
        }])

    .controller('CartController', ['$rootScope', '$scope', '$window', 'Carts',
        CartController = function ($rootScope, $scope, $window, Carts) {
            $scope.deleteAllItemsFromCart = function (cartData) {
                angular.forEach(cartData, function (cart) {
                    $rootScope.deleteItemFromCart(cart);
                });
            };

            $scope.updateCartItems = function (cartData) {
                angular.forEach(cartData, function (cart) {
                    var payload = {};
                    payload.cart_item_guid = cart.cart_item_guid;
                    payload.product_data = JSON.stringify(cart.product_data);
                    Carts.updateCart(JSON.stringify(payload), function (data) {
                        $rootScope.getCartDetails();
                    }, function (error) {
                        console.log(error);
                    })
                })
            };
            var init = function () {
                $rootScope.getCartDetails();
            };
            init();
        }])

    .controller('WishlistController', ['$rootScope', '$scope', 'WishList', 'Carts',
        WishlistController = function ($rootScope, $scope, WishList, Carts) {
            $scope.wishlistData = [];
            var init = function () {
                WishList.getWishlist(
                    function (data) {
                        $scope.wishlistData = data;
                    },
                    function (error) {
                        console.log(error);
                    });
            };

            $scope.addItemsToCart = function () {
                var wishlist_guids = [];
                angular.forEach($scope.wishlistData, function (wishlist) {
                    wishlist_guids.push(wishlist.wishlist_guid);
                });
                var payload = {};
                payload.wishlist_guids = wishlist_guids;
                Carts.addItemsToCart(JSON.stringify(payload), function (data) {
                    $rootScope.loadRoute('/shopping_cart');
                }, function (error) {
                    console.log(error);
                })
            };

            $scope.addItemToCart = function (wishlist_guid) {
                var payload = {};
                payload.wishlist_guids = [wishlist_guid];
                Carts.addItemsToCart(JSON.stringify(payload), function (data) {
                    init();
                }, function (error) {
                    console.log(error);
                })
            };

            $scope.deleteWishlist = function (wishlist_guid) {
                WishList.deleteWishlist({'wishlist_guid': wishlist_guid}, function (data) {
                    init();
                }, function (error) {
                    console.log(error);
                });
            };

            init();
        }])
;