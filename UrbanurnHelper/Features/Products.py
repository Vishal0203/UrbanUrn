import os
import json
import requests
from UrbanurnHelper.Classes.ProductExcelReader import ProductExcelReader


def process_product_uploads(auth_object):
    print("Reading Products Excel.........................", end="")

    excel_reader = ProductExcelReader()
    product_jsons = excel_reader.get_product_json()
    print("[ OK ]")

    products_url = os.environ.get('uu_products')
    uu_auth_header = {'X-Urbanurn-Auth': auth_object.jwt_token}

    for product in product_jsons:
        print("Pumping Product................................", end="")
        product_json = {"product_json": json.dumps(product.get('product_json'))}
        r = requests.post(products_url, files=list(product.get('product_images')), headers=uu_auth_header,
                          cookies=auth_object.session_id, data=product_json)

        if r.status_code == 201:
            print("[ PASSED {0} ]".format(product.get('product_json')['name']))
        else:
            print("[ FAILED {0} ]".format(product.get('product_json')['name']))
