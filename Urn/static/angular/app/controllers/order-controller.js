angular.module('order', ['urn.services'])
    .controller('CheckoutController', ['$rootScope', '$scope','$cookies','Address','Orders',
        CheckoutController = function ($rootScope, $scope, $cookies, Address, Orders) {
            $scope.createBillingAddress = 'same';
            $scope.createShippingAddress = 'same';
            $scope.displayItems = [{show : true},{show : false}, {show : false}, {show : false}];
            $scope.newBillingAddress = {};
            $scope.newShippingAddress = {};
            $scope.saveBillingAddress =  false;
            $scope.hideDetails =  true;
            $scope.saveShippingAddress =  false;
            $scope.useBillingAddress = false;
            $scope.paymentInfo = {};
            $scope.selectedAddressGuid = '';
            $rootScope.orderDetail = '';
            $scope.updateDetailsBilling = function() {
                if($scope.createBillingAddress == 'diff'){
                    $scope.selectedBillingAddress = $scope.newBillingAddress;
                }
                if($scope.saveBillingAddress){
                  Address.add(JSON.stringify($scope.newBillingAddress), function(data){
                      $rootScope.user.addresses = data.addresses;
                  }, function (error) {
                      console.log(error);
                  })
                }

            };
            $scope.updateShippingAddress = function(){
                if($scope.useBillingAddress) {
                    $scope.newShippingAddress = $scope.selectedBillingAddress;
                }
            };
            $scope.updateDetailsShipping = function() {
                if($scope.createShippingAddress == 'diff'){
                    $scope.selectedShippingAddress = $scope.newShippingAddress;
                }
                else {
                    $scope.selectedAddressGuid = $scope.selectedShippingAddress.address_guid;
                }
                if($scope.saveShippingAddress){
                  Address.add(JSON.stringify($scope.newShippingAddress), function(data){
                      $scope.selectedAddressGuid = data.address;
                      $rootScope.user.addresses = data.addresses;
                  }, function (error) {
                      console.log(error);
                  })
                }

            };
            $scope.updateOnContinue= function(index){
              $scope.displayItems[index].show = false;
              if(index!=3){
                  $scope.displayItems[index+1].show = true;
              }
            };
            $scope.updateDisplay = function(index) {
                angular.forEach($scope.displayItems, function(data, key){
                    if(key==index){
                        data.show=!data.show;
                    }
                    else {
                        data.show=false;
                    }
                });
            };
            $scope.sendPaymentDetails = function() {
              console.log($scope.paymentInfo);
              var payload = {};
              payload.products = [];
              angular.forEach($rootScope.cartData, function(cart){
                 var product = {};
                 product.cart_item_guid = cart.cart_item_guid;
                 product.total_cost = cart.product_data.quantity * cart.product_info[0].price;
                 payload.products.push(product);
              });
              payload.final_cost = $rootScope.total;
              payload.address_guid = $scope.selectedAddressGuid;
              console.log(payload);
              Orders.place(JSON.stringify(payload), function(data){
                  $rootScope.orderDetail = data[0];
                  $rootScope.loadRoute("/orders/"+ $rootScope.orderDetail.id);
              }, function(error){
                  console.log(error);
              });
            };
            var init = function () {
                if ($rootScope.user == undefined) {
                    if ($cookies.getObject('user-data')) {
                        $rootScope.user = $cookies.getObject('user-data');
                    } else {
                        $rootScope.loadRoute('/home');
                    }
                }
                $scope.selectedBillingAddress = $rootScope.user.addresses[0];
                $scope.selectedShippingAddress = $rootScope.user.addresses[0];
                console.log($rootScope.user);
            };
            init();
        }])
    .controller('OrdersController', ['$rootScope', '$scope', '$cookies', 'Orders',
        OrdersController = function ($rootScope, $scope, $cookies, Orders) {
            var init = function () {
            };
            init();
        }])
;