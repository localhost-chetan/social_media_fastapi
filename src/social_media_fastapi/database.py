from os import environ

from dotenv import load_dotenv
from psycopg.rows import dict_row
from psycopg_pool import ConnectionPool

load_dotenv()


pool = ConnectionPool(
    kwargs={
        "host": environ['POSTGRES_HOST'],
        "port": environ['POSTGRES_PORT'],
        "dbname": environ['POSTGRES_DB'],
        "user": environ['POSTGRES_USER'],
        "password": environ['POSTGRES_PASSWORD'],
        "row_factory": dict_row,  # preserves your existing dictionary-style query results
        "autocommit": True
    },
    min_size=1,
    max_size=10,
    open=False
)
