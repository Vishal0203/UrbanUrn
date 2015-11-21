<h1><a href="#api-documentation" name="api-documentation" id="api-documentation" class="anchor"></a>API Documentation</h1>
<p>This page describes the API's along with their payloads and expected results<br/>
<h4><a href="#login" name="login" id="logiin" class="anchor"></a>Login</h4>
<table>
  <thead>
    <tr>
      <th>Method </th>
      <th align="center">Access Right </th>
      <th align="center">Endpoint and payload </th>
      <th align="center">Expected response </th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        POST
      </td>
      <td>
        Super user and Staff
      </td>
      <td>
      <b>Endpoint : </b> api/v1_0/login
      <br><br>
<pre lang="javascript">
{
    "username":string,
	"password": string
}
</pre>
      </td>
      <td>
<pre lang="javascript">
{
    "success": {"token": token, "user_guid":uuid}
    "error": Eror reason
}
</pre>
      </td>
    </tr>
  </tbody>
</table>
<h4><a href="#logout" name="logout" id="logout" class="anchor"></a>Log Out</h4>
<table>
  <thead>
    <tr>
      <th>Method </th>
      <th align="center">Access Right </th>
      <th align="center">Endpoint and payload </th>
      <th align="center">Expected response </th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        Get
      </td>
      <td>
        General User
      </td>
      <td>
      <b>Endpoint : </b> api/v1_0/logout
      <br><br>
<pre lang="javascript">
</pre>
      </td>
      <td>
<pre lang="javascript">
{
    "success": "Logged Out"
    "error": Eror reason
}
</pre>
      </td>
    </tr>
  </tbody>
</table>
<h4><a href="#coupons" name="coupons" id="coupons" class="anchor"></a>Coupons</h4>
<table>
  <thead>
    <tr>
      <th>Method </th>
      <th align="center">Access Right </th>
      <th align="center">Endpoint and payload </th>
      <th align="center">Expected response </th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        POST  
      </td>
      <td>
        Super user and Staff
      </td>
      <td>
      <b>Endpoint : </b> api/v1_0/coupons
      <br><br>
<pre lang="javascript">
{
    "coupons": [
        {
            "code": string,
            "discount_value": number,
            "is_percentage": boolean
        },
    ]
}
</pre>
      </td>
      <td>
<pre lang="javascript">
{
    "success": list of coupon codes
    "error": list of coupon codes
}
</pre>        
      </td>
    </tr>
    <tr>
        <td>POST</td>
        <td>General User</td>
        <td>
        <b>Endpoint : </b> api/v1_0/coupons
        <br><br>
<pre lang="javascript">
{
    "code": string
}
</pre>
        </td>
        <td>
<pre lang="javascript">
{
    "coupon_guid": String,
    "discount_value": number,
    "is_percentage": boolean
}
</pre>
        </td>
    </tr>
  </tbody>
</table>
<h4><a href="#reviews" name="reviews" id="reviews" class="anchor"></a>Reviews</h4>
<table>
  <thead>
    <tr>
      <th>Method </th>
      <th align="center">Access Right </th>
      <th align="center">Endpoint and payload </th>
      <th align="center">Expected response </th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        POST
      </td>
      <td>
        Any Authenticated User
      </td>
      <td>
      <b>Endpoint : </b> api/v1_0/reviews
      <br><br>
<pre lang="javascript">
{
    "rating": number,
    "product_guid": string,
    "review_comment": string
}
</pre>
      </td>
      <td>
<pre lang="javascript">
{
    "success": {"review_guid": uuid, "reviewer_name": user, "review_comment": string}
    "error": Error Reason
}
</pre>
      </td>
    </tr>
    <tr>
        <td>PUT</td>
        <td>General User</td>
        <td>
        <b>Endpoint : </b> api/v1_0/reviews
        <br><br>
<pre lang="javascript">
{
    "review_guid": uuid,
    "rating": number,
    "review_detail": string
}
</pre>
        </td>
        <td>
<pre lang="javascript">
{
    "success": "Review Updated",
    "error": Error Message,
}
</pre>
        </td>
    </tr>
	<tr>
        <td>DELETE</td>
        <td>General User</td>
        <td>
        <b>Endpoint : </b> api/v1_0/reviews
        <br><br>
<pre lang="javascript">
{
    "review_guid": uuid
}
</pre>
        </td>
        <td>
<pre lang="javascript">
{
    "success": "Review Deleted",
    "error": Error Message,
}
</pre>
        </td>
    </tr>
  </tbody>
</table>
<h4><a href="#wishlists" name="wishlists" id="wishlists" class="anchor"></a>WishList</h4>
<table>
  <thead>
    <tr>
      <th>Method </th>
      <th align="center">Access Right </th>
      <th align="center">Endpoint and payload </th>
      <th align="center">Expected response </th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        POST
      </td>
      <td>
        Any Authenticated User
      </td>
      <td>
      <b>Endpoint : </b> api/v1_0/wishlists
      <br><br>
<pre lang="javascript">
{
    "product_guid": string,
    "product_data": string
}
</pre>
      </td>
      <td>
<pre lang="javascript">
{
    "success": "product added to wishlist"
    "error": Error Reason
}
</pre>
      </td>
    </tr>
    <tr>
        <td>GET</td>
        <td>General User</td>
        <td>
        <b>Endpoint : </b> api/v1_0/wishlists
        <br><br>
<pre lang="javascript">
</pre>
        </td>
        <td>
<pre lang="javascript">
{
    "success": type: Array , Object : [
  {
    "wishlist_guid": uuid,
    "product_guid": uuid,
    "product_name": string,
    "product_data": string
  }
  ],
    "error": Error Message,
}
</pre>
        </td>
    </tr>
	<tr>
        <td>DELETE</td>
        <td>General User</td>
        <td>
        <b>Endpoint : </b> api/v1_0/wishlists
        <br><br>
<pre lang="javascript">
{
    "wishlist_guid": uuid
}
</pre>
        </td>
        <td>
<pre lang="javascript">
{
    "success": "Product removed from wish list",
    "error": Error Message,
}
</pre>
        </td>
    </tr>
  </tbody>
</table>
<h4><a href="#discounts" name="discounts" id="discounts" class="anchor"></a>Discounts</h4>
<table>
  <thead>
    <tr>
      <th>Method </th>
      <th align="center">Access Right </th>
      <th align="center">Endpoint and payload </th>
      <th align="center">Expected response </th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        POST
      </td>
      <td>
        Business or Superuser
      </td>
      <td>
      <b>Endpoint : </b> api/v1_0/discounts
      <br><br>
<pre lang="javascript">
{
    "product_guid": uuid,
    "description": string,
    "start_time": datetime,
    "end_time": datetime,
    "discount_value": number,
    "is_percentage": boolean,
    "product_quantity": number,
	"active" : active
}
</pre>
      </td>
      <td>
<pre lang="javascript">
{
    "success": {discount_guid: uuid}
    "error": Error Reason
}
</pre>
      </td>
    </tr>
    <tr>
        <td>GET</td>
        <td>Business or Superuser</td>
        <td>
        <b>Endpoint : </b> api/v1_0/discounts?product_guid=guid
        <br><br>
<pre lang="javascript">
</pre>
        </td>
        <td>
<pre lang="javascript">
{
    "success": type: Array , Object : [
  {
    "discount_guid": uuid,
    "description": string,
    "discount_value": number,
    "start_time": datetime,
    "end_time": datetime,
    "product_quantity": number,
    "is_percentage": boolean,
    "created_on": datetime,
    "updated_on": datetime
  }
  ],
    "error": Error Message,
}
</pre>
        </td>
    </tr>
	<tr>
        <td>PUT</td>
        <td>Business user or Superuser</td>
        <td>
        <b>Endpoint : </b> api/v1_0/discounts
        <br><br>
<pre lang="javascript">
{
    "discount_guid": uuid,
	"product_guid": uuid,
    "description": string,
    "start_time": datetime,
    "end_time": datetime,
    "discount_value": number,
    "is_percentage": boolean,
    "product_quantity": number,
	"active" : active
}
</pre>
        </td>
        <td>
<pre lang="javascript">
{
    "success": {discount_guid: uuid},
    "error": Error Message,
}
</pre>
        </td>
    </tr>
  </tbody>
</table>
<h4><a href="#carts" name="carts" id="carts" class="anchor"></a>Carts</h4>
<table>
  <thead>
    <tr>
      <th>Method </th>
      <th align="center">Access Right </th>
      <th align="center">Endpoint and payload </th>
      <th align="center">Expected response </th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        POST
      </td>
      <td>
        General User
      </td>
      <td>
      <b>Endpoint : </b> api/v1_0/carts
      <br><br>
<pre lang="javascript">
{
    "product_guid":uuid,
    "product_data": string
}
</pre>
      </td>
      <td>
<pre lang="javascript">
{
    "success": {cart_item_guid: uuid}
    "error": Error Reason
}
</pre>
      </td>
    </tr>
    <tr>
        <td>GET</td>
        <td>Business or Superuser</td>
        <td>
        <b>Endpoint : </b> api/v1_0/discounts?product_guid=guid
        <br><br>
<pre lang="javascript">
</pre>
        </td>
        <td>
<pre lang="javascript">
{
    "success": type: Array , Object : [
  {
    "cart_item_guid": uuid,
    "product_info": [
      {
        "product_guid": uuid,
        "name": string,
        "discount_info": [
          {
            "discount_guid": uuid,
            "description": string,
            "discount_value": number,
            "start_time": datetime,
            "end_time": datetime,
            "product_quantity": number,
            "is_percentage": boolean,
            "created_on": datetime,
            "updated_on": datetime
          }
        ],
        "reviews_info": [
          {
            "review_guid": uuid,
            "rating": string,
            "review_detail": string,
            "user_id": number,
            "business_id": number,
            "created_on": datetime,
            "updated_on": datetime
          }
        ],
        "description": string,
        "price": number,
        "product_data": {
          "quantity": "number"
        },
        "product_images": [],
        "business_guid": uuid,
        "sku_guid": uuid,
        "created_on": datetime,
        "updated_on": datetime
      }
  ],
    "error": Error Message,
}
</pre>
        </td>
    </tr>
	<tr>
        <td>PUT</td>
        <td>Any General user</td>
        <td>
        <b>Endpoint : </b> api/v1_0/carts
        <br><br>
<pre lang="javascript">
{
    "cart_item_guid": uuid,
	"product_data": string
}
</pre>
        </td>
        <td>
<pre lang="javascript">
{
    "success": "Cart product Updated",
    "error": Error Message,
}
</pre>
        </td>
    </tr>
  </tbody>
</table>
<h4><a href="#productsearh" name="productsearh" id="productsearh" class="anchor"></a>Search</h4>
<table>
  <thead>
    <tr>
      <th>Method </th>
      <th align="center">Access Right </th>
      <th align="center">Endpoint and payload </th>
      <th align="center">Expected response </th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        POST
      </td>
      <td>
        General User
      </td>
      <td>
      <b>Endpoint : </b> api/v1_0/product/search?filter=filterstring
      <br><br>
<pre lang="javascript">
</pre>
      </td>
      <td>
<pre lang="javascript">
{
    "success": type: Array, Object: [
  {
    "product_guid": uuid,
    "description": string,
    "name": string,
    "sku_guid": uuid
  }
  ]
    "error": Error Reason
}
</pre>
      </td>
    </tr>
  </tbody>
</table>