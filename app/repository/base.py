from pymongo import MongoClient
from core.config import MONGO_DATABASE



class BaseRepository:
    """
    A base repository class that provides access to the MongoDB database.

    This class is intended to be inherited by specific repository classes
    that need to interact with MongoDB collections.

    Attributes:
        _mongo (MongoClient): The MongoDB client instance used to interact with the database.
        database (Database): The MongoDB database instance.
    """
    def __init__(self, mongo: MongoClient):
        self._mongo= mongo
        self.database = self._mongo[MONGO_DATABASE]


    @property
    def mongo_client(self) -> MongoClient:
        """
        Property to access the MongoDB client instance.

        Returns:
            MongoClient: The MongoDB client instance.
        """
        return self._mongo
