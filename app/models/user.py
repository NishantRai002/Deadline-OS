"""
DeadlineOS — User model (Flask-Login integration)
Author (Backend): Nishant Kumar
"""

from flask_login import UserMixin
from app.extensions import login_manager
from app.db import query


class User(UserMixin):
    """Wraps a database Users row for Flask-Login."""

    def __init__(self, row):
        self.id = row[0]            # user_id
        self.email = row[1]
        self.full_name = row[2]
        self.role = row[3]          # 'student' | 'faculty' | 'admin'
        self.program = row[4]
        self.semester = row[5]
        self.section = row[6]

    @property
    def is_admin(self):
        return self.role == "admin"

    @property
    def is_faculty(self):
        return self.role in ("faculty", "admin")

    @property
    def is_student(self):
        return self.role == "student"


@login_manager.user_loader
def load_user(user_id):
    rows = query(
        "SELECT user_id, email, full_name, role, program, semester, section "
        "FROM Users WHERE user_id = ?",
        (user_id,),
    )
    if rows:
        return User(rows[0])
    return None
