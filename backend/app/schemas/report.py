from typing import Optional, Any
from uuid import UUID
from pydantic import BaseModel
from .submission import SubmissionResponse
from app.services.aggregation.dto import CanonicalReviewReport

class ReviewDetailedResponse(BaseModel):
    success: bool = True
    data: CanonicalReviewReport
    request_id: Optional[str] = None
