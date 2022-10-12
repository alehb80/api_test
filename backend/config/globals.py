from backend.config.app_config import MONGO_DB, MONGO_COLL
from backend.odm.odm import DocumentODM

odm = DocumentODM(
    db=MONGO_DB,
    collection=MONGO_COLL
)
