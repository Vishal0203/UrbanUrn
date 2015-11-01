from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from Urn.decorators.validators import jwt_validate


@jwt_validate
@csrf_exempt
def process_orders_request(request):
    if request.method == 'GET':
        return process_orders_get(request)
    elif request.method == 'POST':
        return process_orders_post(request)
    elif request.method == 'PUT':
        return process_orders_put(request)


def process_orders_get(request):
    pass


def process_orders_post(request):
    pass


def process_orders_put(request):
    pass

