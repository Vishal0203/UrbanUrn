from collections import OrderedDict
from Urn.common import utils


def format_addresses(addresses):
    addresses_data = []
    for address in addresses:
        address_data = OrderedDict()
        address_data['address_guid'] = utils.convert_uuid_string(address.address_guid)
        address_data['is_default'] = address.is_default
        address_data['street_1'] = address.street_1
        address_data['street_2'] = address.street_2
        address_data['city'] = address.city
        address_data['state'] = address.state
        address_data['country'] = address.country
        address_data['pincode'] = address.pincode
        address_data['latitude'] = address.latitude
        address_data['longitude'] = address.longitude
        address_data['created_on'] = utils.format_timestamp(address.created_on)
        address_data['updated_on'] = utils.format_timestamp(
            address.updated_on) if address.updated_on is not None else None
        addresses_data.append(address_data)
    return addresses_data
