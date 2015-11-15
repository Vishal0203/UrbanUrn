from collections import OrderedDict
import json
from datetime import datetime
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from Urn.common.formatters import format_discounts
from Urn.common.utils import build_json, convert_uuid_string
from Urn.decorators.validators import jwt_validate, check_business_or_super
from Urn.models import Products, Discounts


@csrf_exempt
@jwt_validate
@check_business_or_super
def process_discount_request(request):
    if request.method == 'POST':
        return process_discount_post(request)
    elif request.method == 'GET':
        return process_discount_get(request)
    elif request.method == 'PUT':
        return process_discount_put(request)
    else:
        return HttpResponseBadRequest("API not found")


def process_discount_post(request):
    request_data = json.loads(request.body.decode())
    product = Products.objects.filter(product_guid=request_data['product_guid'])
    if product.exists():
        discount = product.get().discounts_set.filter()
        if discount.exists():
            response = OrderedDict()
            response["product_guid"] = convert_uuid_string(discount.get().product.product_guid)
            response["discount_guid"] = convert_uuid_string(discount.get().discount_guid)
            response["product_quantity"] = discount.get().product_quantity
            response["discount_value"] = discount.get().discount_value
            response["is_percentage"] = discount.get().is_percentage
            return HttpResponse(status=409, content=build_json(response))

        discount = Discounts.objects.create(product_id=product.get().product_id,
                                            description=request_data["description"],
                                            start_time=datetime.strptime(request_data["start_time"],
                                                                         "%Y-%m-%d %H:%M:%S"),
                                            end_time=datetime.strptime(request_data["end_time"], "%Y-%m-%d %H:%M:%S"),
                                            discount_value=request_data["discount_value"],
                                            is_percentage=request_data["is_percentage"],
                                            active=request_data["active"],
                                            created_by=request.user.user_profile,
                                            product_quantity=request_data["product_quantity"])
        response = OrderedDict()
        response["discount_guid"] = convert_uuid_string(discount.discount_guid)
        return HttpResponse(build_json(response))
    else:
        return HttpResponseBadRequest("No such product exists")


def process_discount_get(request):
    params = request.GET
    if len(params) == 0:
        return HttpResponseBadRequest(content="Expected parameter 'product_guid'")
    elif 'product_guid' in params:
        product = Products.objects.filter(product_guid=params['product_guid'])
        discount = product.get().discounts_set.all()
        return HttpResponse(build_json(format_discounts(discount)))


def process_discount_put(request):
    request_data = json.loads(request.body.decode())
    discount = Discounts.objects.filter(discount_guid=request_data["discount_guid"])
    if discount.exists():
        request_data["updated_by"] = request.user.user_profile
        discount.update(**request_data)

        response = OrderedDict()
        response["discount_guid"] = convert_uuid_string(discount.get().discount_guid)
        return HttpResponse(status=202, content=build_json(response))
