"""
DeadlineOS — Authentication routes (login / register / logout)
Author (Backend): Nishant Kumar
"""

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app.db import query, execute
from app.models.user import User

auth_bp = Blueprint("auth", __name__)


# ── Register ───────────────────────────────────────────────────────────────
@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.index"))

    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        full_name = request.form.get("full_name", "").strip()
        password = request.form.get("password", "")
        role = request.form.get("role", "student")
        program = request.form.get("program", "").strip()
        semester = request.form.get("semester", "").strip()
        section = request.form.get("section", "").strip().upper()

        # Basic validation
        if not email or not full_name or not password:
            flash("All fields are required.", "danger")
            return render_template("auth/register.html")

        existing = query("SELECT user_id FROM Users WHERE email = ?", (email,))
        if existing:
            flash("An account with that email already exists.", "warning")
            return render_template("auth/register.html")

        hashed = generate_password_hash(password)
        execute(
            """INSERT INTO Users (email, full_name, password_hash, role, program, semester, section)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (email, full_name, hashed, role, program, semester, section),
        )
        flash("Account created! Please log in.", "success")
        return redirect(url_for("auth.login"))

    return render_template("auth/register.html")


# ── Login ──────────────────────────────────────────────────────────────────
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.index"))

    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        rows = query(
            "SELECT user_id, email, full_name, role, program, semester, section, password_hash "
            "FROM Users WHERE email = ?",
            (email,),
        )
        if not rows:
            flash("Invalid email or password.", "danger")
            return render_template("auth/login.html")

        row = rows[0]
        if not check_password_hash(row[7], password):
            flash("Invalid email or password.", "danger")
            return render_template("auth/login.html")

        user = User(row)
        login_user(user)

        # Log the access
        execute(
            "INSERT INTO AuditLogs (user_id, action) VALUES (?, ?)",
            (user.id, "login"),
        )

        next_page = request.args.get("next")
        return redirect(next_page or url_for("dashboard.index"))

    return render_template("auth/login.html")


# ── Logout ─────────────────────────────────────────────────────────────────
@auth_bp.route("/logout")
@login_required
def logout():
    execute(
        "INSERT INTO AuditLogs (user_id, action) VALUES (?, ?)",
        (current_user.id, "logout"),
    )
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("auth.login"))
