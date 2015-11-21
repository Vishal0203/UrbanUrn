import json
import os
from collections import OrderedDict

from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotFound

from Urn.common.formatters import format_skus, format_products
from Urn.models import Sku, Products, Businesses, ProductImages, BusinessUsers
from Urn.schema_validators.products_validation import put_schema, schema as post_schema
from Urn.schema_validators.sku_validation import schema
from Urn.common.utils import build_json, convert_uuid_string
from Urn.decorators.validators import jwt_validate, check_authenticity, validate_schema, check_business_or_super, \
    validate_post_request_schema


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


@csrf_exempt
def process_products_request(request):
    if request.method == 'POST' and request.POST.get('_method', None) is None:
        return process_products_post(request)
    elif request.method == 'POST' and request.POST.get('_method', None) == 'PUT':
        return process_products_put(request)
    elif request.method == 'GET':
        return process_products_get(request)
    elif request.method == 'DELETE':
        return process_products_delete(request)
    else:
        return HttpResponseNotFound("API not found")


@jwt_validate
@check_business_or_super
@validate_post_request_schema(post_schema)
def process_products_post(request):
    request_data = json.loads(request.POST['product_json'])
    files = request.FILES.getlist("product_images")
    business_info = Businesses.objects.get(business_guid=request_data["business_guid"])
    sku_info = Sku.objects.get(sku_guid=request_data["sku_guid"])
    is_fragile = True if request_data.get("is_fragile", None) is not None else False
    product = Products.objects.create(name=request_data["name"], description=request_data["description"],
                                      price=request_data["price"], product_data=request_data["product_data"],
                                      business_id=business_info.business_id, sku_id=sku_info.sku_id,
                                      created_by=request.user.user_profile, is_fragile=is_fragile)
    for file in files:
        ProductImages.objects.create(product_id=product.product_id, image=file)

    return HttpResponse(status=201, content='Product added')


@jwt_validate
@check_business_or_super
@validate_post_request_schema(put_schema)
def process_products_put(request):
    user = request.user
    user_info = request.user.user_profile
    request_data = json.loads(request.POST["product_json"])
    new_images = request.FILES.getlist("new_images")
    deleted_images = json.loads(request.POST["deleted_images"])
    product = Products.objects.filter(product_guid=request_data["product_guid"])
    if product.exists():
        if BusinessUsers.objects.filter(business_id=product.get().business_id,
                                        user_id=user_info.user_id).exists() or user.is_superuser or user.is_staff:
            product_info = product.get()
            sku_info = Sku.objects.get(sku_guid=request_data["sku_guid"])
            request_data["updated_by"] = request.user.user_profile
            request_data["sku_id"] = sku_info.sku_id
            request_data["product_data"] = json.loads(request_data["product_data"])
            del request_data["sku_guid"]
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
            return HttpResponse(status=401, content='You are not authorized to edit this product')
    else:
        return HttpResponseBadRequest('No such product to update')


@jwt_validate
@check_business_or_super
def process_products_delete(request):
    user = request.user
    user_info = request.user.user_profile
    products_to_delete = json.loads(request.body.decode())["product_guid"]
    response = OrderedDict()
    response["success"] = list()
    response["error"] = list()
    for each_product in products_to_delete:
        product_to_delete = Products.objects.filter(product_guid=each_product)
        if product_to_delete.exists():
            if BusinessUsers.objects.filter(business_id=product_to_delete.get().business_id,
                                            user_id=user_info.user_id).exists() or user.is_staff or user.is_superuser:
                success_msg = "Product deleted : "
                response["success"].append(success_msg + product_to_delete.get().name)
                product_to_delete.delete()
            else:
                err = "You are not authorized to delete : "
                response["error"].append(err + product_to_delete.get().name)

    return HttpResponse(build_json(response))


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
