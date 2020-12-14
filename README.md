# flask-toy-project

An online Q/A platform built in Flask.

## Technology used

* Backend:  Flask

* Frontend: Html, CSS

* Database: PostgreSQL

## Prerequisites

1. Download all the files in your local computer
2. Cd to the directory where the downloaded files are located
3. Install all the dependencies from requirements.txt file

## Get Started

* Create role and database in postgres from create_db.sql

* Run below command in your terminal to create tables.

```Python3
  flask db upgrade
```

* Run below command in your terminal if you wish to use my sample data for the database.

```Shell
  pg_dump sudhan_flask --username=sudhan_flask --host=127.0.0.1 < dummy.db
```

* Run below command in your terminal .

```Python3
  python run.py
```

* Open any browser and go to http://localhost:5000/

* Delete database and role in postgres using drop_db.sql
