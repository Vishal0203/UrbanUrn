from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from Urn.decorators.validators import jwt_validate
from Urn.models import Orders, Users


@jwt_validate
@csrf_exempt
def process_orders_request(request):
    if request.method == 'GET':
        return process_orders_get(request)
    elif request.method == 'POST':
        return process_orders_post(request)
    elif request.method == 'PUT':
        return process_orders_put(request)


def process_orders_get(request):
    if request.user.is_superuser or request.user.is_staff:
        return orders_superuser_options(request)
    else:
        # ToDo write a formatter to return a proper json result
        user_guid = request.user.user_profile.user_guid
        user_info = Users.objects.get(user_guid=user_guid)
        order_info = Orders.objects.get(user_id=user_info.user_id)


def orders_superuser_options(request):
    user_guid = request.GET.get('user_guid', None)
    if user_guid is None:
        all_orders = Orders.objects.all()
    else:
        # ToDo write a formatter to return a proper json result
        user_info = Users.objects.get(user_guid=user_guid)
        order_info = Orders.objects.get(user_id=user_info.user_id)


def process_orders_post(request):
    pass


def process_orders_put(request):
    pass
