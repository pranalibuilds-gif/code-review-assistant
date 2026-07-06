import random
from typing import Dict, List
from app.models.project import Project

PROJECT_TEMPLATES = [
    {"name": "Cloud Governance Hub", "description": "Enterprise policy engine for cloud resource compliance."},
    {"name": "Payments Gateway", "description": "Secure transaction core for omnichannel payments."},
    {"name": "Inventory Forecasting", "description": "Predictive inventory optimization for supply chain teams."},
    {"name": "Customer Insights API", "description": "Analytics pipeline for customer behavior and segmentation."},
    {"name": "AI Document Processor", "description": "Automated extraction and classification for enterprise documents."},
    {"name": "DevOps Pipeline", "description": "CI/CD orchestration and security validation workflows."},
    {"name": "Retail Catalog Service", "description": "Product data management platform for multi-region storefronts."},
    {"name": "Compliance Dashboard", "description": "Executive risk reporting with audit traceability."},
    {"name": "Data Lake Ingestion", "description": "High-throughput batch and streaming data capture."},
    {"name": "Identity Federation", "description": "Authentication and authorization for distributed teams."},
    {"name": "Mobile Experience", "description": "Cross-platform mobile backend with offline sync."},
    {"name": "Knowledge Graph", "description": "Semantic search and recommendation services for support."},
    {"name": "Release Automation", "description": "End-to-end release management with validation gates."},
    {"name": "Security Analytics", "description": "Threat detection and incident dashboard for SOC teams."},
    {"name": "Onboarding Portal", "description": "Employee onboarding workflow and user provisioning."},
    {"name": "ML Feature Store", "description": "Reusable feature management service for models."},
    {"name": "Fraud Detection", "description": "Real-time transaction anomaly detection engine."},
    {"name": "Support Chatbot", "description": "AI-powered help desk assistant with escalations."},
    {"name": "License Compliance", "description": "Open source license scanning and reporting."},
    {"name": "Telemetry Collector", "description": "Centralized observability for microservice health."},
]


def seed_projects(db, profile, users: Dict[str, object]) -> List[Project]:
    projects = []
    project_count = min(profile["project_count"], len(PROJECT_TEMPLATES))
    owner_pool = [u for key, u in users.items() if key not in {"admin_password", "demo_user_password"}]

    for idx in range(project_count):
        template = PROJECT_TEMPLATES[idx]
        owner = random.choice(owner_pool)
        existing = db.query(Project).filter(Project.name == template["name"]).first()
        if existing:
            projects.append(existing)
            continue

        project = Project(
            owner_id=owner.id,
            name=template["name"],
            description=template["description"],
            default_language="python",
        )
        db.add(project)
        db.flush()
        projects.append(project)

    return projects
