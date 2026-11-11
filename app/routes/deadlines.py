"""
DeadlineOS — Deadline & task-tracking routes
Author (Backend): Nishant Kumar
"""

from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from app.db import query, execute

deadlines_bp = Blueprint("deadlines", __name__)

VALID_STATUSES = ("pending", "in_progress", "completed")


@deadlines_bp.route("/")
@login_required
def list_all():
    if current_user.is_student:
        rows = query(
            """SELECT d.deadline_id, d.title, d.due_date, d.course_name,
                      ISNULL(st.status, 'pending') AS status
               FROM Deadlines d
               LEFT JOIN StudentTasks st
                      ON st.deadline_id = d.deadline_id AND st.student_id = ?
               WHERE d.is_active = 1
                 AND (d.target_program = ? OR d.target_program IS NULL)
               ORDER BY d.due_date ASC""",
            (current_user.id, current_user.program),
        )
    else:
        rows = query(
            """SELECT deadline_id, title, due_date, course_name, NULL AS status
               FROM Deadlines WHERE is_active = 1 ORDER BY due_date ASC"""
        )
    return render_template("deadlines/list.html", deadlines=rows)


@deadlines_bp.route("/create", methods=["GET", "POST"])
@login_required
def create():
    if not current_user.is_faculty:
        flash("Only faculty or admins can create deadlines.", "danger")
        return redirect(url_for("deadlines.list_all"))

    if request.method == "POST":
        title = request.form.get("title", "").strip()
        course_name = request.form.get("course_name", "").strip()
        due_date = request.form.get("due_date", "").strip()
        target_program = request.form.get("target_program") or None
        target_semester = request.form.get("target_semester") or None

        if not title or not due_date:
            flash("Title and due date are required.", "danger")
            return render_template("deadlines/create.html")

        execute(
            """INSERT INTO Deadlines
                   (title, course_name, due_date, created_by, target_program, target_semester, is_active)
               VALUES (?, ?, ?, ?, ?, ?, 1)""",
            (title, course_name, due_date, current_user.id, target_program, target_semester),
        )
        flash("Deadline added.", "success")
        return redirect(url_for("deadlines.list_all"))

    return render_template("deadlines/create.html")


@deadlines_bp.route("/<int:deadline_id>/status", methods=["POST"])
@login_required
def update_status(deadline_id):
    """AJAX endpoint: student updates their task status."""
    if not current_user.is_student:
        return jsonify({"error": "forbidden"}), 403

    new_status = request.form.get("status", "pending")
    if new_status not in VALID_STATUSES:
        return jsonify({"error": "invalid status"}), 400

    existing = query(
        "SELECT task_id FROM StudentTasks WHERE student_id = ? AND deadline_id = ?",
        (current_user.id, deadline_id),
    )
    if existing:
        execute(
            "UPDATE StudentTasks SET status = ? WHERE student_id = ? AND deadline_id = ?",
            (new_status, current_user.id, deadline_id),
        )
    else:
        execute(
            "INSERT INTO StudentTasks (student_id, deadline_id, status) VALUES (?, ?, ?)",
            (current_user.id, deadline_id, new_status),
        )

    return jsonify({"ok": True, "status": new_status})
