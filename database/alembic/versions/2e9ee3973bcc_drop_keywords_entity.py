"""drop_keywords_entity

Revision ID: 2e9ee3973bcc
Revises: 3c6f48c72314
Create Date: 2015-11-15 11:52:31.184000

"""

# revision identifiers, used by Alembic.
revision = '2e9ee3973bcc'
down_revision = '3c6f48c72314'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa

drop_tables = """
DROP TABLE entity_keywords CASCADE;
DROP TABLE keywords CASCADE;
"""

revert_drop = """
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

ALTER TABLE ONLY entity_keywords ALTER COLUMN entity_keyword_id SET DEFAULT nextval('entity_keywords_entity_keyword_id_seq'::regclass);

ALTER TABLE ONLY keywords ALTER COLUMN keyword_id SET DEFAULT nextval('keywords_keyword_id_seq'::regclass);

SELECT pg_catalog.setval('entity_keywords_entity_keyword_id_seq', 1, false);

SELECT pg_catalog.setval('keywords_keyword_id_seq', 1, false);

ALTER TABLE ONLY entity_keywords
    ADD CONSTRAINT "entity_keywords_PRIMARY" PRIMARY KEY (entity_keyword_id);

ALTER TABLE ONLY keywords
    ADD CONSTRAINT "keyword_guid_UNIQUE" UNIQUE (keyword_guid);

ALTER TABLE ONLY keywords
    ADD CONSTRAINT "keywords_PRIMARY" PRIMARY KEY (keyword_id);

CREATE INDEX "fki_entity_keywords_keywords_keyword_id_FK" ON entity_keywords USING btree (keyword_id);

CREATE INDEX "fki_keywords_users_created_by_FK" ON keywords USING btree (created_by);

CREATE INDEX "fki_keywords_users_updated_by_FK" ON keywords USING btree (updated_by);

CREATE TRIGGER "entity_keywords_BINS" BEFORE INSERT ON entity_keywords FOR EACH ROW EXECUTE PROCEDURE before_insert_function();

CREATE TRIGGER "entity_keywords_BUPD" BEFORE UPDATE ON entity_keywords FOR EACH ROW EXECUTE PROCEDURE before_update_function();

CREATE TRIGGER "keywords_BINS" BEFORE INSERT ON keywords FOR EACH ROW EXECUTE PROCEDURE before_insert_function();

CREATE TRIGGER "keywords_BUPD" BEFORE UPDATE ON keywords FOR EACH ROW EXECUTE PROCEDURE before_update_function();

ALTER TABLE ONLY entity_keywords
    ADD CONSTRAINT "entity_keywords_keywords_keyword_id_FK" FOREIGN KEY (keyword_id) REFERENCES keywords(keyword_id) ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE ONLY keywords
    ADD CONSTRAINT "keywords_users_created_by_FK" FOREIGN KEY (created_by) REFERENCES users(user_id) ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE ONLY keywords
    ADD CONSTRAINT "keywords_users_updated_by_FK" FOREIGN KEY (updated_by) REFERENCES users(user_id) ON UPDATE CASCADE ON DELETE CASCADE;
"""


def upgrade():
    op.execute(drop_tables)


def downgrade():
    op.execute(revert_drop)
