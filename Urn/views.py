import datetime
import jwt
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseNotAllowed, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from setuptools.compat import basestring
from Urn.models import Sessions


@csrf_exempt
def validate_input_and_authenticate(request):
    if request.method == 'GET':
        return HttpResponseNotFound("Page not found")
    else:
        username = request.POST['username']
        password = request.POST['password']
        auth_user = authenticate(username=username, password=password)
        if auth_user is not None:
            if auth_user.is_active:
                login(request, auth_user)
                jwt_payload = {
                    'iss': settings.JWT_ISSUER,
                    'iat': datetime.datetime.now(),
                    'exp': datetime.datetime.now() + datetime.timedelta(hours=2),
                    'session_key': request.session.session_key,
                    'user_guid': basestring(auth_user.user_profile.user_guid)
                }
                encoded_token = jwt.encode(jwt_payload, settings.JWT_SECRET_KEY, algorithm='HS256')
                user_session = Sessions(user_id=auth_user.user_profile.user_id, session_key=request.session.session_key)
                user_session.save()

                return HttpResponse(encoded_token)
            else:
                return HttpResponseNotAllowed('This user has a disabled account')
        else:
            return HttpResponseForbidden('Invalid username or password')
