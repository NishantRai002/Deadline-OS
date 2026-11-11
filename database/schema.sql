-- ============================================================
-- DeadlineOS — Azure SQL Database Schema
-- Author (Backend): Nishant Kumar
-- Run this script once against your Azure SQL Database to
-- set up all tables, indexes, and a view.
-- ============================================================

-- ── Users ────────────────────────────────────────────────────
CREATE TABLE Users (
    user_id       INT IDENTITY(1,1) PRIMARY KEY,
    email         NVARCHAR(255) NOT NULL UNIQUE,
    full_name     NVARCHAR(255) NOT NULL,
    password_hash NVARCHAR(512) NOT NULL,
    role          NVARCHAR(20)  NOT NULL DEFAULT 'student'
                  CHECK (role IN ('student','faculty','admin')),
    program       NVARCHAR(100),
    semester      NVARCHAR(10),
    section       NVARCHAR(10),
    created_at    DATETIME2     NOT NULL DEFAULT SYSUTCDATETIME()
);

-- ── Announcements ─────────────────────────────────────────────
CREATE TABLE Announcements (
    announcement_id  INT IDENTITY(1,1) PRIMARY KEY,
    title            NVARCHAR(300)  NOT NULL,
    body             NVARCHAR(MAX)  NOT NULL,
    created_by       INT            NOT NULL REFERENCES Users(user_id),
    target_program   NVARCHAR(100),   -- NULL = all programs
    target_semester  NVARCHAR(10),    -- NULL = all semesters
    target_section   NVARCHAR(10),    -- NULL = all sections
    is_active        BIT            NOT NULL DEFAULT 1,
    created_at       DATETIME2      NOT NULL DEFAULT SYSUTCDATETIME()
);

-- ── Deadlines ─────────────────────────────────────────────────
CREATE TABLE Deadlines (
    deadline_id      INT IDENTITY(1,1) PRIMARY KEY,
    title            NVARCHAR(300) NOT NULL,
    course_name      NVARCHAR(200),
    due_date         DATETIME2     NOT NULL,
    created_by       INT           NOT NULL REFERENCES Users(user_id),
    target_program   NVARCHAR(100),
    target_semester  NVARCHAR(10),
    is_active        BIT           NOT NULL DEFAULT 1,
    created_at       DATETIME2     NOT NULL DEFAULT SYSUTCDATETIME()
);

-- ── StudentTasks (per-student tracking) ───────────────────────
CREATE TABLE StudentTasks (
    task_id      INT IDENTITY(1,1) PRIMARY KEY,
    student_id   INT          NOT NULL REFERENCES Users(user_id),
    deadline_id  INT          NOT NULL REFERENCES Deadlines(deadline_id),
    status       NVARCHAR(20) NOT NULL DEFAULT 'pending'
                 CHECK (status IN ('pending','in_progress','completed')),
    updated_at   DATETIME2    NOT NULL DEFAULT SYSUTCDATETIME(),
    CONSTRAINT uq_student_deadline UNIQUE (student_id, deadline_id)
);

-- ── Attachments ───────────────────────────────────────────────
CREATE TABLE Attachments (
    attachment_id    INT IDENTITY(1,1) PRIMARY KEY,
    announcement_id  INT           REFERENCES Announcements(announcement_id),
    deadline_id      INT           REFERENCES Deadlines(deadline_id),
    blob_name        NVARCHAR(500) NOT NULL,  -- key in Azure Blob Storage
    original_name    NVARCHAR(300) NOT NULL,
    uploaded_at      DATETIME2     NOT NULL DEFAULT SYSUTCDATETIME()
);

-- ── AuditLogs ─────────────────────────────────────────────────
CREATE TABLE AuditLogs (
    log_id      INT IDENTITY(1,1) PRIMARY KEY,
    user_id     INT           NOT NULL REFERENCES Users(user_id),
    action      NVARCHAR(200) NOT NULL,
    created_at  DATETIME2     NOT NULL DEFAULT SYSUTCDATETIME()
);

-- ── Indexes ───────────────────────────────────────────────────
CREATE INDEX idx_ann_program_sem  ON Announcements(target_program, target_semester, is_active);
CREATE INDEX idx_dl_program_sem   ON Deadlines(target_program, target_semester, is_active);
CREATE INDEX idx_tasks_student    ON StudentTasks(student_id);
CREATE INDEX idx_audit_user       ON AuditLogs(user_id);

-- ── View: Upcoming deadlines with student status ──────────────
CREATE VIEW vw_UpcomingDeadlines AS
SELECT
    d.deadline_id,
    d.title,
    d.course_name,
    d.due_date,
    d.target_program,
    d.target_semester,
    st.student_id,
    ISNULL(st.status, 'pending') AS task_status
FROM Deadlines d
LEFT JOIN StudentTasks st ON st.deadline_id = d.deadline_id
WHERE d.is_active = 1
  AND d.due_date >= SYSUTCDATETIME();
GO
