from collections import OrderedDict
from Urn.views import addresses
from Urn.common import utils
from Urn.models import Addresses, BusinessUsers


def format_get_businesses(businesses, include_users=False, include_addresses=False, user=None):
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
            business_data['users'] = format_get_business_users(business_users, business)

        if include_addresses:
            business_addresses = Addresses.objects.filter(business_id=business.business_id)
            business_data['addresses'] = addresses.format_addresses(business_addresses)

        if user:
            business_data['role'] = get_business_user_entry(business, user).role

        business_data['created_by'] = business.created_by.user.username
        business_data['updated_by'] = business.updated_by.user.username if business.updated_by is not None else None
        business_data['created_on'] = utils.format_timestamp(business.created_on)
        business_data['updated_on'] = utils.format_timestamp(
            business.updated_on) if business.updated_on is not None else None
        businesses_data.append(business_data)
    return businesses_data


def format_get_business_users(business_users, business):
    business_users_data = []
    for business_user in business_users:
        business_user_data = OrderedDict()
        business_user_data['user_guid'] = utils.convert_uuid_string(business_user.user_guid)
        business_user_data['username'] = business_user.user.username
        business_user_data['role'] = get_business_user_entry(business, business_user).role
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


def get_business_user_entry(business, user):
    return BusinessUsers.objects.get(business=business, user=user)


def format_user(user):
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
        user_data['businesses'] = format_get_businesses(user_businesses, False, False, user.user_profile)

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
    return user_data
