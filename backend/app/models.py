from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, text
from .database import Base

class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, nullable=False)
    contact_number = Column(String, nullable=False)
    user_name = Column(String, nullable=False)
    product_name = Column(String, nullable=False)
    product_review = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)