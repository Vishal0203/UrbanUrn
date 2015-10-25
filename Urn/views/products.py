import json
import os
from UrbanUrn import settings
from Urn.common import utils
from collections import OrderedDict
from Urn.models import Sku, Products, Businesses, ProductImages, BusinessUsers
from django.views.decorators.csrf import csrf_exempt

from Urn.schema_validators.sku_validation import schema
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
    sku_data['products'] = format_products(products, False) if products is not None else []
    sku_data['created_by'] = sku.created_by.user.username
    sku_data['updated_by'] = sku.updated_by.user.username if sku.updated_by is not None else None
    sku_data['created_on'] = utils.format_timestamp(sku.created_on)
    sku_data['updated_on'] = utils.format_timestamp(sku.updated_on) if sku.updated_on is not None else None
    return sku_data


def format_products(products, json=True):
    products_data = []
    for product in products:
        product_images = ProductImages.objects.filter(product_id=product.product_id)
        product_data = OrderedDict()
        product_data['product_guid'] = utils.convert_uuid_string(product.product_guid)
        product_data['name'] = product.name
        product_data['description'] = product.description
        product_data['price'] = product.price
        product_data['product_data'] = product.product_data
        product_data['product_images'] = format_product_images(product_images,
                                                               False) if len(product_images) > 0 else []
        product_data['business_guid'] = utils.convert_uuid_string(product.business.business_guid)
        product_data['sku_guid'] = utils.convert_uuid_string(product.sku.sku_guid)
        product_data['created_on'] = utils.format_timestamp(product.created_on)
        product_data['updated_on'] = utils.format_timestamp(
            product.updated_on) if product.updated_on is not None else None
        products_data.append(product_data)
    if json:
        return utils.build_json(products_data)
    return products_data


def format_product_images(product_images, json=True):
    product_images_data = []
    for product_image in product_images:
        product_image_data = OrderedDict()
        product_image_data['product_image_guid'] = utils.convert_uuid_string(product_image.product_image_guid)
        product_image_data['image'] = settings.BASE_URL + product_image.image.url
        product_image_data['size'] = product_image.size
        product_image_data['is_default'] = product_image.is_default
        product_image_data['created_on'] = utils.format_timestamp(product_image.created_on)
        product_image_data['updated_on'] = utils.format_timestamp(
            product_image.updated_on) if product_image.updated_on is not None else None
        product_images_data.append(product_image_data)
    if not json:
        return product_images_data
    return utils.build_json(product_images_data)


@csrf_exempt
def process_products_request(request):
    if request.method == 'POST':
        return process_products_post(request)
    elif request.method == 'GET':
        return process_products_get(request)
    elif request.method == 'DELETE':
        return product_delete_helper(request)
    else:
        return HttpResponseNotFound("API not found")


@jwt_validate
@check_business_or_super
def process_products_post(request):
    if request.method == 'POST' and request.POST.get('_method', None) is None:
        request_data = json.loads(request.POST['product_json'])
        files = request.FILES.getlist("product_images")
        business_info = Businesses.objects.get(business_guid=request_data["business_guid"])
        sku_info = Sku.objects.get(sku_guid=request_data["sku_guid"])
        product = Products.objects.create(name=request_data["name"], description=request_data["description"],
                                          price=request_data["price"], product_data=request_data["product_data"],
                                          business_id=business_info.business_id, sku_id=sku_info.sku_id,
                                          created_by=request.user.user_profile)
        for file in files:
            ProductImages.objects.create(product_id=product.product_id, image=file)

        return HttpResponse(status=201, content='Product added')

    elif request.POST.get('_method', None) == "PUT":
        return product_update_helper(request)


def product_update_helper(request):
    request_data = json.loads(request.POST["product_json"])
    new_images = request.FILES.getlist("new_images")
    deleted_images = json.loads(request.POST["deleted_images"])
    product = Products.objects.filter(product_guid=request_data["product_guid"])
    if product.exists():
        product_info = product.get()
        sku_info = Sku.objects.get(sku_guid=request_data["sku_guid"])
        request_data["updated_by"] = request.user.user_profile
        request_data["sku_id"] = sku_info.sku_id
        request_data["product_data"] = json.loads(request_data["product_data"])
        del request_data["sku_guid"]
        del request_data["business_guid"]
        product.update(**request_data)

        for image in new_images:
            ProductImages.objects.create(product_id=product_info.product_id, image=image)

        for image_guid in deleted_images:
            image_info = ProductImages.objects.get(product_image_guid=image_guid)
            if os.path.exists(image_info.image.url):
                os.remove(image_info.image.url)
            image_info.delete()

        return HttpResponse(status=202, content='Product updated')
    else:
        return HttpResponseBadRequest('No such product to update')


@jwt_validate
@check_business_or_super
def product_delete_helper(request):
    products_to_delete = json.loads(request.body.decode())["product_guid"]
    for each_product in products_to_delete:
        product_to_delete = Products.objects.filter(product_guid=each_product)
        if product_to_delete.exists():
            try:
                if BusinessUsers.objects.filter(business_id=product_to_delete.get().business_id,
                                                user_id=request.user.user_profile.user_id).exists():
                    product_to_delete.delete()
                else:
                    raise BusinessUsers.DoesNotExist
            except BusinessUsers.DoesNotExist:
                return HttpResponse(status=401, content='Not authorized to perform this operation')

    return HttpResponse(status=202, content='Product deleted')


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
