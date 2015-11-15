import json
from datetime import datetime
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from Urn.decorators.validators import jwt_validate, check_business_or_super
from Urn.models import Products, Discounts


@csrf_exempt
def process_discount_request(request):
    if request.method == 'POST':
        return process_discount_post(request)
    elif request.method == 'GET':
        return process_discount_get(request)
    elif request.method == 'PUT':
        return process_discount_put(request)
    else:
        return HttpResponseBadRequest("API not found")


@jwt_validate
@check_business_or_super
def process_discount_post(request):
    request_data = json.loads(request.body.decode())
    product = Products.objects.filter(product_guid=request['product_guid'])
    if product.exists():
        discount = Discounts.objects.create(product_id=product.get().product_id,
                                            description=request_data["description"],
                                            start_time=datetime.strptime(request_data["start_time"],
                                                                         "%Y-%m-%d %H:%M:%S"),
                                            end_time=datetime.strptime(request_data["end_time"], "%Y-%m-%d %H:%M:%S"),
                                            discount_value=request_data["discount_value"],
                                            is_percentage=request_data["is_percentage"],
                                            product_quantity=request_data["product_quantity"])


def process_discount_get(request):
    pass


@jwt_validate
@check_business_or_super
def process_discount_put(request):
    pass
