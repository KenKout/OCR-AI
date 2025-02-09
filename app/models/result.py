from datetime import datetime
from typing import Optional

import bson
from loguru import logger
from pydantic import BaseModel, Field

from app.internal.db import result_collection


class ResultModel(BaseModel):
    id: Optional[bson.ObjectId] = Field(default=None)
    pdf_id: str
    page: int
    text: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        arbitrary_types_allowed = True
        json_schema_extra = {
            "example": {
                "pdf_id": "60f1b3b3b3b3b3b3b3b3b3b3",
                "page": 1,
                "text": "This is a sample text",
                "created_at": "2024-01-01T00:00:00"
            }
        }


class ResultTables:
    async def insert_result(self, result: ResultModel) -> Optional[dict]:
        result_dict = result.model_dump(exclude_none=True)
        try:
            result = await result_collection.insert_one(result_dict)
            result_id = str(result.inserted_id)
            return {"_id": result_id, **result_dict}
        except Exception as e:
            logger.error(f"An error occurred: {e}")
            return None

    async def get_result_by_pdf_id(self, pdf_id: str) -> Optional[dict]:
        result = await result_collection.find({"pdf_id": pdf_id}).sort("page", 1).to_list(length=None)
        return result
