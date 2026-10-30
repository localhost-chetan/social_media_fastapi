from psycopg.rows import dict_row
from psycopg_pool import ConnectionPool
from social_media_fastapi.utils import get_env_key


pool = ConnectionPool(
    conninfo=get_env_key(key_name="DATABASE_URL"),
    kwargs={
        "row_factory": dict_row,  # preserves your existing dictionary-style query results
        "autocommit": True
    },
    min_size=1,
    max_size=10,
    open=False
)
