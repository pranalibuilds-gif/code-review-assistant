from enum import Enum

class SubmissionType(str, Enum):
    PASTE = "PASTE"
    UPLOAD = "UPLOAD"
    GITHUB = "GITHUB"

class ReviewStatus(str, Enum):
    QUEUED = "QUEUED"
    VALIDATING = "VALIDATING"
    STATIC_ANALYSIS = "STATIC_ANALYSIS"
    AI_ANALYSIS = "AI_ANALYSIS"
    SYNTHESIS = "SYNTHESIS"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    PARTIAL_SUCCESS = "PARTIAL_SUCCESS"

class Severity(str, Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
    INFO = "INFO"

class FindingSource(str, Enum):
    PYLINT = "PYLINT"
    BANDIT = "BANDIT"
    RADON = "RADON"
    AI = "AI"
