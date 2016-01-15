import sys
sys.path.append('..')  # needed to run from command prompt

import argparse
from UrbanurnHelper.Features.Products import process_product_uploads
from UrbanurnHelper.Classes.Authentication import Authentication
from UrbanurnHelper.Features.Skus import process_sku_uploads
from UrbanurnHelper.config.env import excel_config

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Upload products and skus')
    parser.add_argument("--product", help="Switch to upload products", action="store_true")
    parser.add_argument("--sku", help="Switch to upload sku", action="store_true")
    args = parser.parse_args()

    if not (args.product or args.sku):
        parser.error('No action requested, add --product or --sku')

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

    if args.sku:
        print("Checking SKU config............................", end="")
        if excel_config.get('SKU_PARENT_EXCEL', None) is None and excel_config.get('SKU_CHILD_EXCEL',
                                                                                   None) is None:
            print("[ FAIL ]")
        else:
            print("[ OK ]")
            print("Uploading parent SKUs........................")
            process_sku_uploads(auth_object, 'parent')

            print("Uploading child SKUs.........................")
            process_sku_uploads(auth_object, 'child')

    if args.product:
        process_product_uploads(auth_object)
