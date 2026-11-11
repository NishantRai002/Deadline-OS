"""
DeadlineOS — Admin panel routes
Author (Backend): Nishant Kumar
"""

from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app.db import query, execute

admin_bp = Blueprint("admin", __name__)


def _require_admin():
    if not current_user.is_admin:
        flash("Admin access required.", "danger")
        return redirect(url_for("dashboard.index"))
    return None


@admin_bp.route("/")
@login_required
def index():
    guard = _require_admin()
    if guard:
        return guard

    users = query("SELECT user_id, full_name, email, role, program, semester FROM Users ORDER BY role, full_name")
    total_ann = query("SELECT COUNT(*) FROM Announcements WHERE is_active = 1")[0][0]
    total_dl = query("SELECT COUNT(*) FROM Deadlines WHERE is_active = 1")[0][0]
    total_users = query("SELECT COUNT(*) FROM Users")[0][0]

    return render_template(
        "admin/index.html",
        users=users,
        total_ann=total_ann,
        total_dl=total_dl,
        total_users=total_users,
    )


@admin_bp.route("/users/<int:user_id>/delete", methods=["POST"])
@login_required
def delete_user(user_id):
    guard = _require_admin()
    if guard:
        return guard

    execute("DELETE FROM Users WHERE user_id = ?", (user_id,))
    flash("User removed.", "info")
    return redirect(url_for("admin.index"))


@admin_bp.route("/audit-logs")
@login_required
def audit_logs():
    guard = _require_admin()
    if guard:
        return guard

    logs = query(
        """SELECT al.log_id, u.full_name, al.action, al.created_at
           FROM AuditLogs al JOIN Users u ON u.user_id = al.user_id
           ORDER BY al.created_at DESC"""
    )
    return render_template("admin/audit_logs.html", logs=logs)
