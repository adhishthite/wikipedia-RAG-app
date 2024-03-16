import os

import elasticapm

from .database import MongoDB


@elasticapm.capture_span()
def healthcheck():
    """
    Simple healthcheck function that returns a byte string.
    """
    return b'Hello, World!'


@elasticapm.capture_span()
def get_mongo_status():
    """
    Retrieves the current MongoDB connection information.

    Returns:
        dict: A dictionary containing the collection name, database name, host, and port.
    """
    MONGO_URL = os.environ.get("MONGO_URL")
    mongo_db = MongoDB(mongo_url=MONGO_URL, database_name="admin")
    return mongo_db.ping()
