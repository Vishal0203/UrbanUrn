angular.module('user', ['urn.services'])
    .controller('DashboardController', ['$rootScope', '$scope',
        DashboardController = function ($rootScope, $scope) {
            var init = function () {
            };
            init();
        }])

    .controller('LoginController', ['$rootScope', '$scope', '$cookies', 'UserLogin', 'Whoami',
        LoginController = function ($rootScope, $scope, $cookies, UserLogin, Whoami) {
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
            init();
        }])

    .controller('AddressController', ['$rootScope', '$scope',
        AddressController = function ($rootScope, $scope) {
            var init = function () {
            };
            init();
        }])

    .controller('CartController', ['$rootScope', '$scope',
        CartController = function ($rootScope, $scope) {
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