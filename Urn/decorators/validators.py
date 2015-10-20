import json
from django.http import HttpResponseServerError, HttpResponseForbidden, HttpResponseBadRequest, HttpResponse
from jwt import decode, InvalidTokenError, InvalidIssuerError, InvalidIssuedAtError
from django.conf import settings
from setuptools.compat import basestring
from Urn.models import Sessions
import jsonschema


def jwt_validate(original_function):
    def validator(request_argument):
        authorization_head = request_argument.META.get('HTTP_X_URBANURN_AUTH', None)
        if request_argument.user.is_authenticated() and authorization_head is not None:
            status = validate_jwt_values(authorization_head, request_argument.user)
            if status is 'OK':
                return original_function(request_argument)
            else:
                return HttpResponseForbidden('Invalid token')
        else:
            return HttpResponseBadRequest("Header 'X-Urbanurn-Auth' expected")

    return validator


def check_authenticity(original_function):
    def authenticity_checker(request_arg):
        if request_arg.user.is_superuser or request_arg.user.is_staff:
            return original_function(request_arg)
        else:
            return HttpResponse(status=401, content="You are not authorized to use this API")

    return authenticity_checker


def check_business_or_super(original_function):
    def authenticity_checker(request_arg):
        if request_arg.user.user_profile.is_business_user or request_arg.user.is_superuser or request_arg.user.is_staff:
            return original_function(request_arg)
        else:
            return HttpResponse(status=401, content="You are not authorized to use this API")

    return authenticity_checker


def validate_jwt_values(encoded_token, logged_in_user):
    try:
        decoded_payload = decode(encoded_token, settings.JWT_SECRET_KEY, algorithms=['HS256'])
        guid_check = basestring(logged_in_user.user_profile.user_guid) == decoded_payload.get('user_guid')
        session_check = Sessions.objects.get(session_key=decoded_payload.get('session_key'))
        if guid_check and session_check is not None:
            return 'OK'
        else:
            return 'INVALID'
    except (InvalidIssuerError, InvalidIssuedAtError, InvalidTokenError, Sessions.DoesNotExist) as e:
        return 'INVALID'


def validate_schema(schema):
    def wrap_schema_validator(func):
        def actual_schema_validator(request, *args):
            try:
                jsonschema.validate(json.loads(request.body.decode()), schema)
                return func(request, *args)
            except Exception as e:
                request.session["Error"] = e
                return HttpResponseServerError(e)

        return actual_schema_validator

    return wrap_schema_validator
