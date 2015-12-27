import os
import json
import requests
import openpyxl
from UrbanurnHelper.Classes.SkuExcelReader import SkuExcelReader
from UrbanurnHelper.config.env import excel_config


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

    parent_sku_mapping = {}
    for sku in sku_jsons:
        print("Pumping SKU...................................", end="")
        r = requests.post(skus_url, headers=uu_auth_header, cookies=auth_object.session_id, data=json.dumps(sku))
        if r.status_code == 201:
            if sku_type == 'parent':
                parent_sku_mapping[json.loads(r.text).get('sku_guid')] = {'category': "", 'name': ""}
                parent_sku_mapping[json.loads(r.text).get('sku_guid')]['category'] = sku.get('category')
                parent_sku_mapping[json.loads(r.text).get('sku_guid')]['name'] = sku.get('name')

            print("[ PASSED {0} ]".format(sku.get('name')))
        else:
            print("[ FAILED {0} ]".format(sku.get('name')))

    if len(parent_sku_mapping.keys()) is not 0:
        print("Writing to Child Excel...........................", end="")
        update_child_excel(parent_sku_mapping)
        print("[ OK ]")


def update_child_excel(parent_sku_mapping):
    wb = openpyxl.load_workbook(excel_config.get('SKU_CHILD_EXCEL'))
    sheet = wb.get_sheet_by_name('Sheet1')

    keys_to_look = {
        "parent_sku_guid": 0,
        "parent_sku_name": 0,
        "category": 0
    }

    for index, row in enumerate(sheet.rows):
        if index is 0:
            for key, cell in enumerate(row):
                if cell.value in keys_to_look.keys():
                    keys_to_look[cell.value] = key
        else:
            excel_writer(row, keys_to_look, parent_sku_mapping)

    wb.save(excel_config.get('SKU_CHILD_EXCEL'))


def excel_writer(row, keys, mapping):
    row_list = list(row)
    for sku_guid in mapping.keys():
        name, category = mapping[sku_guid]['name'], mapping[sku_guid]['category']
        if row_list[keys.get('parent_sku_name')].value == name and row_list[keys.get('category')].value == category:
            row_list[keys.get('parent_sku_guid')].value = sku_guid
