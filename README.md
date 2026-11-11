# 🕐 DeadlineOS — Personalized Campus Deadline & Notice Platform

> A secure web platform that organizes fragmented campus notices and deadlines into personalized, actionable information for students.

---

## 👥 Team & Contributions

| Team Member | Role | Contribution |
|---|---|---|
| **Nishant Kumar** | Backend Developer | Flask app factory, REST APIs, Azure SQL schema, Auth (login/register/logout), Blob Storage integration, audit logging, role-based access control |
| **Yuvraj** | Frontend Developer | HTML/CSS/JS templates, Bootstrap 5 UI, dashboard, deadlines page with live status update (AJAX), announcements pages, admin panel, responsive design |

> Every file in this repository contains an `Author` comment indicating who built it.

---

## 🚀 Features

| Feature | Description |
|---|---|
| **Personalized Dashboard** | Shows only announcements and deadlines relevant to a student's program, semester, and section |
| **Announcement Publishing** | Faculty/admin can post notices with optional file attachments (stored in Azure Blob Storage) |
| **Deadline Tracking** | Students mark deadlines as *Pending → In Progress → Completed* via live AJAX updates |
| **Document Attachments** | PDFs and files stored securely on Azure Blob Storage with time-limited SAS URLs |
| **Role-Based Access** | Three roles: `student`, `faculty`, `admin` — enforced server-side on every route |
| **Audit Logs** | Every login, logout is recorded; admin can view the full log |
| **Admin Panel** | User management and platform statistics |

---

## 🗂️ Project Structure

```
DeadlineOS/
├── run.py                        # Entry point (Nishant)
├── requirements.txt              # Python dependencies (Nishant)
├── .env.example                  # Env variable template (Nishant)
├── .gitignore
│
├── app/
│   ├── __init__.py               # App factory (Nishant)
│   ├── extensions.py             # Flask extensions (Nishant)
│   ├── db.py                     # Azure SQL helper (Nishant)
│   ├── blob_storage.py           # Azure Blob Storage (Nishant)
│   │
│   ├── models/
│   │   └── user.py               # User model + Flask-Login (Nishant)
│   │
│   ├── routes/
│   │   ├── auth.py               # Register / Login / Logout (Nishant)
│   │   ├── dashboard.py          # Personalized dashboard (Nishant)
│   │   ├── announcements.py      # CRUD for notices (Nishant)
│   │   ├── deadlines.py          # CRUD + status AJAX API (Nishant)
│   │   └── admin.py              # Admin panel routes (Nishant)
│   │
│   ├── templates/
│   │   ├── base.html             # Base layout + navbar (Yuvraj)
│   │   ├── auth/
│   │   │   ├── login.html        # Login page (Yuvraj)
│   │   │   └── register.html     # Registration page (Yuvraj)
│   │   ├── dashboard/
│   │   │   └── index.html        # Dashboard UI (Yuvraj)
│   │   ├── announcements/
│   │   │   ├── list.html         # Notice list (Yuvraj)
│   │   │   ├── detail.html       # Notice detail (Yuvraj)
│   │   │   └── create.html       # Post notice form (Yuvraj)
│   │   ├── deadlines/
│   │   │   ├── list.html         # Deadlines with status update (Yuvraj)
│   │   │   └── create.html       # Add deadline form (Yuvraj)
│   │   └── admin/
│   │       ├── index.html        # Admin panel (Yuvraj)
│   │       └── audit_logs.html   # Audit log view (Yuvraj)
│   │
│   └── static/
│       ├── css/main.css          # Custom styles (Yuvraj)
│       └── js/main.js            # Client-side logic (Yuvraj)
│
└── database/
    ├── schema.sql                # Full Azure SQL schema (Nishant)
    └── seed.sql                  # Sample data (Nishant)
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **Backend** | Python 3.11+, Flask 3, Flask-Login, Werkzeug |
| **Database** | Azure SQL Database (pyodbc) |
| **File Storage** | Azure Blob Storage |
| **Frontend** | HTML5, CSS3, Bootstrap 5, Vanilla JS |
| **Hosting** | Azure App Service |
| **Version Control** | Git / GitHub |

---

## ⚙️ Local Setup

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/DeadlineOS.git
cd DeadlineOS
```

### 2. Create a virtual environment
```bash
python -m venv venv
venv\Scripts\activate      # Windows
# or: source venv/bin/activate  (Mac/Linux)
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment variables
```bash
copy .env.example .env
# Edit .env and fill in your Azure SQL and Blob Storage credentials
```

### 5. Set up the database
Run `database/schema.sql` and then `database/seed.sql` against your Azure SQL Database using Azure Data Studio or the Azure portal query editor.

### 6. Run the app
```bash
python run.py
```

Open **http://localhost:5000** in your browser.

---

## 🔐 Security Measures

- **Password hashing** via Werkzeug `generate_password_hash` (scrypt)
- **Role-based access control** enforced server-side on every route and API endpoint
- **SQL injection protection** via parameterised pyodbc queries (never string interpolation)
- **XSS protection** via Jinja2 auto-escaping
- **Secrets outside source control** — `.env` is in `.gitignore`; only `.env.example` is committed
- **Azure Blob Storage** — blobs are private; access via short-lived SAS URLs only
- **Azure SQL** — firewall rules restrict access to the App Service IP

---

## 📊 Database Schema (Summary)

```
Users            → user_id, email, full_name, password_hash, role, program, semester, section
Announcements    → announcement_id, title, body, created_by(FK), target_*, is_active
Deadlines        → deadline_id, title, course_name, due_date, created_by(FK), target_*, is_active
StudentTasks     → task_id, student_id(FK), deadline_id(FK), status   [UNIQUE(student, deadline)]
Attachments      → attachment_id, announcement_id(FK), deadline_id(FK), blob_name, original_name
AuditLogs        → log_id, user_id(FK), action, created_at

VIEW: vw_UpcomingDeadlines  — joins Deadlines + StudentTasks for the dashboard query
```

---

## 📋 Deliverables Checklist

- [x] Working Flask application with all core features
- [x] Azure SQL Database schema (`database/schema.sql`)
- [x] Azure Blob Storage integration
- [x] Role-based access control (student / faculty / admin)
- [x] Personalized filtering by program, semester, section
- [x] Live deadline status update (AJAX)
- [x] Audit logs
- [x] Responsive Bootstrap 5 UI
- [x] Git repository with meaningful commit history
- [ ] Deployed to Azure App Service (live URL — add after deployment)
- [ ] Project report
- [ ] Power BI analytics report

---

## 🌐 Live URL

> _Add your Azure App Service URL here after deployment_

---

## 📄 License

This project is submitted as part of an academic assignment. All rights reserved by the team members.
