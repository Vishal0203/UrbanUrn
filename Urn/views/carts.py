from collections import OrderedDict
import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from Urn.common.utils import build_json, convert_uuid_string
from Urn.decorators.cookie_manager import manage_cookie
from Urn.decorators.validators import jwt_validate, validate_schema
from Urn.models import Sessions, Products, CartItems
from Urn.schema_validators.cart_validation import *


@csrf_exempt
def process_carts_request(request):
    if request.method == 'POST':
        return process_carts_post(request)
    elif request.method == 'PUT':
        return process_carts_put(request)
    elif request.method == 'GET':
        return process_carts_get(request)
    else:
        return process_carts_delete(request)


@validate_schema(post_schema)
def process_carts_post(request):
    if request.user.is_authenticated() or request.user.is_superuser or request.user.is_staff:
        return process_post_if_authenticated(request)
    else:
        return process_post_if_not_authenticated(request)


@jwt_validate
def process_post_if_authenticated(request):
    request_data = json.loads(request.body.decode())

    product = Products.objects.get(product_guid=request_data["product_guid"])
    cart_item = CartItems.objects.create(product_id=product.product_id, user_id=request.user.user_profile.user_id,
                                         product_data=request_data["product_data"])
    response = OrderedDict()
    response["cart_item_guid"] = convert_uuid_string(cart_item.cart_item_guid)

    return HttpResponse(build_json(response))


@manage_cookie
def process_post_if_not_authenticated(request):
    request_data = json.loads(request.body.decode())

    try:
        active_session = Sessions.objects.get(session_key=request.COOKIES.get('urbanurn_anonymous_cookie'))
    except Sessions.DoesNotExist:
        active_session = Sessions.objects.create(session_key=request.COOKIES.get('urbanurn_anonymous_cookie'))

    product = Products.objects.get(product_guid=request_data["product_guid"])
    cart_item = CartItems.objects.create(product_id=product.product_id, session_id=active_session.session_id,
                                         product_data=request_data["product_data"])
    response = OrderedDict()
    response["cart_item_guid"] = convert_uuid_string(cart_item.cart_item_guid)

    return HttpResponse(build_json(response))


@validate_schema(put_schema)
def process_carts_put(request):
    if request.user.is_authenticated() or request.user.is_superuser or request.user.is_staff:
        process_put_if_authenticated(request)
    else:
        process_put_if_not_authenticated(request)


@jwt_validate
def process_put_if_authenticated(request):
    pass


def process_put_if_not_authenticated(request):
    pass


def process_carts_get(request):
    pass


@validate_schema(delete_schema)
def process_carts_delete(request):
    if request.user.is_authenticated() or request.user.is_superuser or request.user.is_staff:
        process_delete_if_authenticated(request)
    else:
        process_delete_if_not_authenticated(request)


@jwt_validate
def process_delete_if_authenticated(request):
    pass


def process_delete_if_not_authenticated(request):
    pass
