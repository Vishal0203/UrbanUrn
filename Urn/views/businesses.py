import json

from django.http import HttpResponse, HttpResponseNotFound, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from Urn.common import utils, formatters
from Urn.decorators.validators import jwt_validate, validate_schema
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
def api_businesses_get(request):
    if request.user.is_superuser or request.user.is_staff or request.user.user_profile.is_business_user:
        url_params = request.GET
        if request.user.user_profile.is_business_user and len(url_params) == 0:
            return HttpResponse(status=401, content='You are not authorized to use this API.')
        business_guid = url_params['business_guid'] if 'business_guid' in url_params else None
        if business_guid:
            businesses = Businesses.objects.filter(business_guid=business_guid)
        else:
            businesses = Businesses.objects.all()
        return HttpResponse(utils.build_json(formatters.format_get_businesses(businesses, True, True)))
    else:
        return HttpResponse(status=401, content='You are not authorized to use this API.')


@jwt_validate
@validate_schema(schema)
def api_businesses_post(request):
    if request.user.is_superuser or request.user.is_staff:
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
                if address['is_default'].lower() == 'true':
                    is_default = True
                else:
                    is_default = False
            else:
                is_default = False
            Addresses.objects.create(city=address['city'], pincode=address['pincode'], country=address['country'],
                                     street_1=street1, street_2=street2, state=state, is_default=is_default,
                                     business=business)
        return HttpResponse(status=201, content='Business created')
    else:
        return HttpResponse(status=401, content='You are not authorized to use this API.')
