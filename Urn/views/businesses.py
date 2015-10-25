import json

from django.http import HttpResponse, HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt
from Urn.common import utils, formatters
from Urn.decorators.validators import jwt_validate, validate_schema, check_authenticity, check_business_or_super
from Urn.models import Businesses, Addresses
from Urn.schema_validators.businesses_validator import schema


@csrf_exempt
def api_businesses(request):
    if request.method == 'GET':
        return api_businesses_get(request)
    elif request.method == 'POST':
        return api_businesses_post(request)
    else:
        return HttpResponseNotFound("API Not found")


@jwt_validate
@check_business_or_super
def api_businesses_get(request):
    url_params = request.GET
    if request.user.user_profile.is_business_user and len(url_params) == 0:
        return HttpResponse(status=401, content='You are not authorized to use this API.')
    business_guid = url_params['business_guid'] if 'business_guid' in url_params else None
    if business_guid:
        businesses = Businesses.objects.filter(business_guid=business_guid)
    else:
        businesses = Businesses.objects.all()
    return HttpResponse(utils.build_json(formatters.format_get_businesses(businesses, True, True)))


@jwt_validate
@check_authenticity
@validate_schema(schema)
def api_businesses_post(request):
    request_data = json.loads(request.body.decode())
    category = request_data['category'] if 'category' in request_data else None
    description = request_data['description'] if 'description' in request_data else None
    business = Businesses.objects.create(name=request_data['name'], category=category, description=description,
                                         created_by=request.user.user_profile)
    for address in request_data['addresses']:
        street1 = address['street1'] if 'street1' in address else None
        street2 = address['street2'] if 'street2' in address else None
        state = address['state'] if 'state' in address else None
        if 'is_default' in address:
            is_default = utils.request_boolean_field_value(address['is_default'])
        else:
            is_default = False
        Addresses.objects.create(city=address['city'], pincode=address['pincode'], country=address['country'],
                                 street_1=street1, street_2=street2, state=state, is_default=is_default,
                                 business=business)
    return HttpResponse(status=201, content='Business created')
