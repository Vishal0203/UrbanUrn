from collections import OrderedDict

from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

from Urn.decorators.validators import jwt_validate, check_authenticity, validate_schema
from Urn.models import Sku, Products
from Urn.common import utils


@csrf_exempt
def process_sku_request(request):
    if request.method in ['POST', 'PUT']:
        return process_sku_post(request)
    else:
        return process_sku_get(request)


@jwt_validate
@check_authenticity
@validate_schema
def process_sku_post(request):
    pass


def process_sku_get(request):
    url_params = request.GET
    if len(url_params) == 0:
        skus = Sku.objects.all()
        return HttpResponse(format_skus(skus))
    elif len(url_params) == 1 and 'sku_guid' in url_params:
        sku_guid = url_params['sku_guid']
        sku = Sku.objects.get(sku_guid=sku_guid)
        if sku.status:
            products = Products.objects.filter(sku_id=sku.sku_id)
            return HttpResponse(format_products(products))


def format_skus(skus):
    skus_data = []
    for sku in skus:
        sku_data = OrderedDict()
        sku_data['sku_guid'] = utils.convert_uuid_string(sku.sku_guid)
        sku_data['name'] = sku.name
        sku_data['description'] = sku.description
        skus_data.append(sku_data)
    return utils.build_json(skus_data)


def format_products(products):
    products_data = []
    for product in products:
        product_data = OrderedDict()
        product_data['product_guid'] = utils.convert_uuid_string(product.product_guid)
        product_data['name'] = product.name
        product_data['description'] = product.description
        product_data['price'] = product.price
        product_data['product_data'] = product.product_data
        product_data['business_id'] = product.business_id
        products_data.append(product_data)
    return utils.build_json(products_data)
