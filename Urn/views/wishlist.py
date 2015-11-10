import json
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from Urn.decorators.validators import jwt_validate, validate_schema
from Urn.models import Products, Wishlist, Users
from Urn.schema_validators.wishlist_validator import wishlist_post


@csrf_exempt
@jwt_validate
def process_wishlist_api(request):
    if request.method == 'GET':
        return process_wishlist_get(request)
    elif request.method == 'POST':
        return process_wishlist_post(request)
    elif request.method == 'PUT':
        return process_wishlist_put(request)
    else:
        return HttpResponseBadRequest("API not found")


# ToDo formatting the get call
def process_wishlist_get(request):
    if request.user.is_staff or request.user.is_superuser:
        user_guid = request.GET.get("user_guid", None)
        if user_guid is None:
            return HttpResponseBadRequest("Expected parameter user_guid")
        user_info = Users.objects.filter(user_guid=user_guid)
        if user_info.exists():
            users_wishlist = user_info.get().wishlist_set.all()
        else:
            return HttpResponseBadRequest("No such user exist")
    else:
        users_wishlist = request.user.user_profile.wishlist_set.all()


@validate_schema(wishlist_post)
def process_wishlist_post(request):
    request_data = json.loads(request.body.decode())
    product = Products.objects.filter(product_guid=request_data["product_guid"])
    if product.exists():
        product_info = product.get()
        Wishlist.objects.create(user_id=request.user.user_profile.user_id,
                                product_id=product_info.product_id,
                                product_data=json.dumps(request_data["product_data"]))
        return HttpResponse("Product added to wishlist")
    else:
        return HttpResponseBadRequest("No such product")


def process_wishlist_put(request):
    pass
