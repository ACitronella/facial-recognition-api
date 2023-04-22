import os
try:
    from dotenv import load_dotenv
    load_dotenv()
    del load_dotenv
except ImportError:
    pass

DATABASE_URL = os.getenv("DATABASE_URL", None)
assert DATABASE_URL != None

