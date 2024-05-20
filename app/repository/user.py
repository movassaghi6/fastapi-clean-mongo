from pymongo import MongoClient

from app.core.config import MONGO_COLLECTION_USERS
from app.repository.base import BaseRepository
from app.model.user import User

from fastapi.encoders import jsonable_encoder



class UserRepository(BaseRepository):
    def __init__(self, mongo: MongoClient):
        self._mongo = mongo
        super().__init__(mongo)

    def create(self, model: User, collection: MONGO_COLLECTION_USERS) -> User:
        model_in_json = jsonable_encoder(model)
        new_model = self.database[collection].insert_one(document=model_in_json)
        created_model = self.database[collection].find_one(
            {"_id": new_model.inserted_id}
        )
        return User(**created_model)





