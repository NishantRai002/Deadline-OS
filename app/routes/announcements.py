"""
DeadlineOS — Announcement routes
Author (Backend): Nishant Kumar
"""

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.db import query, execute

announcements_bp = Blueprint("announcements", __name__)


@announcements_bp.route("/")
@login_required
def list_all():
    rows = query(
        """SELECT a.announcement_id, a.title, a.body, a.created_at,
                  u.full_name, a.target_program, a.target_semester, a.target_section
           FROM Announcements a JOIN Users u ON u.user_id = a.created_by
           WHERE a.is_active = 1 ORDER BY a.created_at DESC"""
    )
    return render_template("announcements/list.html", announcements=rows)


@announcements_bp.route("/<int:ann_id>")
@login_required
def detail(ann_id):
    rows = query(
        """SELECT a.announcement_id, a.title, a.body, a.created_at,
                  u.full_name, a.target_program, a.target_semester, a.target_section,
                  att.blob_name, att.original_name
           FROM Announcements a
           JOIN Users u ON u.user_id = a.created_by
           LEFT JOIN Attachments att ON att.announcement_id = a.announcement_id
           WHERE a.announcement_id = ?""",
        (ann_id,),
    )
    if not rows:
        flash("Announcement not found.", "warning")
        return redirect(url_for("announcements.list_all"))

    return render_template("announcements/detail.html", ann=rows[0], attachments=rows)


@announcements_bp.route("/create", methods=["GET", "POST"])
@login_required
def create():
    if not current_user.is_faculty:
        flash("Only faculty or admins can post announcements.", "danger")
        return redirect(url_for("dashboard.index"))

    if request.method == "POST":
        title = request.form.get("title", "").strip()
        body = request.form.get("body", "").strip()
        target_program = request.form.get("target_program") or None
        target_semester = request.form.get("target_semester") or None
        target_section = request.form.get("target_section") or None

        if not title or not body:
            flash("Title and body are required.", "danger")
            return render_template("announcements/create.html")

        execute(
            """INSERT INTO Announcements
                   (title, body, created_by, target_program, target_semester, target_section, is_active)
               VALUES (?, ?, ?, ?, ?, ?, 1)""",
            (title, body, current_user.id, target_program, target_semester, target_section),
        )

        # Handle optional file upload
        file = request.files.get("attachment")
        if file and file.filename:
            from app.blob_storage import upload_file
            blob_name = upload_file(file.stream, file.filename)
            ann_id_rows = query(
                "SELECT TOP 1 announcement_id FROM Announcements ORDER BY announcement_id DESC"
            )
            if ann_id_rows:
                execute(
                    "INSERT INTO Attachments (announcement_id, blob_name, original_name) VALUES (?, ?, ?)",
                    (ann_id_rows[0][0], blob_name, file.filename),
                )

        flash("Announcement published.", "success")
        return redirect(url_for("announcements.list_all"))

    return render_template("announcements/create.html")


@announcements_bp.route("/<int:ann_id>/delete", methods=["POST"])
@login_required
def delete(ann_id):
    if not current_user.is_faculty:
        flash("Permission denied.", "danger")
        return redirect(url_for("announcements.list_all"))

    execute("UPDATE Announcements SET is_active = 0 WHERE announcement_id = ?", (ann_id,))
    flash("Announcement removed.", "info")
    return redirect(url_for("announcements.list_all"))
