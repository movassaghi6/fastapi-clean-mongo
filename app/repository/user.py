from pymongo import MongoClient
import pymongo

from app.core.config import MONGO_COLLECTION_USERS
from app.repository.base import BaseRepository
from app.model.user import User
from pydantic import conint

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

    def get_by_id(self, collection: MONGO_COLLECTION_USERS, id: str) -> User :
        find_model = self.database[collection].find_one(
            {"_id": id}
        )

        return User(**find_model)

    def get_list(self,
                 collection: MONGO_COLLECTION_USERS,
                 sort_field: str = "created_at",
                 sort_order: int = pymongo.DESCENDING,
                 skip: conint(ge=0) = 0,
                 limit: conint(ge=5, multiple_of=5) = 10
                 ):

        users= self.database[collection].find({}).sort([(sort_field, sort_order)]).skip(skip).limit(limit)
        total = self.database[collection].count_documents(filter={})

        return [User(**user) for user in users], total

    def delete(self, collection: MONGO_COLLECTION_USERS, id: str) -> User:
        find_model = self.database[collection].find_one(
            {"_id": id}
        )
        delete_model = self.database[collection].delete_one(
            {"_id": id}
        )

        return User(**find_model)

    def update(self,
               collection: MONGO_COLLECTION_USERS,
               id: str,
               req):


        request_in_json = jsonable_encoder(req)

        update_model = self.database[collection].update_one(filter= {'_id': id}, update={ "$set": request_in_json } )
        updated_model = self.database[collection].find_one({"_id": id})

        return User(**updated_model)


