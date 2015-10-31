from collections import OrderedDict
import json
from UrbanUrn import settings
from Urn.common import utils
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from Urn.common.utils import build_json, convert_uuid_string
from Urn.decorators.cookie_manager import manage_cookie
from Urn.decorators.validators import jwt_validate, validate_schema
from Urn.models import Sessions, Products, CartItems
from Urn.schema_validators.cart_validation import *
from Urn.views.products import format_products


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
        active_session = Sessions.objects.get(session_key=request.COOKIES.get(settings.ANONYMOUS_SESSION_NAME))
    except Sessions.DoesNotExist:
        active_session = Sessions.objects.create(session_key=request.COOKIES.get(settings.ANONYMOUS_SESSION_NAME))

    product = Products.objects.get(product_guid=request_data["product_guid"])
    cart_item = CartItems.objects.create(product_id=product.product_id, session_id=active_session.session_id,
                                         product_data=request_data["product_data"])
    response = OrderedDict()
    response["cart_item_guid"] = convert_uuid_string(cart_item.cart_item_guid)

    return HttpResponse(build_json(response))


@validate_schema(put_schema)
def process_carts_put(request):
    if request.user.is_authenticated() or request.user.is_superuser or request.user.is_staff:
        return process_put_if_authenticated(request)
    else:
        return process_put_if_not_authenticated(request)


@jwt_validate
def process_put_if_authenticated(request):
    request_data = json.loads(request.body.decode())
    cart_item = CartItems.objects.filter(cart_item_guid=request_data["cart_item_guid"])
    if cart_item.exists() or cart_item.get().user_id == request.user.user_profile.user_id:
        cart_item.update(**request_data)
        return HttpResponse(status=202, content='cart product updated')
    else:
        return HttpResponse(status=401, content='You are not authorized to edit this cart item')


def process_put_if_not_authenticated(request):
    request_data = json.loads(request.body.decode())
    cart_item = CartItems.objects.filter(cart_item_guid=request_data["cart_item_guid"])
    if cart_item.exists() or cart_item.get().session.session_key == request.COOKIES.get(
            settings.ANONYMOUS_SESSION_NAME):
        cart_item.update(**request_data)
        return HttpResponse(status=202, content='cart product updated')
    else:
        return HttpResponse(status=401, content='You are not authorized to edit this cart item')


@manage_cookie
def process_carts_get(request):
    if request.user.is_authenticated():
        user = request.user.user_profile.id
        cart_items = CartItems.objects.filter(user_id=user)
    else:
        # TODO
        session = request.COOKIES
        cart_items = CartItems.objects.filter(session_id=session)

    return HttpResponse(build_json(format_carts(cart_items)))


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


@validate_schema(delete_schema)
def process_carts_delete(request):
    if request.user.is_authenticated() or request.user.is_superuser or request.user.is_staff:
        return process_delete_if_authenticated(request)
    else:
        return process_delete_if_not_authenticated(request)


@jwt_validate
def process_delete_if_authenticated(request):
    request_data = json.loads(request.body.decode())
    cart_item = CartItems.objects.filter(cart_item_guid=request_data["cart_item_guid"])
    if cart_item.exists() or cart_item.get().user_id == request.user.user_profile.user_id:
        cart_item.delete()
        return HttpResponse(status=202, content='cart product deleted')
    else:
        return HttpResponse(status=401, content='You are not authorized to delete this cart item')


def process_delete_if_not_authenticated(request):
    request_data = json.loads(request.body.decode())
    cart_item = CartItems.objects.filter(cart_item_guid=request_data["cart_item_guid"])
    if cart_item.exists() or cart_item.get().session.session_key == request.COOKIES.get(
            settings.ANONYMOUS_SESSION_NAME):
        cart_item.delete()
        return HttpResponse(status=202, content='cart product deleted')
    else:
        return HttpResponse(status=401, content='You are not authorized to delete this cart item')

