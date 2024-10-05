from pydantic import BaseModel, Field
from bson import ObjectId
from datetime import datetime, timezone


class PyObjectId(ObjectId):
    """
    A custom Pydantic-compatible ObjectId field to handle MongoDB's ObjectId.

    Provides:
    - Validation: Ensures that the ObjectId is valid.
    - Schema modification: Adjusts OpenAPI schema to treat the field as a string.
    """


    @classmethod
    def __get_validators__(cls):
        """Yield the validator for ObjectId to be used by Pydantic."""
        yield cls.validate

    @classmethod
    def validate(cls, v):
        """
        Validate that the input is a valid ObjectId.

        Args:
            v: The value to validate.

        Returns:
            A valid ObjectId.

        Raises:
            ValueError: If the ObjectId is invalid.
        """
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        """Modify the field schema to represent ObjectId as a string."""
        field_schema.update(type="string")



class UserDB(BaseModel):
    """
    A Pydantic model representing a user in the database.
    """
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    email: str = Field(unique=True)
    hashed_password: str
    username: str = Field(unique=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


    class Config:
        """
        Configuration for the Pydantic model.
        
        Settings:
            allow_population_by_field_name: Allows the model to populate fields using the field's alias.
            arbitrary_types_allowed: Allows the use of arbitrary Python types like ObjectId.
            json_encoders: Custom JSON encoder for ObjectId to convert it to a string.
        """
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}



