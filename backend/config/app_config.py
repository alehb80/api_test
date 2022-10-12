import os
import pathlib
from enum import Enum

################################################################################################
RESOURCES = pathlib.Path(__file__).parent.absolute().parent / "resources"

################################################################################################
# MONGODB MOCKUP
MONGO_HOST = "localhost"
MONGO_PORT = 27017
MONGO_DB = "test_tecnico"
MONGO_USERNAME = ""
MONGO_PASSWORD = ""
MONGO_COLL = "stats"

MONGODB_URL = os.environ.get("MONGODB_URL")

################################################################################################
# WS API CONFIGS
API_URL = "/api/v1/"
API_KEY = "BigProfiles-API"


class ApiEndpoint(Enum):
    API_ENDPOINT_INGEST = "ingest"
    API_ENDPOINT_RETRIEVE = "retrieve"
