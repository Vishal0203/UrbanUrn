import json
from collections import OrderedDict
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from Urn.common import utils, formatters
from Urn.decorators.validators import validate_schema, jwt_validate
from Urn.models import Users, Status, Addresses
from Urn.schema_validators.registration_validator import schema
from Urn.views import addresses


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
    for user in users:
        user_data = OrderedDict()
        user_data['user_guid'] = utils.convert_uuid_string(user.user_profile.user_guid)
        user_data['username'] = user.username
        user_data['first_name'] = user.first_name
        user_data['last_name'] = user.last_name
        user_data['email'] = user.email
        user_data['phone'] = user.user_profile.phone
        user_data['status'] = user.user_profile.status

        user_addresses = Addresses.objects.filter(user_id=user.user_profile.user_id)
        user_data['addresses'] = addresses.format_addresses(user_addresses)

        if user.user_profile.is_business_user:
            user_businesses = user.user_profile.businesses_set.all()
            user_data['businesses'] = formatters.format_get_businesses(user_businesses)

        user_data['push_notification'] = user.user_profile.push_notification
        user_data['email_notification'] = user.user_profile.email_notification
        user_data['sms_notification'] = user.user_profile.sms_notification
        user_data['is_business_user'] = user.user_profile.is_business_user
        user_data['is_superuser'] = user.is_superuser
        user_data['is_staff'] = user.is_staff
        user_data['last_login'] = utils.format_timestamp(user.last_login) if user.last_login is not None else None
        user_data['created_on'] = utils.format_timestamp(user.user_profile.created_on)
        user_data['updated_on'] = utils.format_timestamp(
            user.user_profile.updated_on) if user.user_profile.updated_on is not None else None
        users_data.append(user_data)
    return utils.build_json(users_data)


def format_get_business_users(business_users):
    business_users_data = []
    for business_user in business_users:
        business_user_data = OrderedDict()
        business_user_data['user_guid'] = utils.convert_uuid_string(business_user.user_guid)
        business_user_data['username'] = business_user.user.username
        business_user_data['first_name'] = business_user.user.first_name
        business_user_data['last_name'] = business_user.user.last_name
        business_user_data['email'] = business_user.user.email
        business_user_data['phone'] = business_user.phone
        business_user_data['status'] = business_user.status
        business_user_data['created_on'] = utils.format_timestamp(business_user.created_on)
        business_user_data['updated_on'] = utils.format_timestamp(
            business_user.updated_on) if business_user.updated_on is not None else None
        business_users_data.append(business_user_data)
    return business_users_data
