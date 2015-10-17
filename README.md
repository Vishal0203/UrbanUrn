# UrbanUrn

Setting up this application will require the following.

1. Clone the repo.
2. Copy UrbanUrn/settings.py.dist to UrbanUrn/settings.py
3. Go to "database" tag, make changes int Postgres database connection string.

# Python environment setup

- Install the following python packages:
```
pip install alembic
pip install pyjwt
pip install cryptography
pip install jsonschema
```

- Modify the database connection URL in alembic.ini and env.py
- Run the following command to migrate the tables to your database
```
alembic upgrade HEAD
```