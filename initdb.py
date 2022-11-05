#Create database if it doesn't exist with psycopg2
from psycopg2 import connect, extensions, sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from psycopg2.errors import DuplicateDatabase
from psycopg2.extras import execute_values
import os

DB_NAME = "db"
DB_USER = "postgres"
DEFAULT_DB_NAME = "postgres"
DB_HOST = "localhost"
#Create database if it doesn't exist with psycopg2

conn = connect(
        dbname=DEFAULT_DB_NAME,
        user=DB_USER,
        host=DB_HOST,
        port=5432,
    )
conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
cur = conn.cursor()
try:
    cur.execute(sql.SQL("CREATE DATABASE {}".format(DB_NAME)))
except Exception as e:
    print(e)

cur.close()
conn.close()

#database imports
from app.models.database.database import Base
from app.models.database.database import Engine

#create models if they do not exist
Base.metadata.create_all(bind=Engine)