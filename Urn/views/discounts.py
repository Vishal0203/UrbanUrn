from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from Urn.decorators.validators import jwt_validate, check_business_or_super


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
    pass


def process_discount_get(request):
    pass


@jwt_validate
@check_business_or_super
def process_discount_put(request):
    pass
