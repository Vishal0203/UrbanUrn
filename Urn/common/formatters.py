from collections import OrderedDict
from Urn.views import addresses
from Urn.common import utils
from Urn.models import Addresses


def format_get_businesses(businesses, include_users=False, include_addresses=False):
    businesses_data = []
    for business in businesses:
        business_data = OrderedDict()
        business_data['business_guid'] = utils.convert_uuid_string(business.business_guid)
        business_data['name'] = business.name
        business_data['category'] = business.category
        business_data['description'] = business.description
        business_data['business_image'] = business.business_image

        if include_users:
            business_users = business.users.all()
            business_data['users'] = format_get_business_users(business_users)

        if include_addresses:
            business_addresses = Addresses.objects.filter(business_id=business.business_id)
            business_data['addresses'] = addresses.format_addresses(business_addresses)

        business_data['created_by'] = business.created_by.user.username
        business_data['updated_by'] = business.updated_by.user.username if business.updated_by is not None else None
        business_data['created_on'] = utils.format_timestamp(business.created_on)
        business_data['updated_on'] = utils.format_timestamp(
            business.updated_on) if business.updated_on is not None else None
        businesses_data.append(business_data)
    return businesses_data


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


