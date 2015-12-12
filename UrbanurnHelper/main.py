import os
import sys
import json
import requests
from UrbanurnHelper.Classes.ExcelReader import ExcelReader
from UrbanurnHelper.Classes.Authentication import Authentication

if __name__ == '__main__':
    auth_object = Authentication()
    payload = auth_object.check_config()
    if not payload:
        print("Reconfigure env.py - keys {0}, {1} or {2} might be missing".format('USERNAME', 'PASSWORD', 'BASE_URL'))
        del auth_object
        sys.exit(1)

    if auth_object.login_admin_user(payload) is True:
        if not auth_object.who_am_i():
            print("Access Denied : Only for superuser or staff")
            del auth_object
            sys.exit(1)

    print("[ OK ]")
    print("Reading Excel..................................", end="")

    excel_reader = ExcelReader()
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
