import pathlib
from enum import Enum

from backend.dao.dao import DocumentDAO

################################################################################################
RESOURCES = pathlib.Path(__file__).parent.absolute().parent / "resources"

################################################################################################
# MONGODB MOCKUP
MONGO_HOST = "localhost"  # 44.242.171.0 - 68.183.66.3
MONGO_PORT = 27017
MONGO_DB = "test_tecnico"
MONGO_USERNAME = ""
MONGO_PASSWORD = ""
MONGO_COLL = "stats"

################################################################################################
# WS API CONFIGS
API_URL = "/api/v1/"
API_KEY = "BigProfiles-API"


class ApiEndpoint(Enum):
    API_ENDPOINT_INGEST = "ingest"
    API_ENDPOINT_RETRIEVE = "retrieve"


dao = DocumentDAO(
    host=MONGO_HOST,
    port=MONGO_PORT,
    db=MONGO_DB,
    username=MONGO_USERNAME,
    password=MONGO_PASSWORD,
    collection=MONGO_COLL
)
