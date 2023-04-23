from .postgresql_db import PostgresDB
from setting import DATABASE_URL

if DATABASE_URL:
    db = PostgresDB()
else:
    print("Database url can't be found, running without Database")
    db = None
__all__ = [db]
