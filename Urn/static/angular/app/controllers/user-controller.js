angular.module('user', ['urn.services'])
    .controller('DashboardController', ['$rootScope', '$scope',
        DashboardController = function ($rootScope, $scope) {
            var init = function () {
            };
            init();
        }])

    .controller('LoginController', ['$rootScope', '$scope', 'UserLogin',
        LoginController = function ($rootScope, $scope, UserLogin) {
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
                       // TODO: Set the JWT token received in response in $cookies service and user_guid in rootscope and redirect to home page
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