from collections import OrderedDict
import json
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from Urn.common import utils
from Urn.common.formatters import format_orders
from Urn.common.utils import build_json
from Urn.decorators.validators import jwt_validate
from Urn.models import Orders, Users, CartItems, OrderDetails


@csrf_exempt
@jwt_validate
def process_orders_request(request):
    if request.method == 'GET':
        return process_orders_get(request)
    elif request.method == 'POST':
        return process_orders_post(request)
    elif request.method == 'PUT':
        return process_orders_put(request)


def process_orders_get(request):
    if request.user.is_superuser or request.user.is_staff:
        return orders_superuser_options(request)
    else:
        user_guid = request.user.user_profile.user_guid
        user_info = Users.objects.get(user_guid=user_guid)
        order_info = Orders.objects.filter(user_id=user_info.user_id)
        return HttpResponse(utils.build_json(format_orders(order_info)))


def orders_superuser_options(request):
    user_guid = request.GET.get('user_guid', None)
    if user_guid is None:
        all_orders = Orders.objects.all()
        return HttpResponse(utils.build_json(all_orders))
    else:
        user_info = Users.objects.get(user_guid=user_guid)
        order_info = Orders.objects.get(user_id=user_info.user_id)
        return HttpResponse(utils.build_json(order_info))


def process_orders_post(request):
    request_data = json.loads(request.body.decode())
    user_info = request.user
    checked_out_products = request_data["products"]

    order = Orders.objects.create(user_id=user_info.user_profile.user_id,
                                  address_id=user_info.user_profile.addresses_set.get(
                                      address_guid=request_data["address_guid"]).address_id,
                                  final_cost=request_data["final_cost"],
                                  created_by=user_info.user_profile)
    for each_product in checked_out_products:
        item_in_cart = CartItems.objects.filter(cart_item_guid=each_product["cart_item_guid"],
                                                user_id=user_info.user_profile)
        if item_in_cart.exists():
            discount_id = None
            discount = item_in_cart.get().product.discounts_set.filter(
                product_id=item_in_cart.get().product_id)
            if discount.exists():
                discount_id = discount.get().discount_id
            order_detail = OrderDetails.objects.create(order_id=order.order_id,
                                                       product_id=item_in_cart.get().product_id,
                                                       discount_id=discount_id,
                                                       total_cost=each_product["total_cost"],
                                                       product_data=item_in_cart.get().product_data)
        else:
            return HttpResponse(status=401, content="You are not authorized to view this cart")
        item_in_cart.delete()

    response = format_orders(Orders.objects.filter(user_id=user_info.id).filter(order_id=order.order_id))
    return HttpResponse(build_json(response))


def process_orders_put(request):
    pass
