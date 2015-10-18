import json
from Urn.common import utils
from collections import OrderedDict
from Urn.models import Sku, Products, Businesses
from django.views.decorators.csrf import csrf_exempt

from Urn.schema_validators.sku_validation import schema
from Urn.schema_validators.products_validation import schema as product_schema
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotFound
from Urn.common.utils import build_json, convert_uuid_string
from Urn.decorators.validators import jwt_validate, check_authenticity, validate_schema, check_business_or_super


@csrf_exempt
def process_sku_request(request):
    if request.method in ['POST', 'PUT']:
        return process_sku_post(request)
    elif request.method == 'GET':
        return process_sku_get(request)
    else:
        return HttpResponseNotFound("API Not found")


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
            return HttpResponse(status=202, content='sku updated')
        else:
            return HttpResponseBadRequest('No such sku to update')


def process_sku_get(request):
    url_params = request.GET
    if len(url_params) == 0:
        skus = Sku.objects.all()
        result = []
        for sku in skus:
            products = Products.objects.filter(sku_id=sku.sku_id)
            result.append(format_skus(sku, products))
        return HttpResponse(build_json(result))
    elif 'sku_guid' in url_params:
        sku_guid = url_params['sku_guid']
        try:
            sku = Sku.objects.get(sku_guid=sku_guid)
            if sku.status:
                products = Products.objects.filter(sku_id=sku.sku_id)
                return HttpResponse(build_json(format_skus(sku, products)))
        except Sku.DoesNotExist as e:
            return HttpResponseBadRequest("No such SKU exists")
    else:
        return HttpResponseBadRequest("No such SKU exists")


def format_skus(sku, products):
    sku_data = OrderedDict()
    sku_data['sku_guid'] = utils.convert_uuid_string(sku.sku_guid)
    sku_data['name'] = sku.name
    sku_data['description'] = sku.description
    sku_data['id'] = sku.sku_id
    sku_data['products'] = format_products(products, False) if products is not None else []
    return sku_data


def format_products(products, json=True):
    products_data = []
    for product in products:
        product_data = OrderedDict()
        product_data['product_guid'] = utils.convert_uuid_string(product.product_guid)
        product_data['name'] = product.name
        product_data['description'] = product.description
        product_data['price'] = product.price
        product_data['product_data'] = product.product_data
        product_data['business_id'] = product.business_id
        product_data['sku_id'] = product.sku_id
        products_data.append(product_data)
    if not json:
        return products_data
    return utils.build_json(products_data)


@csrf_exempt
def process_products_request(request):
    if request.method in ['POST', 'PUT']:
        return process_products_post(request)
    elif request.method == 'GET':
        return process_products_get(request)
    else:
        return HttpResponseNotFound("API not found")


@jwt_validate
@check_business_or_super
@validate_schema(product_schema)
def process_products_post(request):
    request_data = json.loads(request.body.decode())
    if request.method == 'POST':
        business_info = Businesses.objects.get(business_guid=request_data["business_guid"])
        sku_info = Sku.objects.get(sku_guid=request_data["sku_guid"])
        Products.objects.create(name=request_data["name"], description=request_data["description"],
                                price=request_data["price"], product_data=request_data["product_data"],
                                business_id=business_info.business_id, sku_id=sku_info.sku_id,
                                created_by=request.user.user_profile)
        return HttpResponse(status=201, content='Product added')

    else:
        product = Products.objects.filter(product_guid=request_data["product_guid"])
        if product.exists():
            sku_info = Sku.objects.get(sku_guid=request_data["sku_guid"])
            request_data["updated_by"] = request.user.user_profile
            request_data["sku_id"] = sku_info.sku_id
            request_data["product_data"] = json.loads(request_data["product_data"])
            del request_data["sku_guid"]
            del request_data["business_guid"]
            product.update(**request_data)
            return HttpResponse(status=202, content='Product updated')
        else:
            return HttpResponseBadRequest('No such product to update')


def process_products_get(request):
    url_params = request.GET
    if len(url_params) == 0:
        products = Products.objects.all()
        return HttpResponse(format_products(products))
    elif 'product_guid' in url_params:
        product_guid = url_params['product_guid']
        try:
            product = Products.objects.get(product_guid=product_guid)
            return HttpResponse(format_products([product]))
        except Products.DoesNotExist as e:
            return HttpResponseBadRequest("No such product exists")
    else:
        return HttpResponseBadRequest("No such product exists")
