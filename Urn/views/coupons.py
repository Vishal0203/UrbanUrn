from collections import OrderedDict
import json
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from Urn.common.utils import build_json, convert_uuid_string
from Urn.decorators.validators import jwt_validate, validate_schema
from Urn.models import Coupons
from Urn.schema_validators.coupons_validator import superuser_schema, general_schema


@csrf_exempt
@jwt_validate
def process_coupons_request(request):
    if request.method == 'POST':
        return process_coupons_post(request)
    else:
        return HttpResponseBadRequest("API not found")


def process_coupons_post(request):
    if request.user.is_superuser or request.user.is_staff:
        return process_superuser_coupon_request(request)
    else:
        return process_general_coupon_request(request)


@validate_schema(superuser_schema)
def process_superuser_coupon_request(request):
    request_data = json.loads(request.body.decode())
    response = OrderedDict()
    response["success"] = response["error"] = list()
    for coupon in request_data["coupons"]:
        each_coupon = Coupons.objects.filter(code=coupon["code"], discount_value=coupon["discount_value"],
                                             is_percentage=coupon["is_percentage"])
        if not each_coupon.exists():
            added_coupon = Coupons.objects.create(code=coupon["code"], discount_value=coupon["discount_value"],
                                                  is_percentage=coupon["is_percentage"])
            response["success"].append(added_coupon.code)
        else:
            response["error"].append(coupon["code"])

    return HttpResponse(build_json(response))


@validate_schema(general_schema)
def process_general_coupon_request(request):
    request_data = json.loads(request.body.decode())
    response = OrderedDict()
    coupon = Coupons.objects.filter(code=request_data["code"])
    if coupon.exists():
        response["coupon_guid"] = convert_uuid_string(coupon.get().coupon_guid)
        response["discount_value"] = coupon.get().discount_value
        response["is_percentage"] = coupon.get().is_percentage
    else:
        return HttpResponseBadRequest("No such coupon code exists")

    return HttpResponse(build_json(response))
