import os


def set_urls(base_url):
    separator = '/'
    uu_api_base = 'api/v1_0'
    os.environ["uu_login"] = base_url + separator + uu_api_base + separator + 'login'
    os.environ["uu_logout"] = base_url + separator + uu_api_base + separator + 'logout'
    os.environ["uu_products"] = base_url + separator + uu_api_base + separator + 'products'
    os.environ["uu_whoami"] = base_url + separator + uu_api_base + separator + 'whoami'
    os.environ["uu_skus"] = base_url + separator + uu_api_base + separator + 'skus'
    return True
