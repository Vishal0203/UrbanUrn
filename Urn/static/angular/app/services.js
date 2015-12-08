angular.module('urn.services', ['urn.models'])
	.factory('Products', function( $resource, ApiUrls){
		return $resource(ApiUrls.products,{},
		{
			getProducts : {method : "GET", isArray : true}
		})
	})
	.factory('UserLogin', function( $resource, ApiUrls){
		return $resource(ApiUrls.login,{},
		{
			login : {method : "POST"}
		})
	})
;