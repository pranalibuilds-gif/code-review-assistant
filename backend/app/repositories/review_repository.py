from typing import Optional
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.review import Review

class ReviewRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, review_id: UUID) -> Optional[Review]:
        return self.db.get(Review, review_id)

    def get_by_submission(self, submission_id: UUID) -> Optional[Review]:
        return self.db.execute(
            select(Review).where(Review.submission_id == submission_id)
        ).scalar_one_or_none()

    def create(self, review: Review) -> Review:
        self.db.add(review)
        self.db.commit()
        self.db.refresh(review)
        return review

    def update(self, review: Review) -> Review:
        self.db.commit()
        self.db.refresh(review)
        return review
