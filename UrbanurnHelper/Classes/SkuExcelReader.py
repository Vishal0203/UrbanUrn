import sys
import os
import openpyxl
from UrbanurnHelper.config.env import excel_config, config


class SkuExcelReader:
    def __init__(self, sku_type):
        self.sku_parent_json = []
        self.sku_child_json = []
        self.required_columns = {}
        self.type = sku_type

        try:
            if self.type == 'parent':
                wb = openpyxl.load_workbook(excel_config.get('SKU_PARENT_EXCEL'))
                self.upload_parent_sku(wb)
            else:
                wb = openpyxl.load_workbook(excel_config.get('SKU_CHILD_EXCEL'))
                self.upload_child_sku(wb)

        except FileNotFoundError as e:
            print("[ FAIL ]")
            print(e)
            sys.exit(1)

    def upload_parent_sku(self, workbook):
        sheet = workbook.get_sheet_by_name('Sheet1')
        print("[ OK ]")
        print("Building payload...............................")
        for index, row in enumerate(sheet.rows):
            if index is 0:
                for key, cell in enumerate(row):
                    if cell.value in config.get('SKU_PARENT_KEYS'):
                        self.required_columns[key] = cell.value
            else:
                self.sku_parent_json.append(self.get_required_keys(row, index))

    def get_required_keys(self, row, index):
        sku_json = {}
        for index, key in self.required_columns.items():
            sku_json[key] = row[index].value if row[index].value is not None else ""

        return sku_json

    def upload_child_sku(self, workbook):
        sheet = workbook.get_sheet_by_name('Sheet1')
        print("[ OK ]")
        print("Building payload...............................")
        for index, row in enumerate(sheet.rows):
            if index is 0:
                for key, cell in enumerate(row):
                    if cell.value in config.get('SKU_CHILD_KEYS'):
                        self.required_columns[key] = cell.value
            else:
                self.sku_child_json.append(self.get_required_keys(row, index))

    def get_parent_sku(self):
        return self.sku_parent_json

    def get_child_sku(self):
        return self.sku_child_json
