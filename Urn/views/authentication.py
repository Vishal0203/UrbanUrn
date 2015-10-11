import datetime
from django.contrib.auth.decorators import login_required
import jwt
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseNotAllowed, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from setuptools.compat import basestring
from Urn.decorators.validators import jwt_validate
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
                try:
                    Sessions.objects.get(session_key=active_session)
                except Sessions.DoesNotExist:
                    user_session = Sessions(user_id=auth_user.user_profile.user_id, session_key=active_session)
                    user_session.save()

                return HttpResponse(encoded_token)
            else:
                return HttpResponseNotAllowed('This user has a disabled account')
        else:
            return HttpResponseForbidden('Invalid username or password')


@jwt_validate
def logout_and_clear_session(request):
    if request.method == 'GET':
        Sessions.objects.filter(session_key=request.session.session_key).delete()
        logout(request)
        return HttpResponse("Logged Out")