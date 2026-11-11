-- ============================================================
-- DeadlineOS — Sample / Seed Data
-- Author (Backend): Nishant Kumar
-- Run AFTER schema.sql to populate test data.
-- ============================================================

-- Admin user (password: Admin@123)
INSERT INTO Users (email, full_name, password_hash, role)
VALUES ('admin@university.edu', 'Admin User',
        'scrypt:32768:8:1$placeholder$hash', 'admin');

-- Faculty user (password: Faculty@123)
INSERT INTO Users (email, full_name, password_hash, role)
VALUES ('faculty@university.edu', 'Prof. Sharma',
        'scrypt:32768:8:1$placeholder$hash', 'faculty');

-- Student user (password: Student@123)
INSERT INTO Users (email, full_name, password_hash, role, program, semester, section)
VALUES ('student@university.edu', 'Ravi Verma',
        'scrypt:32768:8:1$placeholder$hash', 'student', 'BCA', '5', 'A');

-- Sample announcement (all students)
INSERT INTO Announcements (title, body, created_by, is_active)
VALUES ('Welcome to DeadlineOS',
        'This platform will help you track all your academic deadlines in one place.',
        1, 1);

-- Sample deadline for BCA Semester 5
INSERT INTO Deadlines (title, course_name, due_date, created_by, target_program, target_semester)
VALUES ('DBMS Lab Assignment 2', 'Database Management Systems',
        DATEADD(DAY, 7, SYSUTCDATETIME()), 2, 'BCA', '5');

INSERT INTO Deadlines (title, course_name, due_date, created_by, target_program, target_semester)
VALUES ('Cloud Computing Quiz 1', 'Cloud Computing',
        DATEADD(DAY, 3, SYSUTCDATETIME()), 2, 'BCA', '5');
