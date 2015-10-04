# UrbanUrn

Setting up this application will require the following.

1. Clone the repo.
2. Copy UrbanUrn/settings.py.dist to UrbanUrn/settings.py
3. Go to "database" tag, make changes int Postgres database connection string.

Alembic setup

1. Install alembic using pip

```
pip install alembic
```

2. Modify the database connection URL in alembic.ini
3. Run the following command to migrate the tables to your database

```
alembic upgrade HEAD
```
