angular.module('urn.services', ['urn.models'])
	.factory('Products', function( $resource, ApiUrls){
		return $resource(ApiUrls.products,{},
		{
			getProducts : {method : "GET", isArray : true}
		})
	})
;