from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from Urn.decorators.validators import jwt_validate, validate_schema
from Urn.schema_validators.cart_validation import *


@csrf_exempt
def process_carts_request(request):
    if request.method == 'POST':
        process_carts_post(request)
    elif request.method == 'PUT':
        process_carts_put(request)
    elif request.method == 'GET':
        process_carts_get(request)
    else:
        process_carts_delete(request)


def process_carts_post(request):
    if request.user.is_authenticated() or request.user.is_superuser or request.user.is_staff:
        process_post_if_authenticated(request)
    else:
        process_post_if_not_authenticated(request)


@jwt_validate
@validate_schema(post_auth_schema)
def process_post_if_authenticated(request):
    pass


@validate_schema(post_non_auth_schema)
def process_post_if_not_authenticated(request):
    pass


def process_carts_put(request):
    if request.user.is_authenticated() or request.user.is_superuser or request.user.is_staff:
        process_put_if_authenticated(request)
    else:
        process_put_if_not_authenticated(request)


@jwt_validate
@validate_schema(put_auth_schema)
def process_put_if_authenticated(request):
    pass


@validate_schema(put_non_auth_schema)
def process_put_if_not_authenticated(request):
    pass


def process_carts_get(request):
    pass


def process_carts_delete(request):
    if request.user.is_authenticated() or request.user.is_superuser or request.user.is_staff:
        process_delete_if_authenticated(request)
    else:
        process_delete_if_not_authenticated(request)


@jwt_validate
@validate_schema(delete_auth_schema)
def process_delete_if_authenticated(request):
    pass


@validate_schema(delete_non_auth_schema)
def process_delete_if_not_authenticated(request):
    pass
