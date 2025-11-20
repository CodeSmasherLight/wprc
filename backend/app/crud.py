from sqlalchemy.orm import Session
from .models import Review

def create_review(db: Session, contact_number, user_name, product_name, product_review):
    review = Review(
        contact_number=contact_number,
        user_name=user_name,
        product_name=product_name,
        product_review=product_review
    )
    db.add(review)
    db.commit()
    db.refresh(review)
    return review

def get_reviews(db: Session):
    return db.query(Review).order_by(Review.created_at.desc()).all()
