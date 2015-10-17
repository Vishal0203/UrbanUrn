# Urban Urn

Setting up this application will require the following.

- Clone the repo.
- Copy UrbanUrn/settings.py.dist to UrbanUrn/settings.py
- Go to "database" tag, make changes int Postgres database connection string.

### Python environment setup

- Install the following python packages:
```
pip install alembic
pip install pyjwt
pip install cryptography
pip install jsonschema
```

### Database setup and load data

- Modify the database connection URL in alembic.ini and env.py
- Run the following commands to migrate the tables to your database.
a) Run from project root folder 
```
python manage.py migrate
```
b) Run from `<root_folder>\database`
```
alembic upgrade HEAD
```

- To load sample data in the database. Go to project root folder and run the a manage.py command
```
python manage.py loaddata database\fixtures\sample_fixture.json
```

