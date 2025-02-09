from datetime import datetime
from typing import Optional

import bson
from loguru import logger
from pydantic import BaseModel, Field

from app.internal.db import pdf_collection


class PDFModel(BaseModel):
    id: Optional[bson.ObjectId] = Field(default=None)
    pdf_id: str
    pages: int
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Adjust metadata for Pydantic V2
    class Config:
        arbitrary_types_allowed = True
        json_schema_extra = {
            "example": {
                "pdf_id": "60f1b3b3b3b3b3b3b3b3b3b3",
                "pages": 10,
                "created_at": "2024-01-01T00:00:00"
            }
        }


class PDFTables:
    async def insert_pdf(self, pdf: PDFModel) -> Optional[dict]:
        pdf_dict = pdf.model_dump(exclude_none=True)
        try:
            result = await pdf_collection.insert_one(pdf_dict)
            pdf_id = str(result.inserted_id)
            return {"_id": pdf_id, **pdf_dict}
        except Exception as e:
            logger.error(f"An error occurred: {e}")
            return None

    async def get_pdf_by_id(self, pdf_id: str) -> Optional[dict]:
        pdf = await pdf_collection.find_one({"pdf_id": pdf_id})
        return pdf
