import os
import json
import requests
from UrbanurnHelper.Classes.SkuExcelReader import SkuExcelReader


def process_sku_uploads(auth_object, sku_type):
    print("Reading Sku Excel..............................", end="")
    excel_reader = SkuExcelReader(sku_type)
    if sku_type == 'parent':
        sku_jsons = excel_reader.get_parent_sku()
    else:
        sku_jsons = excel_reader.get_child_sku()

    print("[ OK ]")
    skus_url = os.environ.get('uu_skus')
    uu_auth_header = {'X-Urbanurn-Auth': auth_object.jwt_token}

    for sku in sku_jsons:
        print("Pumping SKU...................................", end="")
        r = requests.post(skus_url, headers=uu_auth_header, cookies=auth_object.session_id, data=json.dumps(sku))
        if r.status_code == 201:
            print("[ PASSED {0} ]".format(sku.get('name')))
        else:
            print("[ FAILED {0} ]".format(sku.get('name')))
