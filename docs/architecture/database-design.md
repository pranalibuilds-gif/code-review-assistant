# Database Design

CodeSage uses a relational model optimized for project-level grouping and historical trend tracking.

## Entity Relationship Diagram

```mermaid
erDiagram
    USER ||--o{ PROJECT : owns
    PROJECT ||--o{ SUBMISSION : has
    SUBMISSION ||--|| REVIEW : produces
    REVIEW ||--o{ FINDING : contains
    REVIEW ||--o{ METRIC : has
    REVIEW ||--o{ ARTIFACT : generates
    USER ||--o{ AUDIT_LOG : triggers

    USER {
        uuid id PK
        string email UK
        string username
        string password_hash
        string role
        boolean is_active
    }

    PROJECT {
        uuid id PK
        uuid owner_id FK
        string name
        string default_language
    }

    SUBMISSION {
        uuid id PK
        uuid project_id FK
        string type
        string status
        string github_url
    }

    REVIEW {
        uuid id PK
        uuid submission_id FK
        float overall_score
        string grade
        text summary
        json cached_report
    }

    FINDING {
        uuid id PK
        uuid review_id FK
        string source
        string severity
        string title
        text description
        string file_path
        integer line
    }

    METRIC {
        uuid id PK
        uuid review_id FK
        string name
        float value
    }

    ARTIFACT {
        uuid id PK
        uuid review_id FK
        string type
        string path
    }
```

## Optimization Strategies

- **UUID Primary Keys:** Used for all tables to prevent ID enumeration and simplify distributed scaling.
- **Indexes:** 
  - `ix_users_email`
  - `ix_projects_owner_id`
  - `ix_findings_review_id`
- **Cached Report:** The `Review` table stores a complete JSON snapshot of the aggregated analysis. This allows the Frontend to render complex dashboards and reports with a single indexed primary key lookup, avoiding heavy joins during read operations.
