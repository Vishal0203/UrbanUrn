from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from Urn.decorators.validators import jwt_validate


@csrf_exempt
def process_reviews_request(request):
    if request.method == 'GET':
        return process_get_request(request)
    elif request.method == 'POST':
        return process_post_request(request)
    elif request.method == 'PUT':
        return process_put_request(request)
    elif request.method == 'DELETE':
        return process_delete_request(request)
    else:
        return HttpResponseBadRequest("API not found")


def process_get_request(request):
    pass


@jwt_validate
def process_post_request(request):
    pass


@jwt_validate
def process_put_request(request):
    pass


@jwt_validate
def process_delete_request(request):
    pass
