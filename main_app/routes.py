import os, secrets
from flask import render_template, request, redirect, url_for, flash, session
from flask_mail import Message
from werkzeug.security import generate_password_hash
from functools import wraps
from main_app.models import EditorBoard, ContactDetail, ResearchPaper, User, JournalMaster
from main_app.extensions import db, mail, app


# Automatically create tables and admin user
with app.app_context():
    db.create_all()
    admin = User.query.filter_by(username="admin").first()
    if not admin:
        admin = User(username="admin", email="admin@example.com", role="admin")
        admin.set_password("admin123")
        db.session.add(admin)
        db.session.commit()
        print("Admin user created: username='admin', password='admin123'")
    else:
        print("Admin user already exists")

users = {
    "admin": {
        "password": generate_password_hash("admin123"),
        "email": "admin@example.com",
        "role": "admin",
    }
}


@app.context_processor
def inject_globals():
    return dict(users=users, session=session)


@app.context_processor
def inject_contacts():
    contact = ContactDetail.query.first()
    return dict(contact=contact)


# ----------------------------------
# Helpers
# ----------------------------------
def login_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if "username" not in session:
            flash("Please log in first.", "warning")
            return redirect(url_for("login"))
        return fn(*args, **kwargs)

    return wrapper


def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if "username" not in session:
            flash("Please log in first.", "warning")
            return redirect(url_for("login"))
        current_user = session["username"]
        if users.get(current_user, {}).get("role") != "admin":
            flash("Admin access required.", "danger")
            return redirect(url_for("dashboard"))
        return fn(*args, **kwargs)

    return wrapper


# Homepage for the all journals
@app.route("/")
def cibdi_group():
    return render_template("group.html")

# Common Error page
@app.route('/error')
def error_page():
    title = request.args.get('title', 'Error')
    message = request.args.get('message', 'general')
    journal_code = request.args.get('journal_code', '')
    
    return render_template('error.html', 
        title=title,
        message=message,
        journal_code=journal_code
    )

# ------------------- CIBDI PAGES -------------------


@app.route("/cibdi/home")
def cibdi_home():
    editors = (
        EditorBoard.query.join(JournalMaster)
        .filter(JournalMaster.journal_id == "001")
        .order_by(EditorBoard.id.asc())
        .all()
    )
    contact = (
        ContactDetail.query.join(JournalMaster)
        .filter(JournalMaster.journal_id == "001")
        .order_by(ContactDetail.id.desc())
        .first()
    )
    return render_template("cibdi/homepage.html", editors=editors, contact=contact)


@app.route("/cibdi/about")
def cibdi_about():
    contact = (
        ContactDetail.query.join(JournalMaster)
        .filter(JournalMaster.journal_id == "001")
        .order_by(ContactDetail.id.desc())
        .first()
    )
    return render_template("cibdi/about.html", contact=contact)


@app.route("/cibdi/peer_reviewed")
def cibdi_peer_reviewed():
    contact = (
        ContactDetail.query.join(JournalMaster)
        .filter(JournalMaster.journal_id == "001")
        .order_by(ContactDetail.id.desc())
        .first()
    )
    return render_template("cibdi/peer_reviewed.html", contact=contact)


@app.route("/cibdi/ugc_care")
def cibdi_ugc_care():
    contact = (
        ContactDetail.query.join(JournalMaster)
        .filter(JournalMaster.journal_id == "001")
        .order_by(ContactDetail.id.desc())
        .first()
    )
    return render_template("cibdi/ugc_care.html", contact=contact)


@app.route("/cibdi/doi_allocation")
def cibdi_doi_Allocation():
    contact = (
        ContactDetail.query.join(JournalMaster)
        .filter(JournalMaster.journal_id == "001")
        .order_by(ContactDetail.id.desc())
        .first()
    )
    return render_template("cibdi/DOI_Allocation.html", contact=contact)


@app.route("/cibdi/payment")
def cibdi_payment():
    contact = (
        ContactDetail.query.join(JournalMaster)
        .filter(JournalMaster.journal_id == "001")
        .order_by(ContactDetail.id.desc())
        .first()
    )
    return render_template("cibdi/Payment.html", contact=contact)


@app.route("/cibdi/current_issue")
def cibdi_current_issue():
    papers = (
        ResearchPaper.query.join(JournalMaster)
        .filter(JournalMaster.journal_id == "001")
        .order_by(ResearchPaper.id.desc())
        .all()
    )
    contact = (
        ContactDetail.query.join(JournalMaster)
        .filter(JournalMaster.journal_id == "001")
        .order_by(ContactDetail.id.desc())
        .first()
    )
    return render_template("cibdi/Current_issue.html", papers=papers, contact=contact)


@app.route("/cibdi/paper/<int:paper_id>")
def cibdi_paper_detail(paper_id):
    contact = (
        ContactDetail.query.join(JournalMaster)
        .filter(JournalMaster.journal_id == "001")
        .order_by(ContactDetail.id.desc())
        .first()
    )
    paper = ResearchPaper.query.filter_by(id=paper_id, journal_id="001").first_or_404()
    return render_template("cibdi/paper_detail.html", paper=paper, contact=contact)


# ================= CRIN ROUTES ================= #

@app.route("/crin/home")
def crin_home():
    editors = (
        EditorBoard.query.join(JournalMaster)
        .filter(JournalMaster.journal_id == "002")
        .order_by(EditorBoard.id.asc())
        .all()
    )
    contact = (
        ContactDetail.query.join(JournalMaster)
        .filter(JournalMaster.journal_id == "002")
        .order_by(ContactDetail.id.desc())
        .first()
    )
    return render_template("crin/homepage.html", editors=editors, contact=contact)


@app.route("/crin/about")
def crin_about():
    contact = (
        ContactDetail.query.join(JournalMaster)
        .filter(JournalMaster.journal_id == "002")
        .order_by(ContactDetail.id.desc())
        .first()
    )
    return render_template("crin/about.html", contact=contact)


@app.route("/crin/peer_reviewed")
def crin_peer_reviewed():
    contact = (
        ContactDetail.query.join(JournalMaster)
        .filter(JournalMaster.journal_id == "002")
        .order_by(ContactDetail.id.desc())
        .first()
    )
    return render_template("crin/peer_reviewed.html", contact=contact)


@app.route("/crin/ugc_care")
def crin_ugc_care():
    contact = (
        ContactDetail.query.join(JournalMaster)
        .filter(JournalMaster.journal_id == "002")
        .order_by(ContactDetail.id.desc())
        .first()
    )
    return render_template("crin/ugc_care.html", contact=contact)


@app.route("/crin/doi_allocation")
def crin_doi_allocation():
    contact = (
        ContactDetail.query.join(JournalMaster)
        .filter(JournalMaster.journal_id == "002")
        .order_by(ContactDetail.id.desc())
        .first()
    )
    return render_template("crin/DOI_Allocation.html", contact=contact)


@app.route("/crin/payment")
def crin_payment():
    contact = (
        ContactDetail.query.join(JournalMaster)
        .filter(JournalMaster.journal_id == "002")
        .order_by(ContactDetail.id.desc())
        .first()
    )
    return render_template("crin/Payment.html", contact=contact)


@app.route("/crin/current_issue")
def crin_current_issue():
    contact = (
        ContactDetail.query.join(JournalMaster)
        .filter(JournalMaster.journal_id == "002")
        .order_by(ContactDetail.id.desc())
        .first()
    )
    papers = (
        ResearchPaper.query.join(JournalMaster)
        .filter(JournalMaster.journal_id == "002")
        .order_by(ResearchPaper.id.desc())
        .all()
    )
    return render_template("crin/Current_issue.html", papers=papers, contact=contact)


@app.route("/crin/paper/<int:paper_id>")
def crin_paper_detail(paper_id):
    contact = (
        ContactDetail.query.join(JournalMaster)
        .filter(JournalMaster.journal_id == "002")
        .order_by(ContactDetail.id.desc())
        .first()
    )
    # Fetch the paper with given id AND journal_id = '002'
    paper = ResearchPaper.query.filter_by(id=paper_id, journal_id="002").first_or_404()
    return render_template("crin/paper_detail.html", paper=paper, contact=contact)


# ================= FAAI ROUTES ================= #


@app.route("/faai/home")
def faai_home():
    editors = (
        EditorBoard.query.join(JournalMaster)
        .filter(JournalMaster.journal_id == "003")
        .order_by(EditorBoard.id.asc())
        .all()
    )
    contact = (
        ContactDetail.query.join(JournalMaster)
        .filter(JournalMaster.journal_id == "003")
        .order_by(ContactDetail.id.desc())
        .first()
    )

    return render_template("faai/homepage.html", editors=editors, contact=contact)


@app.route("/faai/about")
def faai_about():
    contact = (
        ContactDetail.query.join(JournalMaster)
        .filter(JournalMaster.journal_id == "003")
        .order_by(ContactDetail.id.desc())
        .first()
    )
    return render_template("faai/about.html", contact=contact)


@app.route("/faai/peer_reviewed")
def faai_peer_reviewed():
    contact = (
        ContactDetail.query.join(JournalMaster)
        .filter(JournalMaster.journal_id == "003")
        .order_by(ContactDetail.id.desc())
        .first()
    )
    return render_template("faai/peer_reviewed.html", contact=contact)


@app.route("/faai/ugc_care")
def faai_ugc_care():
    contact = (
        ContactDetail.query.join(JournalMaster)
        .filter(JournalMaster.journal_id == "003")
        .order_by(ContactDetail.id.desc())
        .first()
    )
    return render_template("faai/ugc_care.html", contact=contact)


@app.route("/faai/doi_allocation")
def faai_DOI_Allocation():
    contact = (
        ContactDetail.query.join(JournalMaster)
        .filter(JournalMaster.journal_id == "003")
        .order_by(ContactDetail.id.desc())
        .first()
    )
    return render_template("faai/DOI_Allocation.html", contact=contact)


@app.route("/faai/payment")
def faai_Payment():
    contact = (
        ContactDetail.query.join(JournalMaster)
        .filter(JournalMaster.journal_id == "003")
        .order_by(ContactDetail.id.desc())
        .first()
    )
    return render_template("faai/Payment.html", contact=contact)


@app.route("/faai/current_issue")
def faai_current_issue():
    contact = (
        ContactDetail.query.join(JournalMaster)
        .filter(JournalMaster.journal_id == "003")
        .order_by(ContactDetail.id.desc())
        .first()
    )
    papers = (
        ResearchPaper.query.join(JournalMaster)
        .filter(JournalMaster.journal_id == "003")
        .order_by(ResearchPaper.id.desc())
        .all()
    )
    return render_template("faai/Current_issue.html", papers=papers, contact=contact)


@app.route("/faai/paper/<int:paper_id>")
def faai_paper_detail(paper_id):
    contact = (
        ContactDetail.query.join(JournalMaster)
        .filter(JournalMaster.journal_id == "003")
        .order_by(ContactDetail.id.desc())
        .first()
    )
    paper = ResearchPaper.query.filter_by(id=paper_id, journal_id="003").first_or_404()
    return render_template("faai/paper_detail.html", paper=paper, contact=contact)


# ================= FERI ROUTES ================= #


@app.route("/feri/home")
def feri_home():
    editors = (
        EditorBoard.query.join(JournalMaster)
        .filter(JournalMaster.journal_id == "004")
        .order_by(EditorBoard.id.asc())
        .all()
    )
    contact = (
        ContactDetail.query.join(JournalMaster)
        .filter(JournalMaster.journal_id == "004")
        .order_by(ContactDetail.id.desc())
        .first()
    )
    return render_template("feri/homepage.html", editors=editors, contact=contact)


@app.route("/feri/about")
def feri_about():
    contact = (
        ContactDetail.query.join(JournalMaster)
        .filter(JournalMaster.journal_id == "004")
        .order_by(ContactDetail.id.desc())
        .first()
    )
    return render_template("feri/about.html", contact=contact)


@app.route("/feri/peer_reviewed")
def feri_peer_reviewed():
    contact = (
        ContactDetail.query.join(JournalMaster)
        .filter(JournalMaster.journal_id == "004")
        .order_by(ContactDetail.id.desc())
        .first()
    )
    return render_template("feri/peer_reviewed.html", contact=contact)


@app.route("/feri/ugc_care")
def feri_ugc_care():
    contact = (
        ContactDetail.query.join(JournalMaster)
        .filter(JournalMaster.journal_id == "004")
        .order_by(ContactDetail.id.desc())
        .first()
    )
    return render_template("feri/ugc_care.html", contact=contact)


@app.route("/feri/doi_allocation")
def feri_doi_allocation():
    contact = (
        ContactDetail.query.join(JournalMaster)
        .filter(JournalMaster.journal_id == "004")
        .order_by(ContactDetail.id.desc())
        .first()
    )
    return render_template("feri/DOI_Allocation.html", contact=contact)


@app.route("/feri/payment")
def feri_payment():
    contact = (
        ContactDetail.query.join(JournalMaster)
        .filter(JournalMaster.journal_id == "004")
        .order_by(ContactDetail.id.desc())
        .first()
    )
    return render_template("feri/Payment.html", contact=contact)


@app.route("/feri/current_issue")
def feri_current_issue():
    contact = (
        ContactDetail.query.join(JournalMaster)
        .filter(JournalMaster.journal_id == "004")
        .order_by(ContactDetail.id.desc())
        .first()
    )
    papers = (
        ResearchPaper.query.join(JournalMaster)
        .filter(JournalMaster.journal_id == "004")
        .order_by(ResearchPaper.id.desc())
        .all()
    )
    return render_template("feri/Current_issue.html", papers=papers, contact=contact)


@app.route("/feri/paper/<int:paper_id>")
def feri_paper_detail(paper_id):
    contact = (
        ContactDetail.query.join(JournalMaster)
        .filter(JournalMaster.journal_id == "004")
        .order_by(ContactDetail.id.desc())
        .first()
    )
    paper = ResearchPaper.query.filter_by(id=paper_id, journal_id="004").first_or_404()
    return render_template("feri/paper_detail.html", paper=paper, contact=contact)


# ================= FHIM ROUTES ================= #


@app.route("/fhim/home")
def fhim_home():
    editors = (
        EditorBoard.query.join(JournalMaster)
        .filter(JournalMaster.journal_id == "005")
        .order_by(EditorBoard.id.asc())
        .all()
    )
    contact = (
        ContactDetail.query.join(JournalMaster)
        .filter(JournalMaster.journal_id == "005")
        .order_by(ContactDetail.id.desc())
        .first()
    )

    return render_template("fhim/homepage.html", editors=editors, contact=contact)


@app.route("/fhim/about")
def fhim_about():
    contact = (
        ContactDetail.query.join(JournalMaster)
        .filter(JournalMaster.journal_id == "005")
        .order_by(ContactDetail.id.desc())
        .first()
    )
    return render_template("fhim/about.html", contact=contact)


@app.route("/fhim/peer_reviewed")
def fhim_peer_reviewed():
    contact = (
        ContactDetail.query.join(JournalMaster)
        .filter(JournalMaster.journal_id == "005")
        .order_by(ContactDetail.id.desc())
        .first()
    )
    return render_template("fhim/peer_reviewed.html", contact=contact)


@app.route("/fhim/ugc_care")
def fhim_ugc_care():
    contact = (
        ContactDetail.query.join(JournalMaster)
        .filter(JournalMaster.journal_id == "005")
        .order_by(ContactDetail.id.desc())
        .first()
    )
    return render_template("fhim/ugc_care.html", contact=contact)


@app.route("/fhim/doi_allocation")
def fhim_doi_allocation():
    contact = (
        ContactDetail.query.join(JournalMaster)
        .filter(JournalMaster.journal_id == "005")
        .order_by(ContactDetail.id.desc())
        .first()
    )
    return render_template("fhim/DOI_Allocation.html", contact=contact)


@app.route("/fhim/payment")
def fhim_payment():
    contact = (
        ContactDetail.query.join(JournalMaster)
        .filter(JournalMaster.journal_id == "005")
        .order_by(ContactDetail.id.desc())
        .first()
    )
    return render_template("fhim/Payment.html", contact=contact)


@app.route("/fhim/current_issue")
def fhim_current_issue():
    papers = (
        ResearchPaper.query.join(JournalMaster)
        .filter(JournalMaster.journal_id == "005")
        .order_by(ResearchPaper.id.desc())
        .all()
    )
    contact = (
        ContactDetail.query.join(JournalMaster)
        .filter(JournalMaster.journal_id == "005")
        .order_by(ContactDetail.id.desc())
        .first()
    )
    return render_template("fhim/Current_issue.html", papers=papers, contact=contact)


@app.route("/fhim/paper/<int:paper_id>")
def fhim_paper_detail(paper_id):
    contact = (
        ContactDetail.query.join(JournalMaster)
        .filter(JournalMaster.journal_id == "005")
        .order_by(ContactDetail.id.desc())
        .first()
    )
    paper = ResearchPaper.query.filter_by(id=paper_id, journal_id="005").first_or_404()
    return render_template("fhim/paper_detail.html", paper=paper, contact=contact)


# ------------------------------------------------------------------------
# admin
# -------------------------------------------------------------------------
# -------------------------------------------------------------------------


# ----------------------------------
# Auth Routes
# ----------------------------------

@app.route("/login", methods=["GET", "POST"])
def login():
    # Agar user already login hai
    if "username" in session:
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        username = (request.form.get("username") or "").strip()
        password = request.form.get("password") or ""
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            session["username"] = username
            flash("Login successful!", "success")
            return redirect(url_for("dashboard"))
        flash("Invalid username or password", "danger")
    return render_template("login.html")


@app.route("/logout")
@login_required
def logout():
    session.pop("username", None)
    flash("You have been logged out", "info")
    return redirect(url_for("login"))


@app.route("/forgot_password", methods=["GET", "POST"])
def forgot_password():
    if request.method == "POST":
        email = (request.form.get("email") or "").strip()
        user_key = next(
            (u for u, data in users.items() if data.get("email") == email), None
        )
        if not user_key:
            flash("Email not found.", "danger")
            return redirect(url_for("forgot_password"))

        temp_password = secrets.token_urlsafe(8)
        users[user_key]["password"] = generate_password_hash(temp_password)
        try:
            msg = Message("Password Reset", recipients=[email])
            msg.body = f"Your temporary password is: {temp_password}\nPlease change it after login."
            mail.send(msg)
            flash("Temporary password sent to your email.", "success")
        except Exception:
            flash("Could not send email. Please check mail config.", "warning")
        return redirect(url_for("login"))
    return render_template("forgot_password.html")


# ----------------------------------
# Dashboard + User Management
# ----------------------------------
@app.route("/dashboard")
@login_required
def dashboard():
    current_user = User.query.filter_by(username=session["username"]).first()
    is_admin = current_user.role == "admin"
    all_users = User.query.all() if is_admin else None

    return render_template(
        "dashboard.html",
        users=all_users,
        current_user=current_user,
        is_admin=is_admin,
    )


@app.route("/add_user", methods=["POST"])
@admin_required
def add_user():
    user = User.query.filter_by(username=session["username"]).first()
    if not user:
        flash("User not found.", "danger")
        return redirect(url_for("dashboard"))

    username = (request.form.get("username") or "").strip().lower()
    email = (request.form.get("email") or "").strip().lower()
    password = request.form.get("password") or ""
    role = (request.form.get("role") or "user").strip()

    if not username or not password or not email:
        flash("Username, email, and password are required.", "warning")
        return redirect(url_for("dashboard"))

    # check username exists
    if User.query.filter_by(username=username).first():
        flash(" Username already exists.", "danger")
        return redirect(url_for("dashboard"))

    # check email exists
    if User.query.filter_by(email=email).first():
        flash(" Email already registered with another user.", "danger")
        return redirect(url_for("dashboard"))

    # only if unique, then create new user
    new_user = User(
        username=username,
        email=email,
        role=role if role in ("admin", "user") else "user",
    )
    new_user.set_password(password)

    db.session.add(new_user)
    db.session.commit()

    flash("User added successfully.", "success")
    return redirect(url_for("dashboard"))


@app.route("/edit_user/<username>", methods=["GET", "POST"])
@admin_required
def edit_user(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        flash("User not found.", "danger")
        return redirect(url_for("dashboard"))
    
    current_user = User.query.filter_by(username=session["username"]).first()
    is_admin = current_user.role == "admin"

    if request.method == "POST":
        email = (request.form.get("email") or "").strip()
        role = (request.form.get("role") or "user").strip()
        new_password = request.form.get("password") or ""

        if email:
            user.email = email
        user.role = role if role in ("admin", "user") else "user"
        if new_password:
            user.set_password(new_password)  # <-- Use set_password

        db.session.commit()
        flash("User updated successfully.", "success")
        return redirect(url_for("dashboard"))

    return render_template("edit_user.html", user=user, current_user=current_user, is_admin=is_admin)


@app.route("/delete_user/<username>", methods=["POST", "GET"])
@admin_required
def delete_user(username):
    current_user = session["username"]

    if username == current_user:
        flash("You cannot delete the currently logged-in user.", "danger")
        return redirect(url_for("dashboard"))

    user = User.query.filter_by(username=username).first()
    if user:
        db.session.delete(user)
        db.session.commit()
        flash("User deleted successfully.", "success")
    else:
        flash("User not found.", "danger")
    return redirect(url_for("dashboard"))


# ----------------------------------
# CRUD: Editor Board
# ----------------------------------
@app.route("/listedi", methods=["GET"])
@admin_required
def listedi():
    current_user = User.query.filter_by(username=session["username"]).first()
    is_admin = current_user.role == "admin"
    selected_journal = request.args.get("journal_id")
    selected_category = request.args.get("code")

    journals = JournalMaster.query.all()
    query = EditorBoard.query.join(JournalMaster)

    # Journal filter
    if selected_journal and selected_journal != "all":
        query = query.filter(JournalMaster.journal_id == selected_journal)

    # Category filter
    if selected_category and selected_category != "all":
        query = query.filter(EditorBoard.code == selected_category)

    boards = query.order_by(EditorBoard.id.asc()).all()

    return render_template(
        "listedi.html",
        boards=boards,
        journals=journals,
        selected_journal=selected_journal,
        selected_category=selected_category,
        current_user=current_user, 
        is_admin=is_admin
    )


@app.route("/add", methods=["GET", "POST"])
@admin_required
def add_editor():
    current_user = User.query.filter_by(username=session["username"]).first()
    is_admin = current_user.role == "admin"
    journals = JournalMaster.query.all()  # ðŸ”¹ Get all journals for dropdown
    if request.method == "POST":
        journal_id = request.form.get("journal_id")  # Selected journal
        new_editor = EditorBoard(
            name=request.form.get("name"),
            designation=request.form.get("designation"),
            link=request.form.get("link"),
            quote=request.form.get("quote"),
            code=request.form.get("code"),
            journal_id=journal_id,
        )
        db.session.add(new_editor)
        db.session.commit()
        flash("Editor record added.", "success")
        return redirect(url_for("listedi"))
    return render_template("add.html", journals=journals, current_user=current_user, is_admin=is_admin)


@app.route("/edit/<int:id>", methods=["GET", "POST"])
@admin_required
def edit_editor(id):
    current_user = User.query.filter_by(username=session["username"]).first()
    is_admin = current_user.role == "admin"
    editor = EditorBoard.query.get_or_404(id)
    journals = JournalMaster.query.all()
    if request.method == "POST":
        editor.name = request.form.get("name")
        editor.designation = request.form.get("designation")
        editor.link = request.form.get("link")
        editor.quote = request.form.get("quote")
        editor.code = request.form.get("code")
        editor.journal_id = request.form.get("journal_id")
        db.session.commit()
        flash("Editor record updated.", "success")
        return redirect(url_for("listedi"))
    return render_template("edit.html", editor=editor, journals=journals, current_user=current_user, is_admin=is_admin)


@app.route("/delete/<int:id>", methods=["POST", "GET"])
@admin_required
def delete_editor(id):
    editor = EditorBoard.query.get_or_404(id)
    db.session.delete(editor)
    db.session.commit()
    flash("Editor record deleted.", "info")
    return redirect(url_for("listedi"))


# ----------------------------------
# CRUD: Contacts
# ----------------------------------
@app.route("/list_contacts")
@admin_required
def list_contacts():
    current_user = User.query.filter_by(username=session["username"]).first()
    is_admin = current_user.role == "admin"
    contacts = ContactDetail.query.order_by(ContactDetail.id.asc()).all()
    return render_template("contacts/list.html", contacts=contacts, current_user=current_user, is_admin=is_admin)


@app.route("/contacts/add", methods=["GET", "POST"])
@admin_required
def add_contact():
    current_user = User.query.filter_by(username=session["username"]).first()
    is_admin = current_user.role == "admin"
    journals = JournalMaster.query.all()  # ðŸ”¹ fetch all journals for dropdown
    if request.method == "POST":
        journal_id = request.form.get("journal_id")
        new_contact = ContactDetail(
            name=request.form.get("name"),
            email=request.form.get("email"),
            phone=request.form.get("phone"),
            address=request.form.get("address"),
            linkedin=request.form.get("linkedin"),
            instagram=request.form.get("instagram"),
            facebook=request.form.get("facebook"),
            twitter=request.form.get("twitter"),
            company_website=request.form.get("company_website"),
            youtube_url=request.form.get("youtube_url"),
            journal_id=journal_id,
        )
        db.session.add(new_contact)
        db.session.commit()
        flash("Contact added successfully!", "success")
        return redirect(url_for("list_contacts"))
    return render_template("contacts/add.html", journals=journals, current_user=current_user, is_admin=is_admin)


@app.route("/contacts/edit/<int:id>", methods=["GET", "POST"])
@admin_required
def edit_contact(id):
    current_user = User.query.filter_by(username=session["username"]).first()
    is_admin = current_user.role == "admin"
    contact = ContactDetail.query.get_or_404(id)
    journals = JournalMaster.query.all()  # ðŸ”¹ fetch all journals for dropdown
    if request.method == "POST":
        contact.name = request.form.get("name")
        contact.email = request.form.get("email")
        contact.phone = request.form.get("phone")
        contact.address = request.form.get("address")
        contact.linkedin = request.form.get("linkedin")
        contact.instagram = request.form.get("instagram")
        contact.facebook = request.form.get("facebook")
        contact.twitter = request.form.get("twitter")
        contact.company_website = request.form.get("company_website")
        contact.youtube_url = request.form.get("youtube_url")
        contact.journal_id = request.form.get("journal_id")
        db.session.commit()
        flash("Contact updated successfully!", "success")
        return redirect(url_for("list_contacts"))
    return render_template(
        "contacts/edit.html", contact=contact, journals=journals, current_user=current_user, is_admin=is_admin
    )


@app.route("/contacts/delete/<int:id>", methods=["POST", "GET"])
@admin_required
def delete_contact(id):
    contact = ContactDetail.query.get_or_404(id)
    db.session.delete(contact)
    db.session.commit()
    flash("Contact deleted successfully!", "info")
    return redirect(url_for("list_contacts"))


# ----------------------------------
# CRUD: Research Papers
# ----------------------------------

# List
@app.route("/list_papers")
@admin_required
def list_papers():
    current_user = User.query.filter_by(username=session["username"]).first()
    is_admin = current_user.role == "admin"
    papers = ResearchPaper.query.order_by(ResearchPaper.id.desc()).all()
    return render_template("list_papers.html", papers=papers, current_user=current_user, is_admin=is_admin)

# -------------------------
# Research Paper: CRUD (improved)
# -------------------------
import os
from werkzeug.utils import secure_filename
from flask import current_app, send_from_directory

# config (set near top of your app)
app.config.setdefault("UPLOAD_FOLDER", "static/assets/pdf")

app.config["ALLOWED_EXTENSIONS"] = ["pdf", "jpg", "jpeg", "png", "gif"]
# ensure upload folder exists
upload_dir = os.path.join(app.root_path, app.config["UPLOAD_FOLDER"])
os.makedirs(upload_dir, exist_ok=True)


def allowed_file(filename, allowed_extensions=None):
    if allowed_extensions is None:
        allowed_extensions = app.config["ALLOWED_EXTENSIONS"]
    return "." in filename and filename.rsplit(".", 1)[1].lower() in allowed_extensions


# Download / View
@app.route("/download_pdf/<int:paper_id>")
def download_pdf(paper_id):
    paper = ResearchPaper.query.get_or_404(paper_id)
    if not paper.pdf_filename:
        flash("No PDF available for this paper.", "warning")
        return redirect(url_for("list_papers"))
    directory = os.path.join(app.root_path, app.config["UPLOAD_FOLDER"])
    return send_from_directory(directory, paper.pdf_filename, as_attachment=True)


# Add
# ----------------- HELPER -----------------
def allowed_file(filename, allowed_extensions):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in allowed_extensions


# ----------------- ADD PAPER -----------------
@app.route("/add_paper", methods=["GET", "POST"])
@admin_required
def add_paper():
    journals = JournalMaster.query.all()  # fetch all journals for dropdown
    current_user = User.query.filter_by(username=session["username"]).first()
    is_admin = current_user.role == "admin"
    if request.method == "POST":
        # ---------------- Get form fields ----------------
        main_heading = request.form.get("main_heading") or ""
        sub_heading = request.form.get("sub_heading") or ""
        title = request.form.get("title") or ""
        authors = request.form.get("authors") or ""
        journal_id = request.form.get("journal_id")
        volume = request.form.get("volume")
        issue = request.form.get("issue")
        year = request.form.get("year")
        abstract = request.form.get("abstract") or ""
        citation = request.form.get("citation")

        # Validate journal_id
        if not (journal_id and journal_id.isdigit()):
            flash("Please select a valid Journal.", "warning")
            return redirect(request.url)
        journal_id = int(journal_id)

        # ---------------- PDF Upload ----------------
        pdf_file = request.files.get("pdf_file")
        if not pdf_file or pdf_file.filename == "":
            flash("Please upload a PDF file.", "warning")
            return redirect(request.url)
        if not allowed_file(pdf_file.filename, ["pdf"]):
            flash("Only PDF files are allowed.", "danger")
            return redirect(request.url)

        pdf_filename = secure_filename(pdf_file.filename)
        pdf_dir = os.path.join(app.root_path, "static", "assets", "pdf")
        os.makedirs(pdf_dir, exist_ok=True)
        pdf_path = os.path.join(pdf_dir, pdf_filename)

        # Avoid duplicate filenames
        counter = 1
        base, ext = os.path.splitext(pdf_filename)
        while os.path.exists(pdf_path):
            pdf_filename = f"{base}_{counter}{ext}"
            pdf_path = os.path.join(pdf_dir, pdf_filename)
            counter += 1
        pdf_file.save(pdf_path)

        # ---------------- Image Upload (optional) ----------------
        image_file = request.files.get("image_filename")
        image_filename = None
        if image_file and image_file.filename != "":
            if allowed_file(image_file.filename, ["jpg", "jpeg", "png", "gif"]):
                image_filename = secure_filename(image_file.filename)
                img_dir = os.path.join(app.root_path, "static", "assets", "img")
                os.makedirs(img_dir, exist_ok=True)
                img_path = os.path.join(img_dir, image_filename)

                counter = 1
                base, ext = os.path.splitext(image_filename)
                while os.path.exists(img_path):
                    image_filename = f"{base}_{counter}{ext}"
                    img_path = os.path.join(img_dir, image_filename)
                    counter += 1

                image_file.save(img_path)

        # ---------------- Save to DB ----------------
        new_paper = ResearchPaper(
            main_heading=main_heading,
            sub_heading=sub_heading,
            title=title,
            authors=authors,
            journal_id=journal_id,  # Foreign key
            volume=volume,
            issue=issue,
            year=year,
            abstract=abstract,
            pdf_filename=pdf_filename,
            image_filename=image_filename,
            citation=citation,
        )

        db.session.add(new_paper)
        db.session.commit()
        flash("New Research Paper added in the Journal successfully.", "success")
        return redirect(url_for("list_papers"))

    # GET request
    return render_template("add_paper.html", journals=journals, current_user=current_user, is_admin=is_admin)


# ----------------- EDIT PAPER -----------------
@app.route("/edit_paper/<int:id>", methods=["GET", "POST"])
@admin_required
def edit_paper(id):
    current_user = User.query.filter_by(username=session["username"]).first()
    is_admin = current_user.role == "admin"
    paper = ResearchPaper.query.get_or_404(id)
    journals = JournalMaster.query.all()
    if request.method == "POST":
        paper.main_heading = request.form.get("main_heading") or paper.main_heading
        paper.sub_heading = request.form.get("sub_heading") or paper.sub_heading
        paper.title = request.form.get("title") or paper.title
        paper.authors = request.form.get("authors") or paper.authors
        paper.journal_id = request.form.get("journal_id") or paper.journal_id
        paper.volume = request.form.get("volume")
        paper.issue = request.form.get("issue")
        paper.year = request.form.get("year")
        paper.abstract = request.form.get("abstract") or paper.abstract
        paper.citation = request.form.get("citation")

        # ---------------- PDF upload ----------------
        file = request.files.get("pdf_file")
        if file and file.filename:
            if not allowed_file(file.filename, ["pdf"]):
                flash("Only PDF files are allowed.", "danger")
                return redirect(request.url)

            filename = secure_filename(file.filename)
            pdf_dir = os.path.join(app.root_path, "static", "assets", "pdf")
            os.makedirs(pdf_dir, exist_ok=True)
            save_path = os.path.join(pdf_dir, filename)

            base, ext = os.path.splitext(filename)
            counter = 1
            while os.path.exists(save_path):
                filename = f"{base}_{counter}{ext}"
                save_path = os.path.join(pdf_dir, filename)
                counter += 1

            file.save(save_path)

            # remove old file
            if paper.pdf_filename:
                try:
                    old_path = os.path.join(pdf_dir, paper.pdf_filename)
                    if os.path.exists(old_path):
                        os.remove(old_path)
                except Exception:
                    app.logger.exception("Could not remove old PDF")

            paper.pdf_filename = filename

        # ---------------- Image upload ----------------
        image_file = request.files.get("image_filename")
        if image_file and image_file.filename:
            if not allowed_file(image_file.filename, ["jpg", "jpeg", "png", "gif"]):
                flash("Only image files are allowed.", "danger")
                return redirect(request.url)

            image_filename = secure_filename(image_file.filename)
            img_dir = os.path.join(app.root_path, "static", "assets", "img")
            os.makedirs(img_dir, exist_ok=True)
            img_path = os.path.join(img_dir, image_filename)

            base, ext = os.path.splitext(image_filename)
            counter = 1
            while os.path.exists(img_path):
                image_filename = f"{base}_{counter}{ext}"
                img_path = os.path.join(img_dir, image_filename)
                counter += 1

            image_file.save(img_path)

            # remove old image
            if paper.image_filename:
                try:
                    old_img_path = os.path.join(img_dir, paper.image_filename)
                    if os.path.exists(old_img_path):
                        os.remove(old_img_path)
                except Exception:
                    app.logger.exception("Could not remove old image")

            paper.image_filename = image_filename

        db.session.commit()
        flash("Research Paper updated successfully!!", "info")
        return redirect(url_for("list_papers"))

    return render_template("edit_paper.html", paper=paper, journals=journals, current_user=current_user, is_admin=is_admin)


# Delete
@app.route("/delete_paper/<int:id>", methods=["POST", "GET"])
@admin_required
def delete_paper(id):
    paper = ResearchPaper.query.get_or_404(id)
    # delete file from FS
    if paper.pdf_filename:
        try:
            file_path = os.path.join(
                app.root_path, app.config["UPLOAD_FOLDER"], paper.pdf_filename
            )
            if os.path.exists(file_path):
                os.remove(file_path)
        except Exception:
            app.logger.exception("Failed to delete PDF file")

    db.session.delete(paper)
    db.session.commit()
    flash("Research Paper deleted successfully.", "danger")
    return redirect(url_for("list_papers"))
