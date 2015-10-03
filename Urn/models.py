# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin sqlcustom [app_label]'
# into your database.
from __future__ import unicode_literals
from django_enumfield import enum
from jsonfield import JSONField
from django.db import models


class Role(enum.Enum):
    owner = 1
    admin = 2
    member = 3


class Rating(enum.Enum):
    RATING_ZERO = 0
    RATING_ONE = 1
    RATING_TWO = 2
    RATING_THREE = 3
    RATING_FOUR = 4
    RATING_FIVE = 5


class Status(enum.Enum):
    active = 1
    online = 2
    offline = 3
    deleted = 4


class Addresses(models.Model):
    address_id = models.AutoField(primary_key=True)
    address_guid = models.UUIDField(unique=True)
    is_default = models.NullBooleanField()
    street_1 = models.CharField(max_length=50, blank=True, null=True)
    street_2 = models.CharField(max_length=50, blank=True, null=True)
    city = models.CharField(max_length=30)
    state = models.CharField(max_length=30, blank=True, null=True)
    pincode = models.SmallIntegerField()
    country = models.CharField(max_length=30)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    created_on = models.DateTimeField(blank=True, null=True)
    updated_on = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'addresses'


class BusinessAddresses(models.Model):
    business = models.ForeignKey('Businesses')
    address = models.ForeignKey(Addresses)
    created_on = models.DateTimeField(blank=True, null=True)
    updated_on = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'business_addresses'
        unique_together = (('business', 'address'),)


class BusinessUsers(models.Model):
    business = models.ForeignKey('Businesses')
    user = models.ForeignKey('Users')
    role = enum.EnumField(Role, default=Role.admin)
    created_on = models.DateTimeField(blank=True, null=True)
    updated_on = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'business_users'
        unique_together = (('business', 'user'),)


class Businesses(models.Model):
    business_id = models.AutoField(primary_key=True)
    business_guid = models.UUIDField(unique=True)
    name = models.CharField(max_length=50, blank=True, null=True)
    category = models.CharField(max_length=20, blank=True, null=True)
    description = models.CharField(max_length=1024, blank=True, null=True)
    created_by = models.ForeignKey('Users', db_column='created_by', blank=True, null=True,
                                   related_name='businesses_created_by')
    updated_by = models.ForeignKey('Users', db_column='updated_by', blank=True, null=True,
                                   related_name='businesses_updated_by')
    created_on = models.DateTimeField(blank=True, null=True)
    updated_on = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'businesses'


class CartItems(models.Model):
    cart_item_id = models.AutoField(primary_key=True)
    cart_item_guid = models.UUIDField(unique=True)
    product = models.ForeignKey('Products')
    user = models.ForeignKey('Users')
    product_data = JSONField(blank=True, null=True)
    created_on = models.TimeField(blank=True, null=True)
    updated_on = models.TimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cart_items'


class Coupons(models.Model):
    coupon_id = models.AutoField(primary_key=True)
    coupon_guid = models.UUIDField(unique=True)
    code = models.CharField(max_length=30)
    discount_value = models.IntegerField()
    is_percentage = models.NullBooleanField()
    created_on = models.DateTimeField(blank=True, null=True)
    updated_on = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'coupons'


class Discounts(models.Model):
    discount_id = models.AutoField(primary_key=True)
    discount_guid = models.UUIDField(unique=True)
    product = models.ForeignKey('Products', blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    start_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)
    discount_value = models.FloatField(blank=True, null=True)
    is_percentage = models.NullBooleanField()
    product_quantity = models.IntegerField(blank=True, null=True)
    active = models.NullBooleanField()
    created_by = models.ForeignKey('Users', db_column='created_by', blank=True, null=True,
                                   related_name='discounts_created_by')
    updated_by = models.ForeignKey('Users', db_column='updated_by', blank=True, null=True,
                                   related_name='discounts_updated_by')
    created_on = models.DateTimeField(blank=True, null=True)
    updated_on = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'discounts'


class EntityKeywords(models.Model):
    entity_keyword_id = models.AutoField(primary_key=True)
    keyword = models.ForeignKey('Keywords')
    entity_id = models.IntegerField()
    entity_type = models.CharField(max_length=20)
    created_on = models.DateTimeField(blank=True, null=True)
    updated_on = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'entity_keywords'


class Keywords(models.Model):
    keyword_id = models.AutoField(primary_key=True)
    keyword_guid = models.UUIDField(unique=True)
    name = models.CharField(max_length=30, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey('Users', db_column='created_by', related_name='keywords_created_by')
    updated_by = models.ForeignKey('Users', db_column='updated_by', related_name='keywords_updated_by')
    created_on = models.DateTimeField(blank=True, null=True)
    updated_on = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'keywords'


class OrderDetails(models.Model):
    order_detail_id = models.AutoField(primary_key=True)
    order = models.ForeignKey('Orders')
    delivery_party_name = models.CharField(max_length=30)
    product = models.ForeignKey('Products')
    discount = models.ForeignKey(Discounts, blank=True, null=True)
    final_cost = models.FloatField(blank=True, null=True)
    status = models.NullBooleanField()
    product_data = JSONField(blank=True, null=True)
    created_on = models.DateTimeField(blank=True, null=True)
    updated_on = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'order_details'


class Orders(models.Model):
    order_id = models.AutoField(primary_key=True)
    order_guid = models.UUIDField(unique=True)
    user = models.ForeignKey('Users')
    address_id = models.IntegerField()
    coupon = models.ForeignKey(Coupons, blank=True, null=True)
    created_by = models.ForeignKey('Users', db_column='created_by', blank=True, null=True,
                                   related_name='orders_created_by')
    updated_by = models.ForeignKey('Users', db_column='updated_by', blank=True, null=True,
                                   related_name='orders_updated_by')
    created_on = models.DateTimeField(blank=True, null=True)
    updated_on = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'orders'


class ProductImages(models.Model):
    product_image_id = models.AutoField(primary_key=True)
    product = models.ForeignKey('Products')
    url = models.CharField(max_length=255, blank=True, null=True)
    size = models.SmallIntegerField(blank=True, null=True)
    created_on = models.DateTimeField(blank=True, null=True)
    updated_on = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'product_images'


class Products(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_guid = models.UUIDField(unique=True)
    name = models.CharField(max_length=50, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    status = models.NullBooleanField()
    price = models.FloatField()
    product_data = JSONField(blank=True, null=True)
    business = models.ForeignKey(Businesses)
    sku = models.ForeignKey('Sku')
    created_by = models.ForeignKey('Users', db_column='created_by', blank=True, null=True,
                                   related_name='products_created_by')
    updated_by = models.ForeignKey('Users', db_column='updated_by', blank=True, null=True,
                                   related_name='products_updated_by')
    created_on = models.DateTimeField(blank=True, null=True)
    updated_on = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'products'


class Reviews(models.Model):
    review_id = models.AutoField(primary_key=True)
    review_guid = models.UUIDField(unique=True)
    rating = enum.EnumField(Rating, default=Rating.RATING_ZERO)
    review_detail = models.TextField(blank=True, null=True)
    user = models.ForeignKey('Users')
    business = models.ForeignKey(Businesses, blank=True, null=True)
    product_id = models.IntegerField(blank=True, null=True)
    created_on = models.DateTimeField(blank=True, null=True)
    updated_on = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'reviews'


class Sku(models.Model):
    sku_id = models.AutoField(primary_key=True)
    sku_guid = models.UUIDField(unique=True)
    name = models.CharField(max_length=30, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    status = models.NullBooleanField()
    business = models.ForeignKey(Businesses)
    created_by = models.ForeignKey('Users', db_column='created_by', blank=True, null=True,
                                   related_name='sku_created_by')
    updated_by = models.ForeignKey('Users', db_column='updated_by', blank=True, null=True,
                                   related_name='sku_updated_by')
    created_on = models.DateTimeField()
    updated_on = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'sku'


class Tokens(models.Model):
    token_id = models.AutoField(primary_key=True)
    user = models.ForeignKey('Users')
    token = models.CharField(max_length=255)
    token_key = models.CharField(unique=True, max_length=255)
    expiry = models.DateTimeField(blank=True, null=True)
    created_on = models.DateTimeField(blank=True, null=True)
    updated_on = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tokens'


class UserAddresses(models.Model):
    user = models.ForeignKey('Users')
    address = models.ForeignKey(Addresses)
    created_on = models.DateTimeField(blank=True, null=True)
    updated_on = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_addresses'
        unique_together = (('user', 'address'),)


class Users(models.Model):
    user_id = models.AutoField(primary_key=True)
    user_guid = models.UUIDField(unique=True)
    email = models.CharField(unique=True, max_length=120)
    username = models.CharField(unique=True, max_length=20)
    password = models.CharField(max_length=30)
    first_name = models.CharField(max_length=20, blank=True, null=True)
    last_name = models.CharField(max_length=20, blank=True, null=True)
    phone = models.CharField(max_length=12)
    is_business_user = models.NullBooleanField()
    is_superuser = models.NullBooleanField()
    status = enum.EnumField(Status, default=Status.active)
    last_logged_on = models.DateTimeField(blank=True, null=True)
    push_notification = models.NullBooleanField()
    email_notification = models.NullBooleanField()
    sms_notification = models.NullBooleanField()
    created_on = models.DateTimeField(blank=True, null=True)
    updated_on = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'users'


class Wishlist(models.Model):
    wishlist_id = models.AutoField(primary_key=True)
    wishlist_guid = models.UUIDField(unique=True)
    user = models.ForeignKey(Users, blank=True, null=True)
    product = models.ForeignKey(Products)
    product_data = JSONField(blank=True, null=True)
    created_on = models.DateTimeField(blank=True, null=True)
    updated_on = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'wishlist'
