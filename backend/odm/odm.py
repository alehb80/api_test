from typing import Dict

from pymongo import MongoClient

from backend.config.app_config import MONGODB_URL


class DocumentODM:

    def __init__(
            self,
            db: str,
            collection: str
    ):
        self.db = db
        self.client = MongoClient(MONGODB_URL)
        self.collection = self.client.get_database(self.db).get_collection(collection)

    ############## GET ###############

    def get_many_by_query(
            self,
            query: Dict = None,
            projection: Dict = None,
    ):
        """
        List of Documents obtained from the given query q in input.
        :param query: The mongo query that will be run on the collection
        :param projection: Dictionary of the fields used for filter the get operation once obtained the Documents.
        :return: The List of Documents obtained by query, filtered by parameters
        """
        return list(self.collection.find(filter=query, projection=projection, ))

    ################ SAVE ##################
    def save(
            self,
            elem: Dict
    ):
        """
        Function that save a document in the collection. If the document is already in collection, it will raise an Exception.
        :param elem: Document that will be saved in the collection.
        :return: A pymongo.results.InsertOneResult instance. Using '.inserted_id' on the instance will give back the ObjectId of the element saved.
        """
        return self.collection.insert_one(document=elem)
