from collections import OrderedDict
import json
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from Urn.common.formatters import format_wishlist_get
from Urn.common.utils import build_json
from Urn.decorators.validators import jwt_validate, validate_schema
from Urn.models import Products, Wishlist, Users
from Urn.schema_validators.wishlist_validator import wishlist_delete, wishlist_post


@csrf_exempt
@jwt_validate
def process_wishlist_request(request):
    if request.method == 'GET':
        return process_wishlist_get(request)
    elif request.method == 'POST':
        return process_wishlist_post(request)
    elif request.method == 'DELETE':
        return process_wishlist_delete(request)
    else:
        return HttpResponseBadRequest("API not found")


def process_wishlist_get(request):
    if request.user.is_staff or request.user.is_superuser:
        user_guid = request.GET.get("user_guid", None)
        if user_guid is None:
            return HttpResponseBadRequest("Expected parameter user_guid")
        user_info = Users.objects.filter(user_guid=user_guid)
        if user_info.exists():
            users_wishlist = user_info.get().wishlist_set.all()
            response = format_wishlist_get(users_wishlist)
        else:
            return HttpResponseBadRequest("No such user exist")
    else:
        users_wishlist = request.user.user_profile.wishlist_set.all()
        response = format_wishlist_get(users_wishlist)

    return HttpResponse(build_json(response))


@validate_schema(wishlist_post)
def process_wishlist_post(request):
    request_data = json.loads(request.body.decode())
    product = Products.objects.filter(product_guid=request_data["product_guid"])
    if product.exists():
        product_info = product.get()
        Wishlist.objects.create(user_id=request.user.user_profile.user_id,
                                product_id=product_info.product_id,
                                product_data=request_data["product_data"])
        return HttpResponse("Product added to wishlist")
    else:
        return HttpResponseBadRequest("No such product")


@validate_schema(wishlist_delete)
def process_wishlist_delete(request):
    request_data = json.loads(request.body.decode())
    wish = Wishlist.objects.filter(wishlist_guid=request_data["wishlist_guid"],
                                   user_id=request.user.user_profile.user_id)
    if wish.exists():
        wish.delete()
        return HttpResponse("Product removed from wish list")
    else:
        return HttpResponseBadRequest("Product not present in wish list")
