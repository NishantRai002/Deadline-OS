"""
DeadlineOS — Dashboard route
Author (Backend): Nishant Kumar
"""

from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.db import query

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/")
@login_required
def index():
    """
    Student dashboard: personalized announcements + upcoming deadlines.
    Faculty/admin see all recent items instead.
    """
    if current_user.is_student:
        announcements = query(
            """SELECT a.announcement_id, a.title, a.body, a.created_at,
                      u.full_name AS author
               FROM Announcements a
               JOIN Users u ON u.user_id = a.created_by
               WHERE a.is_active = 1
                 AND (a.target_program = ? OR a.target_program IS NULL)
                 AND (a.target_semester = ? OR a.target_semester IS NULL)
                 AND (a.target_section = ? OR a.target_section IS NULL)
               ORDER BY a.created_at DESC""",
            (current_user.program, current_user.semester, current_user.section),
        )

        deadlines = query(
            """SELECT d.deadline_id, d.title, d.due_date, d.course_name,
                      st.status
               FROM Deadlines d
               LEFT JOIN StudentTasks st
                      ON st.deadline_id = d.deadline_id AND st.student_id = ?
               WHERE d.is_active = 1
                 AND (d.target_program = ? OR d.target_program IS NULL)
                 AND (d.target_semester = ? OR d.target_semester IS NULL)
               ORDER BY d.due_date ASC""",
            (current_user.id, current_user.program, current_user.semester),
        )
    else:
        announcements = query(
            """SELECT a.announcement_id, a.title, a.body, a.created_at,
                      u.full_name AS author
               FROM Announcements a JOIN Users u ON u.user_id = a.created_by
               WHERE a.is_active = 1
               ORDER BY a.created_at DESC"""
        )
        deadlines = query(
            """SELECT deadline_id, title, due_date, course_name, NULL AS status
               FROM Deadlines WHERE is_active = 1 ORDER BY due_date ASC"""
        )

    return render_template(
        "dashboard/index.html",
        announcements=announcements,
        deadlines=deadlines,
    )
