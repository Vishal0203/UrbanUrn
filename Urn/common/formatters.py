from collections import OrderedDict

from UrbanUrn import settings
from Urn.common.utils import convert_uuid_string
from Urn.common import utils
from Urn.models import Addresses, BusinessUsers, OrderDetails, ProductImages, Reviews, Sku


def format_get_businesses(businesses, include_users=False, include_addresses=False, user=None):
    businesses_data = []
    for business in businesses:
        business_data = OrderedDict()
        business_data['business_guid'] = utils.convert_uuid_string(business.business_guid)
        business_data['name'] = business.name
        business_data['category'] = business.category
        business_data['description'] = business.description
        business_data['business_image'] = business.business_image

        if include_users:
            business_users = business.users.all()
            business_data['users'] = format_get_business_users(business_users, business)

        if include_addresses:
            business_addresses = Addresses.objects.filter(business_id=business.business_id)
            business_data['addresses'] = format_addresses(business_addresses)

        if user:
            business_data['role'] = get_business_user_entry(business, user).role

        business_data['created_by'] = business.created_by.user.username
        business_data['updated_by'] = business.updated_by.user.username if business.updated_by is not None else None
        business_data['created_on'] = utils.format_timestamp(business.created_on)
        business_data['updated_on'] = utils.format_timestamp(
            business.updated_on) if business.updated_on is not None else None
        businesses_data.append(business_data)
    return businesses_data


def format_get_business_users(business_users, business):
    business_users_data = []
    for business_user in business_users:
        business_user_data = OrderedDict()
        business_user_data['user_guid'] = utils.convert_uuid_string(business_user.user_guid)
        business_user_data['username'] = business_user.user.username
        business_user_data['role'] = get_business_user_entry(business, business_user).role
        business_user_data['first_name'] = business_user.user.first_name
        business_user_data['last_name'] = business_user.user.last_name
        business_user_data['email'] = business_user.user.email
        business_user_data['phone'] = business_user.phone
        business_user_data['status'] = business_user.status
        business_user_data['created_on'] = utils.format_timestamp(business_user.created_on)
        business_user_data['updated_on'] = utils.format_timestamp(
            business_user.updated_on) if business_user.updated_on is not None else None
        business_users_data.append(business_user_data)
    return business_users_data


def get_business_user_entry(business, user):
    return BusinessUsers.objects.get(business=business, user=user)


def format_user(user):
    user_data = OrderedDict()
    user_data['user_guid'] = utils.convert_uuid_string(user.user_profile.user_guid)
    user_data['username'] = user.username
    user_data['first_name'] = user.first_name
    user_data['last_name'] = user.last_name
    user_data['email'] = user.email
    user_data['phone'] = user.user_profile.phone
    user_data['status'] = user.user_profile.status

    user_addresses = Addresses.objects.filter(user_id=user.user_profile.user_id)
    user_data['addresses'] = format_addresses(user_addresses)

    if user.user_profile.is_business_user:
        user_businesses = user.user_profile.businesses_set.all()
        user_data['businesses'] = format_get_businesses(user_businesses, False, False, user.user_profile)

    # TODO Orders,wishlist and Carts
    # users_wishlist = user.user_profile.wishlist_set.all()
    # user_data['wishlist'] = format_wishlist_get(users_wishlist)
    # users_cart = user.user_profile.cartitems_set.all()
    # user_data['cart'] = format_carts(users_cart)


    user_data['push_notification'] = user.user_profile.push_notification
    user_data['email_notification'] = user.user_profile.email_notification
    user_data['sms_notification'] = user.user_profile.sms_notification
    user_data['is_business_user'] = user.user_profile.is_business_user
    user_data['is_superuser'] = user.is_superuser
    user_data['is_staff'] = user.is_staff
    user_data['last_login'] = utils.format_timestamp(user.last_login) if user.last_login is not None else None
    user_data['created_on'] = utils.format_timestamp(user.user_profile.created_on)
    user_data['updated_on'] = utils.format_timestamp(
        user.user_profile.updated_on) if user.user_profile.updated_on is not None else None
    return user_data


def format_wishlist_get(users_wishlist):
    response = list()
    for item in users_wishlist:
        item_dict = OrderedDict()
        item_dict["wishlist_guid"] = convert_uuid_string(item.wishlist_guid)
        item_dict["product_guid"] = convert_uuid_string(item.product.product_guid)
        item_dict["product_name"] = item.product.name
        item_dict["product_data"] = item.product_data
        item_dict["product_price"] = item.product.price
        item_dict["product_description"] = item.product.description
        product_images = ProductImages.objects.filter(product_id=item.product.product_id).order_by('image')
        item_dict['product_images'] = format_product_images(product_images,
                                                            False) if len(product_images) > 0 else []
        response.append(item_dict)

    return response


def format_addresses(addresses):
    addresses_data = []
    for address in addresses:
        address_data = OrderedDict()
        address_data['address_guid'] = utils.convert_uuid_string(address.address_guid)
        address_data['is_default'] = address.is_default
        address_data['street_1'] = address.street_1
        address_data['street_2'] = address.street_2
        address_data['city'] = address.city
        address_data['state'] = address.state
        address_data['country'] = address.country
        address_data['pincode'] = address.pincode
        address_data['latitude'] = address.latitude
        address_data['longitude'] = address.longitude
        address_data['created_on'] = utils.format_timestamp(address.created_on)
        address_data['updated_on'] = utils.format_timestamp(
            address.updated_on) if address.updated_on is not None else None
        addresses_data.append(address_data)
    return addresses_data


def format_carts(cart_items):
    cart_items_data = []
    for item in cart_items:
        cart_item_data = OrderedDict()
        cart_item_data["cart_item_guid"] = utils.convert_uuid_string(item.cart_item_guid)
        cart_item_data["product_info"] = format_products([item.product], False)
        cart_item_data["product_data"] = item.product_data
        cart_item_data["created_on"] = utils.format_timestamp(item.created_on)
        cart_item_data["updated_on"] = utils.format_timestamp(
            item.updated_on) if item.updated_on is not None else None
        cart_items_data.append(cart_item_data)
    return cart_items_data


def format_sku_parent(parent_sku, final_sku_data, is_child=False):
    if is_child:
        response = final_sku_data
    else:
        response = OrderedDict()
        response['children'] = final_sku_data
        response['parent_sku_name'] = parent_sku.name
        response['parent_sku_guid'] = utils.convert_uuid_string(parent_sku.sku_guid)
    if parent_sku.category:
        response['parent_sku_category'] = parent_sku.category
    else:
        grandparent = Sku.objects.get(sku_id=parent_sku.parent_sku_id)
        response['parent_sku_category'] = grandparent.category
    return response


def format_skus(sku, products):
    sku_data = OrderedDict()
    sku_data['sku_guid'] = utils.convert_uuid_string(sku.sku_guid)
    sku_data['name'] = sku.name
    sku_data['description'] = sku.description
    sku_data['products'] = format_products(products, False) if products is not None else []
    sku_data['created_by'] = sku.created_by.user.username
    sku_data['updated_by'] = sku.updated_by.user.username if sku.updated_by is not None else None
    sku_data['created_on'] = utils.format_timestamp(sku.created_on)
    sku_data['updated_on'] = utils.format_timestamp(sku.updated_on) if sku.updated_on is not None else None
    return sku_data


def format_products(products, json=True):
    products_data = []
    for product in products:
        product_images = ProductImages.objects.filter(product_id=product.product_id).order_by('image')
        product_data = OrderedDict()
        product_data['product_guid'] = utils.convert_uuid_string(product.product_guid)
        product_data['name'] = product.name
        product_data['discount_info'] = format_discounts(product.discounts_set.filter())
        product_data['reviews_info'] = format_reviews(Reviews.objects.filter(product_id=product.product_id))
        product_data['description'] = product.description
        product_data['price'] = product.price
        product_data['product_data'] = product.product_data
        product_data['product_images'] = format_product_images(product_images,
                                                               False) if len(product_images) > 0 else []
        product_data['business_guid'] = utils.convert_uuid_string(product.business.business_guid)
        product_data['sku_guid'] = utils.convert_uuid_string(product.sku.sku_guid)
        if product.sku.parent_sku_id:
            product_data['parent_sku_guid'] = utils.convert_uuid_string(Sku.objects.filter(
                sku_id=product.sku.parent_sku_id).get().sku_guid)
        product_data['is_fragile'] = product.is_fragile
        product_data['created_on'] = utils.format_timestamp(product.created_on)
        product_data['updated_on'] = utils.format_timestamp(
            product.updated_on) if product.updated_on is not None else None
        products_data.append(product_data)
    if json:
        return utils.build_json(products_data)
    return products_data


def format_product_images(product_images, json=True):
    product_images_data = []
    for product_image in product_images:
        product_image_data = OrderedDict()
        product_image_data['product_image_guid'] = utils.convert_uuid_string(product_image.product_image_guid)
        product_image_data['image'] = settings.BASE_URL + product_image.image.url[4:]
        product_image_data['size'] = product_image.size
        product_image_data['is_default'] = True if product_image.is_default is True else False
        product_image_data['created_on'] = utils.format_timestamp(product_image.created_on)
        product_image_data['updated_on'] = utils.format_timestamp(
            product_image.updated_on) if product_image.updated_on is not None else None
        product_images_data.append(product_image_data)
    if not json:
        return product_images_data
    return utils.build_json(product_images_data)


def format_orders(order_items):
    orders_data = []
    for item in order_items:
        order_data = OrderedDict()
        order_data["order_guid"] = utils.convert_uuid_string(item.order_guid)
        order_data["id"] = item.order_id
        order_data["order_info"] = format_order_details(OrderDetails.objects.filter(order_id=item.order_id))
        order_data["final_cost"] = item.final_cost
        order_data["address_info"] = format_addresses(Addresses.objects.filter(address_id=item.address_id))
        order_data["created_on"] = utils.format_timestamp(item.created_on)
        order_data["updated_on"] = utils.format_timestamp(
            item.updated_on) if item.updated_on is not None else None
        orders_data.append(order_data)
    return orders_data


def format_order_details(order_details):
    order_items_data = []
    for item in order_details:
        order_item_data = OrderedDict()
        order_item_data["delivery_party_name"] = item.delivery_party_name
        order_item_data["suborder_id"] = item.order_detail_id
        order_item_data["delivery_tracking_number"] = item.delivery_tracking_number
        order_item_data["total_cost"] = item.total_cost
        order_item_data["product_info"] = format_products([item.product], False)
        order_item_data["status"] = item.status
        order_item_data["product_data"] = item.product_data
        order_item_data["created_on"] = utils.format_timestamp(item.created_on)
        order_item_data["updated_on"] = utils.format_timestamp(
            item.updated_on) if item.updated_on is not None else None
        order_items_data.append(order_item_data)
    return order_items_data


def format_discounts(discount_data):
    discounts_data = []
    for item in discount_data:
        discount_data = OrderedDict()
        discount_data["discount_guid"] = utils.convert_uuid_string(item.discount_guid)
        discount_data["description"] = item.description
        discount_data["discount_value"] = item.discount_value
        discount_data["start_time"] = utils.format_timestamp(item.start_time if item.start_time is not None else None)
        discount_data["end_time"] = utils.format_timestamp(item.start_time if item.start_time is not None else None)
        discount_data["product_quantity"] = item.product_quantity
        discount_data["is_percentage"] = item.is_percentage
        discount_data["created_on"] = utils.format_timestamp(item.created_on)
        discount_data["updated_on"] = utils.format_timestamp(
            item.updated_on) if item.updated_on is not None else None
        discounts_data.append(discount_data)
    return discounts_data


def format_reviews(review_data):
    reviews_data = []
    for item in review_data:
        review_data = OrderedDict()
        review_data["review_guid"] = utils.convert_uuid_string(item.review_guid)
        review_data["rating"] = item.rating
        review_data["review_detail"] = item.review_detail
        review_data["user_id"] = item.user_id
        review_data["business_id"] = item.business_id
        review_data["created_on"] = utils.format_timestamp(item.created_on)
        review_data["updated_on"] = utils.format_timestamp(
            item.updated_on) if item.updated_on is not None else None
        reviews_data.append(review_data)
    return reviews_data
