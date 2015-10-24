import json
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from Urn.common import utils, formatters
from Urn.decorators.validators import validate_schema, jwt_validate, check_authenticity
from Urn.models import Users, Status
from Urn.schema_validators.registration_validator import schema


@csrf_exempt
@validate_schema(schema)
def registration(request, users_api=False):
    if request.method in ['POST']:
        request_data = json.loads(request.body.decode())
        if User.objects.filter(email=request_data['email']).exists():
            request.session["Error"] = "EmailId already exists"
            return HttpResponseBadRequest("EmailId already exists")
        elif User.objects.filter(username=request_data['username']).exists():
            request.session["Error"] = "Username already exists"
            return HttpResponseBadRequest("Username already exists")
        else:
            user = User.objects.create_user(request_data['username'], request_data['email'],
                                            request_data['password'],
                                            first_name=request_data['first_name'],
                                            last_name=request_data['last_name'])
            is_business_user = False
            if users_api and 'is_business_user' in request_data:
                is_business_user = True if request_data['is_business_user'].lower() == 'true' else False

            Users.objects.create(
                user_id=user.id,
                phone=request_data['phone'],
                status=Status.active.value,
                is_business_user=is_business_user
            )
            return HttpResponse(status=201, content="User is Created")
    else:
        return HttpResponseNotFound("Page Not Found")


@csrf_exempt
@jwt_validate
@check_authenticity
def get_all_users(request):
    if request.method in ['GET']:
        users = User.objects.all()
        return HttpResponse(format_get_users(users))
    elif request.method in ['POST']:
        return registration(request, True)
    else:
        return HttpResponseNotFound("Page Not Found")


def format_get_users(users):
    users_data = []
    for user in users:
        users_data.append(formatters.format_user(user))
    return utils.build_json(users_data)


@csrf_exempt
@jwt_validate
def who_am_i(request):
    if request.method in ['GET']:
        user = request.user
        return HttpResponse(utils.build_json(formatters.format_user(user)))
    else:
        return HttpResponseNotFound('API Not Found')
