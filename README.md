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

1. Create role and database in postgres from create_db.sql

2. Run below command in your terminal for migration.

   ```Python3
     python manage.py db upgrade
   ```

   or Run below command in your terminal if you wish to use my sample data for the database.

   ```Shell
     psql sudhan_flask --username=sudhan_flask --host=127.0.0.1 < dummy.db
   ```

3. Run below command in your terminal .

   ```python3
     export FLASK_APP=run.py
     flask run
   ```

4. Open any browser and go to http://localhost:5000/

5. Delete database and role in postgres using drop_db.sql
