angular.module('urn')
    .controller('RootController', ['$rootScope', '$scope', '$location', '$route', '$interval', 'Skus',
        RootController = function ($rootScope, $scope, $location, $route, $interval, Skus) {
            $rootScope.womenSkus = [];
            $rootScope.menSkus = [];
            $rootScope.decorSkus = [];
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