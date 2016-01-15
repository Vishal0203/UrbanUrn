angular.module('order', ['urn.services'])
    .controller('CheckoutController', ['$rootScope', '$scope', '$window', 'Address', 'Orders',
        CheckoutController = function ($rootScope, $scope, $window, Address, Orders) {
            $scope.createBillingAddress = 'same';
            $scope.createShippingAddress = 'same';
            $scope.displayItems = [{show: true}, {show: false}, {show: false}, {show: false}];
            $scope.newBillingAddress = {};
            $scope.newShippingAddress = {};
            $scope.saveBillingAddress = false;
            $scope.hideDetails = true;
            $scope.saveShippingAddress = false;
            $scope.useBillingAddress = false;
            $scope.paymentInfo = {};
            $scope.selectedAddressGuid = '';
            $scope.selectedBillingAddressGuid = '';
            $rootScope.orderDetail = '';
            $scope.updateDetailsBilling = function () {
                if ($scope.createBillingAddress == 'diff') {
                    $scope.selectedBillingAddress = $scope.newBillingAddress;
                }
                if ($scope.saveBillingAddress) {
                    Address.add(JSON.stringify($scope.newBillingAddress), function (data) {
                        $rootScope.user.addresses = data.addresses;
                        $scope.selectedBillingAddressGuid = data.address;
                    }, function (error) {
                        console.log(error);
                    })
                }

            };
            $scope.updateShippingAddress = function () {
                if ($scope.useBillingAddress) {
                    $scope.newShippingAddress = $scope.selectedBillingAddress;
                }
            };
            $scope.updateDetailsShipping = function () {
                if ($scope.createShippingAddress == 'diff') {
                    $scope.selectedShippingAddress = $scope.newShippingAddress;
                    $scope.selectedAddressGuid = $scope.selectedBillingAddressGuid ;
                }
                else {
                    $scope.selectedAddressGuid = $scope.selectedShippingAddress.address_guid;
                }
                if ($scope.saveShippingAddress) {
                    Address.add(JSON.stringify($scope.newShippingAddress), function (data) {
                        $scope.selectedAddressGuid = data.address;
                        $rootScope.user.addresses = data.addresses;
                    }, function (error) {
                        console.log(error);
                    })
                }

            };
            $scope.updateOnContinue = function (index) {
                $scope.displayItems[index].show = false;
                if (index != 3) {
                    $scope.displayItems[index + 1].show = true;
                }
            };

            $scope.sendPaymentDetails = function () {
                var payload = {};
                payload.products = [];
                angular.forEach($rootScope.cartData, function (cart) {
                    var product = {};
                    product.cart_item_guid = cart.cart_item_guid;
                    product.total_cost = cart.product_data.quantity * cart.product_info[0].price;
                    payload.products.push(product);
                });
                payload.final_cost = $rootScope.total;
                payload.address_guid = $scope.selectedAddressGuid;
                Orders.place(JSON.stringify(payload), function (data) {
                        $rootScope.navigateToOrders(data[0])
                }, function (error) {
                    console.log(error);
                });
            };

            var init = function () {
                if ($rootScope.user == undefined) {
                    if ($window.localStorage.getItem('user-data')) {
                        $rootScope.user = JSON.parse($window.localStorage.getItem('user-data'));
                    } else {
                        $rootScope.loadRoute('/home');
                    }
                }
                $scope.selectedBillingAddress = $rootScope.user.addresses[0];
                $scope.selectedShippingAddress = $rootScope.user.addresses[0];
            };
            init();
        }])
    .controller('OrdersController', ['$rootScope', '$scope', '$window',
        OrdersController = function ($rootScope, $scope, $window) {
            var init = function () {
                if ($window.localStorage.getItem('selected-order')) {
                        $rootScope.orderDetail = JSON.parse($window.localStorage.getItem('selected-order'));
                    } else {
                        $rootScope.loadRoute('/home');
                    }
            };
            init();
        }])
;