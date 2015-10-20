import json

from collections import OrderedDict
from django.http import HttpResponse, HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt
from Urn.common import utils
from Urn.decorators.validators import jwt_validate, validate_schema
from Urn.models import Businesses, Addresses
from Urn.schema_validators.businesses_validator import schema
from Urn.views import addresses


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
    if request.user.is_superuser or request.user.is_staff:
        businesses = Businesses.objects.all()
        return HttpResponse(format_get_businesses(businesses))
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


# This method formats the businesses result to JSON form
def format_get_businesses(businesses):
    businesses_data = []
    for business in businesses:
        business_data = OrderedDict()
        business_data['business_guid'] = utils.convert_uuid_string(business.business_guid)
        business_data['name'] = business.name
        business_data['category'] = business.category
        business_data['description'] = business.description
        business_data['business_image'] = business.business_image

        business_addresses = Addresses.objects.filter(business_id=business.business_id)
        addresses_data = addresses.format_addresses(business_addresses)
        business_data['addresses'] = addresses_data

        business_data['created_by'] = business.created_by.user.username
        business_data['updated_by'] = business.updated_by.user.username if business.updated_by is not None else None
        business_data['created_on'] = utils.format_timestamp(business.created_on)
        business_data['updated_on'] = \
            utils.format_timestamp(business.updated_on) if business.updated_on is not None else None
        businesses_data.append(business_data)
    return utils.build_json(businesses_data)
