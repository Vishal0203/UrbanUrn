import json
from Urn.common import utils
from collections import OrderedDict
from Urn.models import Sku, Products
from django.views.decorators.csrf import csrf_exempt
from Urn.schema_validators.sku_validation import schema
from django.http import HttpResponse, HttpResponseBadRequest
from Urn.common.utils import build_json, convert_uuid_string
from Urn.decorators.validators import jwt_validate, check_authenticity, validate_schema


@csrf_exempt
def process_sku_request(request):
    if request.method in ['POST', 'PUT']:
        return process_sku_post(request)
    else:
        return process_sku_get(request)


@jwt_validate
@check_authenticity
@validate_schema(schema)
def process_sku_post(request):
    request_data = json.loads(request.body.decode())
    if request.method == 'POST':
        if not Sku.objects.filter(name=request_data["name"]).exists():
            Sku.objects.create(name=request_data["name"], description=request_data["description"],
                               business_id=request_data["business_id"] if 'business_id' in request_data else None,
                               created_by=request.user.user_profile)
            return HttpResponse(status=201, content='sku created')
        else:
            sku_guid = {
                "sku_guid": convert_uuid_string(Sku.objects.get(name=request_data["name"]).sku_guid)
            }
            return HttpResponse(build_json(arg=sku_guid))

    else:
        sku = Sku.objects.filter(sku_guid=request_data["sku_guid"])
        if sku.exists():
            request_data["updated_by"] = request.user.user_profile
            sku.update(**request_data)
            return HttpResponse(status=201, content='sku updated')
        else:
            return HttpResponseBadRequest('No such sku to update')


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


@csrf_exempt
def process_products_request(request):
    if request.method in ['POST', 'PUT']:
        return process_products_post(request)
    else:
        return process_products_get(request)


def process_products_post(request):
    pass


def process_products_get(request):
    pass
