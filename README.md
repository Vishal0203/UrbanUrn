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

### Setting up git-flow

- [Follow the link] (https://github.com/nvie/gitflow/wiki/Windows) and go through the steps defined under `MSysGit`
- Briefly, download the files from the link provided in above document.
- After installing copy `getopt.exe`, `libiconv2.dll` and `libintl3.dll` files from install location (for example: `C:\Program Files (x86)\GnuWin32\bin`)
- Clone gitflow inside your already existing Git installed location (For example: `C:\Program Files (x86)\Git`). Cloning URL's are provided in the link.
- Run `C:\Program Files (x86)\Git\gitflow> contrib\msysgit-install.cmd` from CMD as an administrator.
- Create a symbolic link using git bash to access git flow from anywhere. Run `ln -s /C/Program Files (x86)/Git/gitflow/git-flow git-flow` inside git bash.