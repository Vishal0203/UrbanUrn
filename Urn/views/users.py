import json
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from Urn.common import utils, formatters
from Urn.decorators.validators import validate_schema, jwt_validate, check_authenticity, \
    check_email_exists, check_username_exists
from Urn.models import Users, Status
from Urn.schema_validators.registration_validator import schema, update_schema


@csrf_exempt
@validate_schema(schema)
def registration(request, users_api=False):
    if request.method in ['POST']:
        request_data = json.loads(request.body.decode())
        if check_email_exists(request, request_data['email']):
            return HttpResponseBadRequest("EmailId already exists")
        if check_username_exists(request, request_data['username']):
            return HttpResponseBadRequest("Username already exists")

        user = User.objects.create_user(request_data['username'], request_data['email'],
                                        request_data['password'],
                                        first_name=request_data['first_name'],
                                        last_name=request_data['last_name'])
        is_business_user = False
        if users_api and 'is_business_user' in request_data:
            is_business_user = utils.request_boolean_field_value(request_data['is_business_user'])

        push_notification = utils.request_boolean_field_value(
            request_data['push_notification']) if 'push_notification' in request_data else False
        email_notification = utils.request_boolean_field_value(
            request_data['email_notification']) if 'email_notification' in request_data else False
        sms_notification = utils.request_boolean_field_value(
            request_data['sms_notification']) if 'sms_notification' in request_data else False
        Users.objects.create(
            user_id=user.id,
            phone=request_data['phone'],
            status=Status.active.value,
            push_notification=push_notification,
            email_notification=email_notification,
            sms_notification=sms_notification,
            is_business_user=is_business_user
        )
        return HttpResponse(status=201, content="User is Created")
    else:
        return HttpResponseNotFound("Page Not Found")


@csrf_exempt
@jwt_validate
def api_users(request):
    if request.method == 'GET':
        return api_users_get(request)
    elif request.method == 'POST':
        return api_users_post(request)
    elif request.method == 'PUT':
        return api_users_put(request)
    else:
        return HttpResponseNotFound('API Not found')


@check_authenticity
def api_users_get(request):
    users = User.objects.all()
    return HttpResponse(format_get_users(users))


@check_authenticity
def api_users_post(request):
    return registration(request, True)


@validate_schema(update_schema)
def api_users_put(request):
        url_params = request.GET
        if (request.user.is_superuser or request.user.is_staff) and len(url_params) == 0:
            return HttpResponseBadRequest(content='Please provide the user_guid of the user to update')
        user_guid = url_params['user_guid'] if 'user_guid' in url_params else None
        return update_user(request, user_guid)


def update_user(request, user_guid):
    if user_guid:
        try:
            user_entry = Users.objects.get(user_guid=user_guid)
            user_id = user_entry.user_id
        except Users.DoesNotExist as e:
            return HttpResponseBadRequest("No such user exists")
    else:
        user_id = request.user.user_profile.user_id
    user_entry = Users.objects.get(user_id=user_id)
    request_data = json.loads(request.body.decode())
    if 'email' in request_data and request_data['email'] != user_entry.user.email:
        if check_email_exists(request, request_data['email']):
            return HttpResponseBadRequest("EmailId already exists")
    if 'username' in request_data and request_data['username'] != user_entry.user.username:
        if check_username_exists(request, request_data['username']):
            return HttpResponseBadRequest("Username already exists")

    auth_user_keys = ['username', 'first_name', 'last_name', 'email']
    user_keys = ['phone', 'status']
    user_boolean_keys = ['push_notification', 'email_notification', 'sms_notification']
    for key in request_data:
        if key in auth_user_keys:
            setattr(user_entry.user, key, request_data[key])
        elif key in user_keys:
            setattr(user_entry, key, request_data[key])
        elif key in user_boolean_keys:
            setattr(user_entry, key, utils.request_boolean_field_value(request_data[key]))
    user_entry.user.save()
    user_entry.save()
    return HttpResponse(status=202, content='User successfully updated')


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
