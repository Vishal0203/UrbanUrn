import sys
import os
import openpyxl
from UrbanurnHelper.config.env import excel_config, config


class ProductExcelReader:
    def __init__(self):
        self.product_jsons = []
        self.required_columns = {}

        global wb
        try:
            wb = openpyxl.load_workbook(excel_config.get('PRODUCT_EXCEL'))
        except FileNotFoundError as e:
            print("[ FAIL ]")
            print(e)
            sys.exit(1)

        sheet = wb.get_sheet_by_name('Sheet1')
        print("[ OK ]")
        print("Building payload...............................")
        name_column_number = 0
        for index, row in enumerate(sheet.rows):
            if index is 0:
                for key, cell in enumerate(row):
                    if cell.value in config.get('PRODUCT_KEYS'):
                        if cell.value == 'name':
                            name_column_number = key + 1
                        self.required_columns[key] = cell.value
            else:
                if sheet.cell(row=index + 1, column=name_column_number).value is not None:
                    self.product_jsons.append(self.get_required_keys(row, index))

    def get_required_keys(self, row, product_number):
        product_json = {'product_json': {}}
        product_images = []
        for index, key in self.required_columns.items():
            product_json['product_json'][key] = row[index].value

        product_image_dir = config.get('PRODUCT_IMAGES') + "\product_" + str(product_number)
        for file in os.listdir(product_image_dir):
            if file.lower().endswith('.jpg') or file.lower().endswith('.png'):
                product_images.append(('product_images', (file, open(product_image_dir + "\\" + file, 'rb'), 'image/jpeg')))

        product_json['product_images'] = product_images
        return product_json

    def get_product_json(self):
        return self.product_jsons
