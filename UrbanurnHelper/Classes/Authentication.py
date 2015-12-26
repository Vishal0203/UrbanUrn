from collections import OrderedDict
import json
import os
import sys
import requests
from UrbanurnHelper.config.env import config
from UrbanurnHelper.config.env_variable_setter import set_urls


class Authentication:
    def __init__(self):
        self.user_guid = None
        self.jwt_token = None
        self.session_id = None

    def login_admin_user(self, request_payload):
        print("Trying to login................................", end="")
        login_url = os.environ.get('uu_login')
        r = requests.post(login_url, request_payload)

        if r.status_code == requests.codes.ok:
            print('[ OK ]')
            response = r.json()
            self.user_guid = response.get('user_guid')
            self.jwt_token = response.get('token')
            self.session_id = dict(sessionid=r.cookies['sessionid'])
            return True
        else:
            print('[ FAILED ]')
            print(r.reason)
            sys.exit(1)

    def who_am_i(self):
        who_am_i_url = os.environ.get('uu_whoami')
        uu_auth_header = {'X-Urbanurn-Auth': self.jwt_token}
        r = requests.get(who_am_i_url, headers=uu_auth_header, cookies=self.session_id)

        if r.status_code == requests.codes.ok:
            print('Checking authenticity..........................', end="")
            response = r.json()
            if response.get('is_superuser', False) or response.get('is_staff', False):
                return True
            else:
                logout_url = os.environ.get('uu_logout')
                requests.get(logout_url, headers=uu_auth_header, cookies=self.session_id)
                return False

    def check_config(self):
        print("Checking configuration.........................", end="")
        username = config.get('USERNAME') if config.get('USERNAME', None) is not '' or None else None
        password = config.get('PASSWORD') if config.get('PASSWORD', None) is not '' or None else None
        base_url = config.get('BASE_URL') if config.get('BASE_URL', None) is not '' or None else None
        product_images_dir = config.get('PRODUCT_IMAGES') if config.get('PRODUCT_IMAGES',
                                                                        None) is not '' or None else None

        if not os.path.exists(product_images_dir):
            print('[ FAIL ]')
            return False

        if username is None or password is None or base_url is None:
            print('[ FAIL ]')
            return False
        else:
            set_urls(base_url)
            payload = OrderedDict()
            payload['username'] = username
            payload['password'] = password
            print('[ OK ]')

            return json.dumps(payload)
