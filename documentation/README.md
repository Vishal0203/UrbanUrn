<h1><a href="#api-documentation" name="api-documentation" id="api-documentation" class="anchor"></a>API Documentation</h1>
<p>This page describes the API's along with their payloads and expected results<br/><em>The content below this line is to be removed while pushing the changes on this page. Remove this line too.</em></p>
<h4><a href="#api-name" name="api-name" id="api-name" class="anchor"></a>API Name</h4>
<p>Description of this API</p>
<table>
  <thead>
    <tr>
      <th>Method </th>
      <th align="center">Endpoint and payload </th>
      <th align="right">Expected response </th>
    </tr>
  </thead>
</table>
<p><em>Same goes for each API. Remove this line too.</em></p>
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