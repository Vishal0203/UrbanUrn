from django.views.decorators.csrf import csrf_exempt
from Urn.decorators.validators import jwt_validate, check_authenticity, validate_schema
from django.http import HttpResponse


@csrf_exempt
@jwt_validate
@check_authenticity
def process_sku_request(request):
    if request.method in ['POST', 'PUT']:
        return process_sku_post(request)
    else:
        return process_sku_get(request)


@validate_schema
def process_sku_post(request):
    pass


def process_sku_get(request):
    pass
