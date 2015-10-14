import json
from django.http import HttpResponseRedirect, HttpResponseServerError
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
                return HttpResponseRedirect('login_page')
        else:
            return HttpResponseRedirect('login_page')

    return validator


def validate_jwt_values(encoded_token, loggedin_user):
    try:
        decoded_payload = decode(encoded_token, settings.JWT_SECRET_KEY, algorithms=['HS256'])
        guid_check = basestring(loggedin_user.user_profile.user_guid) == decoded_payload.get('user_guid')
        session_check = Sessions.objects.get(session_key=decoded_payload.get('session_key'))
        if guid_check and session_check is not None:
            return 'OK'
        else:
            return 'INVALID'
    except (InvalidIssuerError, InvalidIssuedAtError, InvalidTokenError, Sessions.DoesNotExist) as e:
        return 'INVALID'


def validate_schema(schema):
    def wrap_schema_validator(func):
        def actual_schema_validator(request):
            try:
                jsonschema.validate(json.loads(request.body.decode()), schema)
                return func(request)
            except Exception as e:
                request.session["Error"] = e
                return HttpResponseServerError(e)
        return actual_schema_validator
    return wrap_schema_validator
