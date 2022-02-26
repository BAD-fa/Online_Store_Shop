from pydantic import BaseModel, Field
from setting import PyObjectId,ObjectId



class DiscountCode(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    user_id: int = Field(...)
    expire_time: str = Field(...)
    code: str = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "user_id": "1",
                "expire_time": "5",
                "code": "4bb96796-93ad-11ec-b296-cda1ab98e3d2",
            }
        }