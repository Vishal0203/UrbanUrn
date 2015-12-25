angular.module('order', ['urn.services'])
    .controller('CheckoutController', ['$rootScope', '$scope','$cookies',
        CheckoutController = function ($rootScope, $scope, $cookies) {
            $scope.createAddress = 'same';
            $scope.selected = true;
            var init = function () {
                if ($rootScope.user == undefined) {
                    if ($cookies.getObject('user-data')) {
                        $rootScope.user = $cookies.getObject('user-data');
                    } else {
                        $rootScope.loadRoute('/home');
                    }
                }
                $scope.selectedAddress = $rootScope.user.addresses[0];
                console.log($rootScope.user);
            };
            init();
        }])
;