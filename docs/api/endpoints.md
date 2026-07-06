# API Reference

CodeSage exposes a RESTful API versioned under `/api/v1/`.

## Response Standard

All responses follow this structure:

```json
{
  "success": true,
  "data": { ... },
  "request_id": "4c8d3c12"
}
```

---

## 🔐 Authentication

### `POST /auth/register`
- **Purpose:** Create a new user account.
- **Body:** `email, username, password, full_name`.

### `POST /auth/login`
- **Purpose:** Authenticate and receive a JWT.
- **Body:** `email, password`.
- **Returns:** `access_token, token_type`.

### `GET /auth/me`
- **Purpose:** Retrieve current user profile.
- **Auth:** Required (JWT).

---

## 📥 Submissions

### `POST /submissions/paste`
- **Purpose:** Submit raw text code for analysis.
- **Body:** `project_id, code, filename`.

### `POST /submissions/upload`
- **Purpose:** Submit a ZIP project.
- **Type:** Multipart/form-data.

### `POST /submissions/github`
- **Purpose:** Submit a public repository URL.
- **Body:** `project_id, github_url`.

---

## 📊 Dashboard & Reviews

### `GET /dashboard/summary`
- **Purpose:** Aggregated stats for the user (Trend, Severity, Averages).

### `GET /reviews/{id}`
- **Purpose:** Retrieve the full canonical report (cached).

### `GET /reviews/{id}/export/{format}`
- **Purpose:** Download PDF, Markdown, or JSON reports.
- **Formats:** `pdf`, `md`, `json`.

---

## 🛡️ Admin

### `GET /admin/health`
- **Purpose:** Real-time health of API, DB, Ollama, and Disk.
- **Role:** Admin only.

### `GET /admin/jobs`
- **Purpose:** Active background tasks monitoring.

### `GET /admin/audit`
- **Purpose:** Immutable audit log retrieval.
