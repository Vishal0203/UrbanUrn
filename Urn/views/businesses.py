from collections import OrderedDict
from django.http import HttpResponse, HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt
from Urn.common import utils
from Urn.decorators.validators import jwt_validate
from Urn.models import Businesses


@csrf_exempt
@jwt_validate
def api_businesses(request):
    if request.method in ['GET']:
        if request.user.is_superuser or request.user.is_staff:
            businesses = Businesses.objects.all()
            return HttpResponse(format_get_businesses(businesses))
        else:
            return HttpResponse(status=401, content='You are not authorized to use this API.')
    else:
        return HttpResponseNotFound("Page Not Found")


# This method formats the businesses result to JSON form
def format_get_businesses(businesses):
    businesses_data = []
    for business in businesses:
        business_data = OrderedDict()
        business_data['business_guid'] = utils.convert_uuid_string(business.business_guid)
        business_data['name'] = business.name
        business_data['category'] = business.category
        business_data['description'] = business.description
        business_data['created_by'] = business.created_by.user.username
        business_data['updated_by'] = business.updated_by.user.username if (business.updated_by != None) else ''
        business_data['created_on'] = utils.format_timestamp(business.created_on)
        business_data['updated_on'] = utils.format_timestamp(business.updated_on)
        businesses_data.append(business_data)
    return utils.build_json(businesses_data)
