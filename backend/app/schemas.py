from pydantic import BaseModel
from datetime import datetime

class ReviewResponse(BaseModel):
    id: int
    contact_number: str
    user_name: str
    product_name: str
    product_review: str
    created_at: datetime

    class ConfigDict:
        from_attributes = True
