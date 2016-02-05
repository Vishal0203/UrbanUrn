angular.module('urn', [
    'ngRoute', 'ngAnimate', 'urn.services','chieffancypants.loadingBar',
    'blog', 'misc', 'order', 'product', 'user'
])
  .config(function(cfpLoadingBarProvider) {
    cfpLoadingBarProvider.includeSpinner = false;
  });