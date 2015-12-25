angular.module('user', ['urn.services'])
    .controller('DashboardController', ['$rootScope', '$scope',
        DashboardController = function ($rootScope, $scope) {
            var init = function () {
            };
            init();
        }])

    .controller('LoginController', ['$rootScope', '$scope', '$cookies', 'UserLogin', 'Whoami', 'UserRegister',
        LoginController = function ($rootScope, $scope, $cookies, UserLogin, Whoami, UserRegister) {
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
                        $cookies.put('auth-token', data.token);
                        $rootScope.user_guid = data.user_guid;
                        Whoami.getUserDetails({},
                            function (data) {
                                $rootScope.user = data;
                                // TODO: Add logic to set username on home page and redirect to home page.
                            },
                            function (error) {
                                console.log(error);
                            });
                    },
                    function (error) {
                        $scope.error = error.data;
                    });
            };

            //var registration_validator = function($scope) {
            //
            //};

            $scope.reg_submit = function () {
                $scope.reg_error = false;
                //registration_validator($scope);

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
                        $cookies.put('auth-token', data.token);
                        $rootScope.user_guid = data.user_guid;
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

    .controller('CartController', ['$rootScope', '$scope', '$cookies', 'Carts',
        CartController = function ($rootScope, $scope, $cookies, Carts) {
            $scope.deleteAllItemsFromCart = function(cartData) {
                angular.forEach(cartData, function(cart){
                    $rootScope.deleteItemFromCart(cart);
                });
            };

            $scope.updateCartItems = function(cartData) {
                angular.forEach(cartData, function(cart){
                    var payload = {};
                    payload.cart_item_guid = cart.cart_item_guid;
                    payload.product_data = JSON.stringify(cart.product_data);
                    Carts.updateCart(JSON.stringify(payload), function(data){
                        $rootScope.getCartDetails();
                        console.log(data);
                }, function(error) {
                    console.log(error);
                })
                })
            };
            var init = function () {
            };
            init();
        }])

    .controller('WishlistController', ['$rootScope', '$scope',
        WishlistController = function ($rootScope, $scope) {
            var init = function () {
            };
            init();
        }])
;