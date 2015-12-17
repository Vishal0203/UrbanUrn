angular.module('urn')
    .controller('RootController', ['$rootScope', '$scope', '$location', '$route', '$interval', 'Skus',
        RootController = function ($rootScope, $scope, $location, $route, $interval, Skus) {
            $scope.womenSkus = [];
            $scope.menSkus = [];
            $scope.decorSkus = [];
            var init = function () {
                Skus.getSkus({},
                    function (data) {
                        angular.forEach(data, function (item, key) {
                            if (item.parent_sku_category == 'women') {
                                $scope.womenSkus.push(item);
                            } else if ((item.parent_sku_category == 'men')) {
                                $scope.menSkus.push(item);
                            } else if (item.parent_sku_category == 'decor') {
                                $scope.decorSkus.push(item);
                            }
                        });
                    },
                    function (error) {
                        console.log(error);
                    });
            };
            init();
        }])
;