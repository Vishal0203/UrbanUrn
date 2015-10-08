"""Added initial tables

Revision ID: 167a46ea121
Revises: 
Create Date: 2015-10-01 14:30:22.157664

"""

# revision identifiers, used by Alembic.
revision = '167a46ea121'
down_revision = None
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


_initial_tables="""
SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;

CREATE EXTENSION IF NOT EXISTS adminpack WITH SCHEMA pg_catalog;

SET search_path = public, pg_catalog;

CREATE TYPE rating_enum AS ENUM (
    '0',
    '1',
    '2',
    '3',
    '4',
    '5'
);

CREATE TYPE role_enum AS ENUM (
    'owner',
    'admin',
    'member'
);

CREATE TYPE status_enum AS ENUM (
    'active',
    'online',
    'offline',
    'deleted'
);

CREATE FUNCTION before_insert_function() RETURNS trigger
    LANGUAGE plpgsql
    AS $$BEGIN
    NEW.created_on := now();
    NEW.updated_on := NULL;
    RETURN NEW;
END;
$$;

CREATE FUNCTION before_update_function() RETURNS trigger
    LANGUAGE plpgsql
    AS $$BEGIN
    NEW.created_on := OLD.created_on;
    NEW.updated_on := now();
    RETURN NEW;
END;$$;

SET default_tablespace = '';

SET default_with_oids = false;

CREATE TABLE addresses (
    address_id integer NOT NULL,
    address_guid uuid NOT NULL,
    is_default boolean DEFAULT false,
    street_1 character varying(50),
    street_2 character varying(50),
    city character varying(30) NOT NULL,
    state character varying(30),
    pincode character varying(15) NOT NULL,
    country character varying(30) NOT NULL,
    latitude double precision,
    longitude double precision,
    created_on timestamp without time zone,
    updated_on timestamp without time zone
);

CREATE TABLE business_addresses (
    business_id integer NOT NULL,
    address_id integer NOT NULL,
    created_on timestamp without time zone,
    updated_on timestamp without time zone
);

CREATE SEQUENCE business_addresses_address_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE business_addresses_address_id_seq OWNED BY addresses.address_id;

CREATE TABLE business_users (
    business_id integer NOT NULL,
    user_id integer NOT NULL,
    role role_enum,
    created_on timestamp without time zone,
    updated_on timestamp without time zone
);

CREATE TABLE businesses (
    business_id integer NOT NULL,
    business_guid uuid NOT NULL,
    name character varying(50),
    category character varying(20),
    description character varying(1024),
    created_by integer,
    updated_by integer,
    created_on timestamp without time zone,
    updated_on timestamp without time zone
);

CREATE SEQUENCE businesses_business_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE businesses_business_id_seq OWNED BY businesses.business_id;

CREATE TABLE cart_items (
    cart_item_id integer NOT NULL,
    cart_item_guid uuid NOT NULL,
    product_id integer NOT NULL,
    user_id integer NOT NULL,
    product_data json,
    created_on time without time zone,
    updated_on time without time zone
);

CREATE SEQUENCE cart_items_cart_item_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE cart_items_cart_item_id_seq OWNED BY cart_items.cart_item_id;

CREATE TABLE coupons (
    coupon_id integer NOT NULL,
    coupon_guid uuid NOT NULL,
    code character varying(30) NOT NULL,
    discount_value integer DEFAULT 0 NOT NULL,
    is_percentage boolean DEFAULT false,
    created_on timestamp without time zone,
    updated_on timestamp without time zone
);

CREATE SEQUENCE coupons_coupon_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE coupons_coupon_id_seq OWNED BY coupons.coupon_id;

CREATE TABLE discounts (
    discount_id integer NOT NULL,
    discount_guid uuid NOT NULL,
    product_id integer,
    description text,
    start_time timestamp without time zone,
    end_time timestamp without time zone,
    discount_value double precision,
    is_percentage boolean DEFAULT false,
    product_quantity integer,
    active boolean DEFAULT false,
    created_by integer,
    updated_by integer,
    created_on timestamp without time zone,
    updated_on timestamp without time zone
);

CREATE SEQUENCE discounts_discount_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE discounts_discount_id_seq OWNED BY discounts.discount_id;

CREATE TABLE entity_keywords (
    entity_keyword_id integer NOT NULL,
    keyword_id integer NOT NULL,
    entity_id integer NOT NULL,
    entity_type character varying(20) NOT NULL,
    created_on timestamp without time zone,
    updated_on timestamp without time zone
);

CREATE SEQUENCE entity_keywords_entity_keyword_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE entity_keywords_entity_keyword_id_seq OWNED BY entity_keywords.entity_keyword_id;

CREATE TABLE keywords (
    keyword_id integer NOT NULL,
    keyword_guid uuid NOT NULL,
    name character varying(30),
    description text,
    created_by integer,
    updated_by integer,
    created_on timestamp without time zone,
    updated_on timestamp without time zone
);

CREATE SEQUENCE keywords_keyword_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE keywords_keyword_id_seq OWNED BY keywords.keyword_id;

CREATE TABLE order_details (
    order_detail_id integer NOT NULL,
    order_id integer NOT NULL,
    delivery_party_name character varying(30) NOT NULL,
    delivery_tracking_number character varying(30) NOT NULL,
    product_id integer NOT NULL,
    discount_id integer,
    final_cost double precision,
    status boolean,
    product_data json,
    created_on timestamp without time zone,
    updated_on timestamp without time zone
);

CREATE SEQUENCE order_details_order_detail_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE order_details_order_detail_id_seq OWNED BY order_details.order_detail_id;

CREATE TABLE orders (
    order_id integer NOT NULL,
    order_guid uuid NOT NULL,
    user_id integer NOT NULL,
    address_id integer NOT NULL,
    coupon_id integer,
    created_by integer,
    updated_by integer,
    created_on timestamp without time zone,
    updated_on timestamp without time zone
);

CREATE SEQUENCE orders_order_id_seq
    START WITH 1000001
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE orders_order_id_seq OWNED BY orders.order_id;

CREATE TABLE product_images (
    product_image_id integer NOT NULL,
    product_id integer NOT NULL,
    url character varying(255),
    size smallint,
    is_default boolean DEFAULT false,
    created_on timestamp without time zone,
    updated_on timestamp without time zone
);

CREATE SEQUENCE product_images_product_image_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE product_images_product_image_id_seq OWNED BY product_images.product_image_id;

CREATE TABLE products (
    product_id integer NOT NULL,
    product_guid uuid NOT NULL,
    name character varying(50),
    description text,
    status boolean,
    price double precision NOT NULL,
    product_data json,
    business_id integer NOT NULL,
    sku_id integer NOT NULL,
    created_by integer,
    updated_by integer,
    created_on timestamp without time zone,
    updated_on timestamp without time zone
);

CREATE SEQUENCE products_product_id_seq
    START WITH 10001
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE products_product_id_seq OWNED BY products.product_id;

CREATE TABLE reviews (
    review_id integer NOT NULL,
    review_guid uuid NOT NULL,
    rating rating_enum DEFAULT '0'::rating_enum NOT NULL,
    review_detail text,
    user_id integer NOT NULL,
    business_id integer,
    product_id integer,
    created_on timestamp without time zone,
    updated_on timestamp without time zone
);

CREATE SEQUENCE reviews_review_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE reviews_review_id_seq OWNED BY reviews.review_id;

CREATE TABLE sku (
    sku_id integer NOT NULL,
    sku_guid uuid NOT NULL,
    name character varying(30),
    description text,
    status boolean,
    business_id integer NOT NULL,
    created_by integer,
    updated_by integer,
    created_on timestamp without time zone,
    updated_on timestamp without time zone
);

CREATE SEQUENCE sku_sku_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE sku_sku_id_seq OWNED BY sku.sku_id;

CREATE TABLE tokens (
    token_id integer NOT NULL,
    user_id integer NOT NULL,
    token character varying(255) NOT NULL,
    token_key character varying(255) NOT NULL,
    expiry timestamp without time zone,
    created_on timestamp without time zone,
    updated_on timestamp without time zone
);

CREATE SEQUENCE tokens_token_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE tokens_token_id_seq OWNED BY tokens.token_id;

CREATE TABLE user_addresses (
    user_id integer NOT NULL,
    address_id integer NOT NULL,
    created_on timestamp without time zone,
    updated_on timestamp without time zone
);

CREATE TABLE users (
    id integer NOT NULL,
    user_id integer NOT NULL,
    user_guid uuid NOT NULL,
    phone character varying(12) NOT NULL,
    is_business_user boolean DEFAULT false,
    status status_enum DEFAULT 'active'::status_enum NOT NULL,
    push_notification boolean DEFAULT false,
    email_notification boolean DEFAULT true,
    sms_notification boolean DEFAULT false,
    created_on timestamp without time zone,
    updated_on timestamp without time zone
);

CREATE SEQUENCE users_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE users_id_seq OWNED BY users.id;

CREATE TABLE wishlist (
    wishlist_id integer NOT NULL,
    wishlist_guid uuid NOT NULL,
    user_id integer,
    product_id integer NOT NULL,
    product_data json,
    created_on timestamp without time zone,
    updated_on timestamp without time zone
);

CREATE SEQUENCE wishlist_wishlist_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE wishlist_wishlist_id_seq OWNED BY wishlist.wishlist_id;

ALTER TABLE ONLY addresses ALTER COLUMN address_id SET DEFAULT nextval('business_addresses_address_id_seq'::regclass);

ALTER TABLE ONLY businesses ALTER COLUMN business_id SET DEFAULT nextval('businesses_business_id_seq'::regclass);

ALTER TABLE ONLY cart_items ALTER COLUMN cart_item_id SET DEFAULT nextval('cart_items_cart_item_id_seq'::regclass);

ALTER TABLE ONLY coupons ALTER COLUMN coupon_id SET DEFAULT nextval('coupons_coupon_id_seq'::regclass);

ALTER TABLE ONLY discounts ALTER COLUMN discount_id SET DEFAULT nextval('discounts_discount_id_seq'::regclass);

ALTER TABLE ONLY entity_keywords ALTER COLUMN entity_keyword_id SET DEFAULT nextval('entity_keywords_entity_keyword_id_seq'::regclass);

ALTER TABLE ONLY keywords ALTER COLUMN keyword_id SET DEFAULT nextval('keywords_keyword_id_seq'::regclass);

ALTER TABLE ONLY order_details ALTER COLUMN order_detail_id SET DEFAULT nextval('order_details_order_detail_id_seq'::regclass);

ALTER TABLE ONLY orders ALTER COLUMN order_id SET DEFAULT nextval('orders_order_id_seq'::regclass);

ALTER TABLE ONLY product_images ALTER COLUMN product_image_id SET DEFAULT nextval('product_images_product_image_id_seq'::regclass);

ALTER TABLE ONLY products ALTER COLUMN product_id SET DEFAULT nextval('products_product_id_seq'::regclass);

ALTER TABLE ONLY reviews ALTER COLUMN review_id SET DEFAULT nextval('reviews_review_id_seq'::regclass);

ALTER TABLE ONLY sku ALTER COLUMN sku_id SET DEFAULT nextval('sku_sku_id_seq'::regclass);

ALTER TABLE ONLY tokens ALTER COLUMN token_id SET DEFAULT nextval('tokens_token_id_seq'::regclass);

ALTER TABLE ONLY users ALTER COLUMN id SET DEFAULT nextval('users_id_seq'::regclass);

ALTER TABLE ONLY wishlist ALTER COLUMN wishlist_id SET DEFAULT nextval('wishlist_wishlist_id_seq'::regclass);

SELECT pg_catalog.setval('business_addresses_address_id_seq', 1, false);

SELECT pg_catalog.setval('businesses_business_id_seq', 1, false);

SELECT pg_catalog.setval('cart_items_cart_item_id_seq', 1, false);

SELECT pg_catalog.setval('coupons_coupon_id_seq', 1, false);

SELECT pg_catalog.setval('discounts_discount_id_seq', 1, false);

SELECT pg_catalog.setval('entity_keywords_entity_keyword_id_seq', 1, false);

SELECT pg_catalog.setval('keywords_keyword_id_seq', 1, false);

SELECT pg_catalog.setval('order_details_order_detail_id_seq', 1, false);

SELECT pg_catalog.setval('orders_order_id_seq', 1000001, false);

SELECT pg_catalog.setval('product_images_product_image_id_seq', 1, false);

SELECT pg_catalog.setval('products_product_id_seq', 1000001, false);

SELECT pg_catalog.setval('reviews_review_id_seq', 1, false);

SELECT pg_catalog.setval('sku_sku_id_seq', 1, false);

SELECT pg_catalog.setval('tokens_token_id_seq', 1, false);

SELECT pg_catalog.setval('users_id_seq', 1, false);

SELECT pg_catalog.setval('wishlist_wishlist_id_seq', 1, false);

ALTER TABLE ONLY addresses
    ADD CONSTRAINT "address_guid_UNIQUE" UNIQUE (address_guid);

ALTER TABLE ONLY addresses
    ADD CONSTRAINT "addresses_PRIMARY" PRIMARY KEY (address_id);

ALTER TABLE ONLY business_addresses
    ADD CONSTRAINT "business_addresses_PRIMARY" PRIMARY KEY (business_id, address_id);

ALTER TABLE ONLY businesses
    ADD CONSTRAINT "business_guid_UNIQUE" UNIQUE (business_guid);

ALTER TABLE ONLY business_users
    ADD CONSTRAINT "business_users_PRIMARY" PRIMARY KEY (business_id, user_id);

ALTER TABLE ONLY businesses
    ADD CONSTRAINT "businesses_PRIMARY" PRIMARY KEY (business_id);

ALTER TABLE ONLY cart_items
    ADD CONSTRAINT "cart_item_guid_UNIQUE" UNIQUE (cart_item_guid);

ALTER TABLE ONLY cart_items
    ADD CONSTRAINT "cart_items_PRIMARY" PRIMARY KEY (cart_item_id);

ALTER TABLE ONLY coupons
    ADD CONSTRAINT "coupon_guid_UNIQUE" UNIQUE (coupon_guid);

ALTER TABLE ONLY coupons
    ADD CONSTRAINT "coupons_PRIMARY" PRIMARY KEY (coupon_id);

ALTER TABLE ONLY discounts
    ADD CONSTRAINT "discount_guid_UNIQUE" UNIQUE (discount_guid);

ALTER TABLE ONLY discounts
    ADD CONSTRAINT "discounts_PRIMARY" PRIMARY KEY (discount_id);

ALTER TABLE ONLY entity_keywords
    ADD CONSTRAINT "entity_keywords_PRIMARY" PRIMARY KEY (entity_keyword_id);

ALTER TABLE ONLY keywords
    ADD CONSTRAINT "keyword_guid_UNIQUE" UNIQUE (keyword_guid);

ALTER TABLE ONLY keywords
    ADD CONSTRAINT "keywords_PRIMARY" PRIMARY KEY (keyword_id);

ALTER TABLE ONLY order_details
    ADD CONSTRAINT "order_details_PRIMARY" PRIMARY KEY (order_detail_id);

ALTER TABLE ONLY orders
    ADD CONSTRAINT "order_guid_UNIQUE" UNIQUE (order_guid);

ALTER TABLE ONLY orders
    ADD CONSTRAINT "orders_PRIMARY" PRIMARY KEY (order_id);

ALTER TABLE ONLY products
    ADD CONSTRAINT "product_guid_UNIQUE" UNIQUE (product_guid);

ALTER TABLE ONLY product_images
    ADD CONSTRAINT "product_images_PRIMARY" PRIMARY KEY (product_image_id);

ALTER TABLE ONLY products
    ADD CONSTRAINT "products_PRIMARY" PRIMARY KEY (product_id);

ALTER TABLE ONLY reviews
    ADD CONSTRAINT "review_guid_UNIQUE" UNIQUE (review_guid);

ALTER TABLE ONLY reviews
    ADD CONSTRAINT "reviews_PRIMARY" PRIMARY KEY (review_id);

ALTER TABLE ONLY sku
    ADD CONSTRAINT "sku_PRIMARY" PRIMARY KEY (sku_id);

ALTER TABLE ONLY sku
    ADD CONSTRAINT "sku_guid_UNIQUE" UNIQUE (sku_guid);

ALTER TABLE ONLY tokens
    ADD CONSTRAINT "token_key_UNIQUE" UNIQUE (token_key);

ALTER TABLE ONLY tokens
    ADD CONSTRAINT "tokens_PRIMARY" PRIMARY KEY (token_id);

ALTER TABLE ONLY user_addresses
    ADD CONSTRAINT "user_addresses_PRIMARY" PRIMARY KEY (user_id, address_id);

ALTER TABLE ONLY users
    ADD CONSTRAINT "user_id_UNIQUE" UNIQUE (user_id);

ALTER TABLE ONLY users
    ADD CONSTRAINT "user_guid_UNIQUE" UNIQUE (user_guid);

ALTER TABLE ONLY users
    ADD CONSTRAINT "users_PRIMARY" PRIMARY KEY (id);

ALTER TABLE ONLY wishlist
    ADD CONSTRAINT "wishlist_PRIMARY" PRIMARY KEY (wishlist_id);

ALTER TABLE ONLY wishlist
    ADD CONSTRAINT "wishlist_guid_UNIQUE" UNIQUE (wishlist_guid);

CREATE INDEX "fki_business_addresses_addresses_address_id_FK" ON business_addresses USING btree (address_id);

CREATE INDEX fki_business_users_users_user_id ON business_users USING btree (user_id);

CREATE INDEX "fki_businesses_users_created_by_FK" ON businesses USING btree (created_by);

CREATE INDEX "fki_businesses_users_updated_by_FK" ON businesses USING btree (updated_by);

CREATE INDEX "fki_cart_items_products_product_id_FK" ON cart_items USING btree (product_id);

CREATE INDEX "fki_cart_items_users_user_id_FK" ON cart_items USING btree (user_id);

CREATE INDEX "fki_discounts_products_product_id_FK" ON discounts USING btree (product_id);

CREATE INDEX "fki_discounts_users_created_by_FK" ON discounts USING btree (created_by);

CREATE INDEX "fki_discounts_users_updated_by_FK" ON discounts USING btree (updated_by);

CREATE INDEX "fki_entity_keywords_keywords_keyword_id_FK" ON entity_keywords USING btree (keyword_id);

CREATE INDEX "fki_keywords_users_created_by_FK" ON keywords USING btree (created_by);

CREATE INDEX "fki_keywords_users_updated_by_FK" ON keywords USING btree (updated_by);

CREATE INDEX "fki_order_details_discounts_discount_id_FK" ON order_details USING btree (discount_id);

CREATE INDEX "fki_order_details_orders_order_id_FK" ON order_details USING btree (order_id);

CREATE INDEX "fki_order_details_products_product_id_FK" ON order_details USING btree (product_id);

CREATE INDEX "fki_orders_coupons_coupon_id_FK" ON orders USING btree (coupon_id);

CREATE INDEX "fki_orders_users_created_by_FK" ON orders USING btree (created_by);

CREATE INDEX "fki_orders_users_updated_by_FK" ON orders USING btree (updated_by);

CREATE INDEX "fki_orders_users_user_id_FK" ON orders USING btree (user_id);

CREATE INDEX "fki_product_images_products_FK" ON product_images USING btree (product_id);

CREATE INDEX "fki_product_users_updated_by_FK" ON products USING btree (updated_by);

CREATE INDEX "fki_products_businesses_business_id_FK" ON products USING btree (business_id);

CREATE INDEX "fki_products_sku_sku_id_FK" ON products USING btree (sku_id);

CREATE INDEX "fki_products_users_created_by_FK" ON products USING btree (created_by);

CREATE INDEX "fki_reviews_businesses_business_id_FK" ON reviews USING btree (business_id);

CREATE INDEX "fki_reviews_users_user_id_FK" ON reviews USING btree (user_id);

CREATE INDEX "fki_sku_businesses_business_id_FK" ON sku USING btree (business_id);

CREATE INDEX "fki_sku_users_created_by_FK" ON sku USING btree (created_by);

CREATE INDEX "fki_sku_users_updated_by_FK" ON sku USING btree (updated_by);

CREATE INDEX "fki_tokens_users_user_id_FK" ON tokens USING btree (user_id);

CREATE INDEX "fki_user_addresses_addresses_address_id_FK" ON user_addresses USING btree (address_id);

CREATE INDEX "fki_wishlist_products_product_id_FK" ON wishlist USING btree (product_id);

CREATE INDEX "fki_wishlist_users_user_id_FK" ON wishlist USING btree (user_id);

CREATE TRIGGER "addresses_BINS" BEFORE INSERT ON addresses FOR EACH ROW EXECUTE PROCEDURE before_insert_function();

CREATE TRIGGER "addresses_BUPD" BEFORE UPDATE ON addresses FOR EACH ROW EXECUTE PROCEDURE before_update_function();

CREATE TRIGGER "business_addresses_BINS" BEFORE INSERT ON business_addresses FOR EACH ROW EXECUTE PROCEDURE before_insert_function();

CREATE TRIGGER "business_addresses_BUPD" BEFORE UPDATE ON business_addresses FOR EACH ROW EXECUTE PROCEDURE before_update_function();

CREATE TRIGGER "business_users_BINS" BEFORE INSERT ON business_users FOR EACH ROW EXECUTE PROCEDURE before_insert_function();

CREATE TRIGGER "business_users_BUPD" BEFORE UPDATE ON business_users FOR EACH ROW EXECUTE PROCEDURE before_update_function();

CREATE TRIGGER "businesses_BINS" BEFORE INSERT ON businesses FOR EACH ROW EXECUTE PROCEDURE before_insert_function();

CREATE TRIGGER "businesses_BUPD" BEFORE UPDATE ON businesses FOR EACH ROW EXECUTE PROCEDURE before_update_function();

CREATE TRIGGER "cart_items_BINS" BEFORE INSERT ON cart_items FOR EACH ROW EXECUTE PROCEDURE before_insert_function();

CREATE TRIGGER "cart_items_BUPD" BEFORE UPDATE ON cart_items FOR EACH ROW EXECUTE PROCEDURE before_update_function();

CREATE TRIGGER "coupons_BINS" BEFORE INSERT ON coupons FOR EACH ROW EXECUTE PROCEDURE before_insert_function();

CREATE TRIGGER "coupons_BUPD" BEFORE UPDATE ON coupons FOR EACH ROW EXECUTE PROCEDURE before_update_function();

CREATE TRIGGER "discounts_BINS" BEFORE INSERT ON discounts FOR EACH ROW EXECUTE PROCEDURE before_insert_function();

CREATE TRIGGER "discounts_BUPD" BEFORE UPDATE ON discounts FOR EACH ROW EXECUTE PROCEDURE before_update_function();

CREATE TRIGGER "entity_keywords_BINS" BEFORE INSERT ON entity_keywords FOR EACH ROW EXECUTE PROCEDURE before_insert_function();

CREATE TRIGGER "entity_keywords_BUPD" BEFORE UPDATE ON entity_keywords FOR EACH ROW EXECUTE PROCEDURE before_update_function();

CREATE TRIGGER "keywords_BINS" BEFORE INSERT ON keywords FOR EACH ROW EXECUTE PROCEDURE before_insert_function();

CREATE TRIGGER "keywords_BUPD" BEFORE UPDATE ON keywords FOR EACH ROW EXECUTE PROCEDURE before_update_function();

CREATE TRIGGER "order_details_BINS" BEFORE INSERT ON order_details FOR EACH ROW EXECUTE PROCEDURE before_insert_function();

CREATE TRIGGER "order_details_BUPD" BEFORE UPDATE ON order_details FOR EACH ROW EXECUTE PROCEDURE before_update_function();

CREATE TRIGGER "orders_BINS" BEFORE INSERT ON orders FOR EACH ROW EXECUTE PROCEDURE before_insert_function();

CREATE TRIGGER "orders_BUPD" BEFORE UPDATE ON orders FOR EACH ROW EXECUTE PROCEDURE before_update_function();

CREATE TRIGGER "product_images_BINS" BEFORE INSERT ON product_images FOR EACH ROW EXECUTE PROCEDURE before_insert_function();

CREATE TRIGGER "product_images_BUPD" BEFORE UPDATE ON product_images FOR EACH ROW EXECUTE PROCEDURE before_update_function();

CREATE TRIGGER "products_BINS" BEFORE INSERT ON products FOR EACH ROW EXECUTE PROCEDURE before_insert_function();

CREATE TRIGGER "products_BUPD" BEFORE UPDATE ON products FOR EACH ROW EXECUTE PROCEDURE before_update_function();

CREATE TRIGGER "reviews_BINS" BEFORE INSERT ON reviews FOR EACH ROW EXECUTE PROCEDURE before_insert_function();

CREATE TRIGGER "reviews_BUPD" BEFORE UPDATE ON reviews FOR EACH ROW EXECUTE PROCEDURE before_update_function();

CREATE TRIGGER "sku_BINS" BEFORE INSERT ON sku FOR EACH ROW EXECUTE PROCEDURE before_insert_function();

CREATE TRIGGER "sku_BUPD" BEFORE UPDATE ON sku FOR EACH ROW EXECUTE PROCEDURE before_update_function();

CREATE TRIGGER "tokens_BINS" BEFORE INSERT ON tokens FOR EACH ROW EXECUTE PROCEDURE before_insert_function();

CREATE TRIGGER "tokens_BUPD" BEFORE UPDATE ON tokens FOR EACH ROW EXECUTE PROCEDURE before_update_function();

CREATE TRIGGER "user_addresses_BINS" BEFORE INSERT ON user_addresses FOR EACH ROW EXECUTE PROCEDURE before_insert_function();

CREATE TRIGGER "user_addresses_BUPD" BEFORE UPDATE ON user_addresses FOR EACH ROW EXECUTE PROCEDURE before_update_function();

CREATE TRIGGER "users_BINS" BEFORE INSERT ON users FOR EACH ROW EXECUTE PROCEDURE before_insert_function();

CREATE TRIGGER "users_BUPD" BEFORE UPDATE ON users FOR EACH ROW EXECUTE PROCEDURE before_update_function();

CREATE TRIGGER "wishlist_BINS" BEFORE INSERT ON wishlist FOR EACH ROW EXECUTE PROCEDURE before_insert_function();

CREATE TRIGGER "wishlist_BUPD" BEFORE UPDATE ON wishlist FOR EACH ROW EXECUTE PROCEDURE before_update_function();

ALTER TABLE ONLY business_addresses
    ADD CONSTRAINT "business_addresses_addresses_address_id_FK" FOREIGN KEY (address_id) REFERENCES addresses(address_id) ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE ONLY business_addresses
    ADD CONSTRAINT "business_addresses_businesses_business_id_FK" FOREIGN KEY (business_id) REFERENCES businesses(business_id) ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE ONLY business_users
    ADD CONSTRAINT "business_users_businesses_business_id_FK" FOREIGN KEY (business_id) REFERENCES businesses(business_id) ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE ONLY business_users
    ADD CONSTRAINT "business_users_users_user_id_FK" FOREIGN KEY (user_id) REFERENCES users(user_id) ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE ONLY businesses
    ADD CONSTRAINT "businesses_users_created_by_FK" FOREIGN KEY (created_by) REFERENCES users(user_id) ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE ONLY businesses
    ADD CONSTRAINT "businesses_users_updated_by_FK" FOREIGN KEY (updated_by) REFERENCES users(user_id) ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE ONLY cart_items
    ADD CONSTRAINT "cart_items_products_product_id_FK" FOREIGN KEY (product_id) REFERENCES products(product_id) ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE ONLY cart_items
    ADD CONSTRAINT "cart_items_users_user_id_FK" FOREIGN KEY (user_id) REFERENCES users(user_id) ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE ONLY discounts
    ADD CONSTRAINT "discounts_products_product_id_FK" FOREIGN KEY (product_id) REFERENCES products(product_id) ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE ONLY discounts
    ADD CONSTRAINT "discounts_users_created_by_FK" FOREIGN KEY (created_by) REFERENCES users(user_id) ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE ONLY discounts
    ADD CONSTRAINT "discounts_users_updated_by_FK" FOREIGN KEY (updated_by) REFERENCES users(user_id) ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE ONLY entity_keywords
    ADD CONSTRAINT "entity_keywords_keywords_keyword_id_FK" FOREIGN KEY (keyword_id) REFERENCES keywords(keyword_id) ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE ONLY keywords
    ADD CONSTRAINT "keywords_users_created_by_FK" FOREIGN KEY (created_by) REFERENCES users(user_id) ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE ONLY keywords
    ADD CONSTRAINT "keywords_users_updated_by_FK" FOREIGN KEY (updated_by) REFERENCES users(user_id) ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE ONLY order_details
    ADD CONSTRAINT "order_details_discounts_discount_id_FK" FOREIGN KEY (discount_id) REFERENCES discounts(discount_id) ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE ONLY order_details
    ADD CONSTRAINT "order_details_orders_order_id_FK" FOREIGN KEY (order_id) REFERENCES orders(order_id) ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE ONLY order_details
    ADD CONSTRAINT "order_details_products_product_id_FK" FOREIGN KEY (product_id) REFERENCES products(product_id) ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE ONLY orders
    ADD CONSTRAINT "orders_coupons_coupon_id_FK" FOREIGN KEY (coupon_id) REFERENCES coupons(coupon_id);

ALTER TABLE ONLY orders
    ADD CONSTRAINT "orders_users_created_by_FK" FOREIGN KEY (user_id) REFERENCES users(user_id) ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE ONLY orders
    ADD CONSTRAINT "orders_users_updated_by_FK" FOREIGN KEY (updated_by) REFERENCES users(user_id) ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE ONLY orders
    ADD CONSTRAINT "orders_users_user_id_FK" FOREIGN KEY (user_id) REFERENCES users(user_id) ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE ONLY product_images
    ADD CONSTRAINT "product_images_products_product_id_FK" FOREIGN KEY (product_id) REFERENCES products(product_id) ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE ONLY products
    ADD CONSTRAINT "product_users_updated_by_FK" FOREIGN KEY (updated_by) REFERENCES users(user_id) ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE ONLY products
    ADD CONSTRAINT "products_businesses_business_id_FK" FOREIGN KEY (business_id) REFERENCES businesses(business_id) ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE ONLY products
    ADD CONSTRAINT "products_sku_sku_id_FK" FOREIGN KEY (sku_id) REFERENCES sku(sku_id) ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE ONLY products
    ADD CONSTRAINT "products_users_created_by_FK" FOREIGN KEY (created_by) REFERENCES users(user_id) ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE ONLY reviews
    ADD CONSTRAINT "reviews_businesses_business_id_FK" FOREIGN KEY (business_id) REFERENCES businesses(business_id) ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE ONLY reviews
    ADD CONSTRAINT "reviews_users_user_id_FK" FOREIGN KEY (user_id) REFERENCES users(user_id) ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE ONLY sku
    ADD CONSTRAINT "sku_businesses_business_id_FK" FOREIGN KEY (business_id) REFERENCES businesses(business_id) ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE ONLY sku
    ADD CONSTRAINT "sku_users_created_by_FK" FOREIGN KEY (created_by) REFERENCES users(user_id) ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE ONLY sku
    ADD CONSTRAINT "sku_users_updated_by_FK" FOREIGN KEY (updated_by) REFERENCES users(user_id) ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE ONLY tokens
    ADD CONSTRAINT "tokens_users_user_id_FK" FOREIGN KEY (user_id) REFERENCES users(user_id) ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE ONLY users
  ADD CONSTRAINT "users_auth_user_user_id_FK" FOREIGN KEY (user_id) REFERENCES auth_user(id) ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE ONLY user_addresses
    ADD CONSTRAINT "user_addresses_addresses_address_id_FK" FOREIGN KEY (address_id) REFERENCES addresses(address_id) ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE ONLY user_addresses
    ADD CONSTRAINT "user_addresses_users_user_id_FK" FOREIGN KEY (user_id) REFERENCES users(user_id) ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE ONLY wishlist
    ADD CONSTRAINT "wishlist_products_product_id_FK" FOREIGN KEY (product_id) REFERENCES products(product_id) ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE ONLY wishlist
    ADD CONSTRAINT "wishlist_users_user_id_FK" FOREIGN KEY (user_id) REFERENCES users(user_id) ON UPDATE CASCADE ON DELETE CASCADE;

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;

GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;
"""

_initial_down="""
DROP TABLE addresses CASCADE;

DROP TABLE business_addresses CASCADE;

DROP TABLE business_users CASCADE;

DROP TABLE businesses CASCADE;

DROP TABLE cart_items CASCADE;

DROP TABLE coupons CASCADE;

DROP TABLE discounts CASCADE;

DROP TABLE entity_keywords CASCADE;

DROP TABLE keywords CASCADE;

DROP TABLE order_details CASCADE;

DROP TABLE orders CASCADE;

DROP TABLE product_images CASCADE;

DROP TABLE products CASCADE;

DROP TABLE reviews CASCADE;

DROP TABLE sku CASCADE;

DROP TABLE tokens CASCADE;

DROP TABLE user_addresses CASCADE;

DROP TABLE users CASCADE;

DROP TABLE wishlist CASCADE;

DROP FUNCTION before_insert_function();

DROP FUNCTION before_update_function();

DROP TYPE rating_enum;

DROP TYPE role_enum;

DROP TYPE status_enum;
"""

def upgrade():
    op.execute(_initial_tables);


def downgrade():
    op.execute(_initial_down);
