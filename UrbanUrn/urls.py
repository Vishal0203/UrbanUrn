"""UrbanUrn URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from Urn.views import authentication, users, businesses, products, fulltextsearch, addresses, carts, orders

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/v1_0/login', authentication.validate_input_and_authenticate),
    url(r'^api/v1_0/logout', authentication.logout_and_clear_session),
    url(r'^api/v1_0/refresh_token', authentication.refresh_jwt_token),
    url(r'^api/v1_0/registration', users.registration),
    url(r'^api/v1_0/businesses', businesses.api_businesses),
    url(r'^api/v1_0/users', users.api_users),
    url(r'^api/v1_0/skus', products.process_sku_request),
    url(r'^api/v1_0/products', products.process_products_request),
    url(r'^api/v1_0/carts', carts.process_carts_request),
    url(r'^api/v1_0/orders', orders.process_orders_request),
    url(r'^api/v1_0/whoami', users.who_am_i),
    url(r'^api/v1_0/product/search', fulltextsearch.fts_products),
    url(r'^api/v1_0/addresses', addresses.api_user_addresses)
]
