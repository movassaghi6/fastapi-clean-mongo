import time
from typing import Any, Tuple

from pymongo import MongoClient

from app.core.config import MONGO_DATABASE


class BaseRepository:
    def __init__(self, mongo: MongoClient):
        self._mongo= mongo
        self.database = self._mongo[MONGO_DATABASE]


    @property
    def mongo_client(self) -> MongoClient:
        return self._mongo
