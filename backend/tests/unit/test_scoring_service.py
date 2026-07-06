import pytest
from app.services.aggregation.scoring_service import ScoringService
from app.services.aggregation.dto import FindingDTO, MetricDTO
from app.models.enums import Severity, FindingSource

def test_calculate_category_score_perfect():
    findings = []
    score = ScoringService._calculate_category_score(findings)
    assert score == 100.0

def test_calculate_category_score_penalties():
    findings = [
        FindingDTO(source=FindingSource.PYLINT, severity=Severity.HIGH, title="Test 1"), # -10
        FindingDTO(source=FindingSource.PYLINT, severity=Severity.MEDIUM, title="Test 2"), # -5
    ]
    score = ScoringService._calculate_category_score(findings)
    assert score == 85.0

def test_calculate_category_score_critical():
    findings = [
        FindingDTO(source=FindingSource.BANDIT, severity=Severity.CRITICAL, title="Test 1"), # -20
    ]
    score = ScoringService._calculate_category_score(findings)
    assert score == 80.0

def test_calculate_category_score_clamped():
    findings = [FindingDTO(source=FindingSource.PYLINT, severity=Severity.CRITICAL, title="T")] * 10
    score = ScoringService._calculate_category_score(findings)
    assert score == 0.0

def test_get_grade():
    assert ScoringService.get_grade(98) == "A+"
    assert ScoringService.get_grade(91) == "A-"
    assert ScoringService.get_grade(85) == "B"
    assert ScoringService.get_grade(75) == "C"
    assert ScoringService.get_grade(50) == "F"

def test_calculate_overall_score_weighted():
    # Security: 40% (1 Critical = 80) -> 32
    # Reliability: 25% (1 High = 90) -> 22.5
    # Maintainability: 20% (100) -> 20
    # AI: 15% (100) -> 15
    # Total: 32 + 22.5 + 20 + 15 = 89.5
    findings = [
        FindingDTO(source=FindingSource.BANDIT, severity=Severity.CRITICAL, title="Sec"),
        FindingDTO(source=FindingSource.PYLINT, severity=Severity.HIGH, title="Rel"),
    ]
    metrics = [MetricDTO(metric_name="Maintainability Index", metric_value=100.0)]

    score = ScoringService.calculate_overall_score(findings, metrics)
    assert score == 89.5
