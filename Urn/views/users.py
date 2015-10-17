import json
from collections import OrderedDict
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from Urn.common import utils
from Urn.decorators.validators import validate_schema, jwt_validate
from Urn.models import Users, Status, User
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
            if users_api:
                is_business_user = request_data['is_business_user']
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
def get_all_users(request):
    if request.method in ['GET']:
        if request.user.is_superuser or request.user.is_staff:
            users = User.objects.all()
            return HttpResponse(format_get_users(users))
        else:
            return HttpResponse(status=401, content='You are not authorized to use this API.')
    elif request.method in ['POST']:
        if request.user.is_superuser or request.user.is_staff:
            return registration(request, True)
        else:
            return HttpResponse(status=401, content='You are not authorized to use this API.')
    else:
        return HttpResponseNotFound("Page Not Found")


def format_get_users(users):
    users_data = []
    for user_entry in users:
        user_data = OrderedDict()
        user_data['user_guid'] = utils.convert_uuid_string(user_entry.user_profile.user_guid)
        user_data['username'] = user_entry.username
        user_data['first_name'] = user_entry.first_name
        user_data['last_name'] = user_entry.last_name
        user_data['email'] = user_entry.email
        user_data['phone'] = user_entry.user_profile.phone
        user_data['status'] = user_entry.user_profile.status
        user_data['push_notification'] = user_entry.user_profile.push_notification
        user_data['email_notification'] = user_entry.user_profile.email_notification
        user_data['sms_notification'] = user_entry.user_profile.sms_notification
        user_data['is_business_user'] = user_entry.user_profile.is_business_user
        user_data['is_superuser'] = user_entry.is_superuser
        user_data['is_staff'] = user_entry.is_staff
        user_data['last_login'] = utils.format_timestamp(user_entry.last_login)
        user_data['created_on'] = utils.format_timestamp(user_entry.user_profile.created_on)
        user_data['updated_on'] = utils.format_timestamp(user_entry.user_profile.updated_on)
        users_data.append(user_data)
    return utils.build_json(users_data)
