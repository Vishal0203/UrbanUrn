import json

from django.http import HttpResponse, HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt

from Urn.common import utils
from Urn.decorators.validators import validate_schema, jwt_validate
from Urn.models import Addresses
from Urn.schema_validators.addresses_validator import schema


@csrf_exempt
@jwt_validate
@validate_schema(schema)
def api_user_addresses(request):
    if request.method in ['POST']:
        user = request.user
        request_data = json.loads(request.body.decode())
        street1 = request_data['street1'] if 'street1' in request_data else None
        street2 = request_data['street2'] if 'street2' in request_data else None
        state = request_data['state'] if 'state' in request_data else None
        if 'is_default' in request_data:
            is_default = utils.request_boolean_field_value(request_data['is_default'])
        else:
            is_default = False
        Addresses.objects.create(city=request_data['city'], pincode=request_data['pincode'],
                                 country=request_data['country'], street_1=street1,
                                 street_2=street2, state=state, is_default=is_default,
                                 user=user.user_profile)
        return HttpResponse(status=201, content='Address created')
    else:
        HttpResponseNotFound('API not found')
