import datetime
import jwt
from Urn.common.utils import build_json
from django.contrib.auth import authenticate, login, logout
from Urn.decorators.validators import validate_schema
from Urn.schema_validators.registration_validator import login_schema
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseNotAllowed, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from setuptools.compat import basestring
from Urn.common import utils
from Urn.decorators.cookie_manager import manage_cookie
from Urn.decorators.validators import jwt_validate
from Urn.models import Sessions
import json


@csrf_exempt
@manage_cookie
@validate_schema(login_schema)
def validate_input_and_authenticate(request):
    if request.method == 'GET':
        return HttpResponseNotFound("Page not found")
    else:
        request_data = json.loads(request.body.decode())
        username = request_data['username']
        password = request_data['password']
        auth_user = authenticate(username=username, password=password)
        if auth_user is not None:
            if auth_user.is_active:
                request.session.set_expiry(1800)
                login(request, auth_user)
                active_session = request.session.session_key
                issued_at = datetime.datetime.utcnow()
                jwt_payload = {
                    'iss': settings.JWT_ISSUER,
                    'iat': issued_at,
                    'exp': issued_at + datetime.timedelta(hours=2),
                    'username': auth_user.username,
                    'session_key': active_session,
                    'user_guid': basestring(auth_user.user_profile.user_guid)
                }
                encoded_token = jwt.encode(jwt_payload, settings.JWT_SECRET_KEY, algorithm='HS256')
                if not Sessions.objects.filter(session_key=active_session).exists():
                    user_session = Sessions(user_id=auth_user.user_profile.user_id, session_key=active_session)
                    user_session.save()

                return HttpResponse(build_json(keys=['username', 'user_guid', 'token'],
                                               values=[auth_user.username,
                                                       utils.convert_uuid_string(auth_user.user_profile.user_guid),
                                                       encoded_token.decode('utf-8')]))
            else:
                return HttpResponseNotAllowed('This user has a disabled account')
        else:
            return HttpResponseForbidden('Invalid username or password')


def post_reg_login(request, request_data):
    auth_user = authenticate(username=request_data['username'], password=request_data['password'])
    request.session.set_expiry(1800)
    login(request, auth_user)
    active_session = request.session.session_key
    issued_at = datetime.datetime.utcnow()
    jwt_payload = {
        'iss': settings.JWT_ISSUER,
        'iat': issued_at,
        'exp': issued_at + datetime.timedelta(hours=2),
        'username': auth_user.username,
        'session_key': active_session,
        'user_guid': basestring(auth_user.user_profile.user_guid)
    }
    encoded_token = jwt.encode(jwt_payload, settings.JWT_SECRET_KEY, algorithm='HS256')
    if not Sessions.objects.filter(session_key=active_session).exists():
        user_session = Sessions(user_id=auth_user.user_profile.user_id, session_key=active_session)
        user_session.save()

    return HttpResponse(build_json(keys=['username', 'user_guid', 'token'],
                                   values=[auth_user.username,
                                           utils.convert_uuid_string(auth_user.user_profile.user_guid),
                                           encoded_token.decode('utf-8')]))


@jwt_validate
def logout_and_clear_session(request):
    if request.method == 'GET':
        Sessions.objects.filter(session_key=request.session.session_key).delete()
        logout(request)
        return HttpResponse(build_json(keys=["success"], values=["Logged Out"]))


@jwt_validate
def refresh_jwt_token(request):
    if request.method == 'GET' and request.user.is_authenticated():
        issued_at = datetime.datetime.utcnow()
        auth_user = request.user
        jwt_payload = {
            'iss': settings.JWT_ISSUER,
            'iat': issued_at,
            'exp': issued_at + datetime.timedelta(hours=2),
            'username': auth_user.username,
            'session_key': request.session.session_key,
            'user_guid': basestring(auth_user.user_profile.user_guid)
        }
        encoded_token = jwt.encode(jwt_payload, settings.JWT_SECRET_KEY, algorithm='HS256')
        if not Sessions.objects.filter(session_key=request.session.session_key).exists():
            user_session = Sessions(user_id=auth_user.user_profile.user_id, session_key=request.session.session_key)
            user_session.save()

        return HttpResponse(build_json(keys=['token'], values=[encoded_token.decode('utf-8')]))
