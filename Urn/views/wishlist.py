from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from Urn.decorators.validators import jwt_validate


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


def process_wishlist_get(request):
    pass


def process_wishlist_post(request):
    pass


def process_wishlist_put(request):
    pass
