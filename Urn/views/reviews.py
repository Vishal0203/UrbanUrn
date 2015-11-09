from collections import OrderedDict
import json
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt
from Urn.common.utils import build_json, convert_uuid_string
from Urn.decorators.validators import jwt_validate, validate_schema
from Urn.models import Products, Reviews
from Urn.schema_validators.reviews_validator import review_schema


@csrf_exempt
def process_reviews_request(request):
    if request.method == 'GET':
        return process_get_request(request)
    elif request.method == 'POST':
        return process_post_request(request)
    elif request.method == 'PUT':
        return process_put_request(request)
    elif request.method == 'DELETE':
        return process_delete_request(request)
    else:
        return HttpResponseBadRequest("API not found")


def process_get_request(request):
    pass


@jwt_validate
@validate_schema(review_schema)
def process_post_request(request):
    request_data = json.loads(request.body.decode())
    product = Products.objects.filter(product_guid=request_data["product_guid"])
    if product.exists():
        product_info = product.get()
        review = Reviews.objects.create(rating=request_data["rating"], review_detail=request_data["review_comment"],
                                        user_id=request.user.user_profile.user_id, business_id=product_info.business_id,
                                        product_id=product_info.product_id)
    else:
        return HttpResponseNotFound("Product not found")

    response = OrderedDict()
    response["review_guid"] = convert_uuid_string(review.review_guid)
    response["reviewer_name"] = "{0} {1}".format(request.user.first_name, request.user.last_name)
    response["review_comment"] = review.review_detail
    return HttpResponse(build_json(response))


@jwt_validate
def process_put_request(request):
    pass


@jwt_validate
def process_delete_request(request):
    pass
