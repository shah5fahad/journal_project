import os, secrets, json
from flask import render_template, request, redirect, url_for, flash, session, jsonify
from flask_mail import Message
from werkzeug.security import generate_password_hash
from functools import wraps
from main_app.models import EditorBoard, ContactDetail, ResearchPaper, User, JournalMaster, UserFeedback, OTPVerification, SubmittedPaper, PaperReviewComment
import random
from main_app.extensions import db, mail, app
from datetime import datetime, timedelta
from collections import defaultdict
from sqlalchemy import tuple_, text, inspect
from sqlalchemy.exc import IntegrityError
from werkzeug.utils import secure_filename

MAX_PAPER_FILE_SIZE_BYTES = 5 * 1024 * 1024
MAX_PAYMENT_FILE_SIZE_BYTES = 1 * 1024 * 1024
PAPER_STATUS_OPTIONS = [
    "under_review",
    "revised",
    "rejected",
    "payment_completed_paper_accepted",
    "paper_published",
]

PAPER_STATUS_LABELS = {
    "under_review": "Under review",
    "revised": "Revised",
    "rejected": "Rejected",
    "payment_completed_paper_accepted": "Payment completed & paper accepted",
    "paper_published": "Paper Published",
}


def get_uploaded_file_size(upload_file):
    if not upload_file or not upload_file.filename:
        return 0

    try:
        current_position = upload_file.stream.tell()
        upload_file.stream.seek(0, os.SEEK_END)
        size = upload_file.stream.tell()
        upload_file.stream.seek(current_position)
        return size
    except Exception:
        return int(upload_file.content_length or 0)


def _ensure_missing_columns():
    inspector = inspect(db.engine) 
    columns = [column_info["name"] for column_info in inspector.get_columns("users")]
    if "name" not in columns:
        db.session.execute(text("ALTER TABLE users ADD COLUMN name VARCHAR(150)"))
    if "is_verified" not in columns:
        db.session.execute(text("ALTER TABLE users ADD COLUMN is_verified BOOLEAN DEFAULT FALSE"))
        
    columns = [column["name"] for column in inspector.get_columns("research_paper")]
    if "main_heading" in columns:
        db.session.execute(text("ALTER TABLE research_paper DROP COLUMN main_heading"))
    if "sub_heading" in columns:
        db.session.execute(text("ALTER TABLE research_paper DROP COLUMN sub_heading"))

    db.session.commit()

    papers_without_id = SubmittedPaper.query.filter((SubmittedPaper.paper_id == None) | (SubmittedPaper.paper_id == "")).order_by(SubmittedPaper.id.asc()).all()
    for paper in papers_without_id:
        paper.paper_id = _generate_submission_paper_id(paper.id)
    papers_without_workflow_status = SubmittedPaper.query.filter((SubmittedPaper.workflow_status == None) | (SubmittedPaper.status == "approved")).order_by(SubmittedPaper.id.asc()).all()
    for paper in papers_without_workflow_status:
        if paper.status == "approved":
            paper.workflow_status = "paper_published"
    db.session.commit()

    try:
        db.session.execute(text("CREATE UNIQUE INDEX IF NOT EXISTS ix_submitted_papers_paper_id ON submitted_papers(paper_id)"))
        db.session.commit()
    except Exception:
        db.session.rollback()


def _generate_submission_paper_id(submission_id=None):
    current_year = datetime.now().year
    if submission_id is None:
        latest_paper = SubmittedPaper.query.order_by(SubmittedPaper.id.desc()).first()
        submission_id = latest_paper.id + 1 if latest_paper else 1
    return f"JRN-{current_year}-{int(submission_id):04d}"


# Automatically create tables and admin user
with app.app_context():
    db.create_all()
    _ensure_missing_columns()
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
    current_user = None
    if "username" in session:
        current_user = User.query.filter_by(username=session["username"]).first()
    return dict(users=users, session=session, current_user=current_user)


@app.context_processor
def inject_contacts():
    contact = ContactDetail.query.first()
    return dict(contact=contact)


def delete_session_if_user_not_exists(current_user):
    if not current_user:
        session.pop("username", None)
        session.pop("user_id", None)
        session.pop("role", None)
        flash("User session expired. Please log in again.", "danger")
        return True
    return False


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
        current_user = User.query.filter_by(username=session["username"]).first()
        if delete_session_if_user_not_exists(current_user):
            return redirect(url_for("login"))
        if not current_user or current_user.role != "admin":
            flash("Admin access required.", "danger")
            return redirect(url_for("dashboard"))
        return fn(*args, **kwargs)

    return wrapper


def approver_or_admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if "username" not in session:
            flash("Please log in first.", "warning")
            return redirect(url_for("login"))
        current_user = User.query.filter_by(username=session["username"]).first()
        if delete_session_if_user_not_exists(current_user):
            return redirect(url_for("login"))
        if not current_user or current_user.role not in ("admin", "approver"):
            flash("Access restricted. Only Admin or Approver roles can access this page.", "danger")
            return redirect(url_for("student_dashboard"))
        return fn(*args, **kwargs)

    return wrapper


def paper_moderation_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if "username" not in session:
            flash("Please log in first.", "warning")
            return redirect(url_for("login"))
        current_user = User.query.filter_by(username=session["username"]).first()
        if delete_session_if_user_not_exists(current_user):
            return redirect(url_for("login"))
        if not current_user or current_user.role not in ("admin", "approver", "reviewer"):
            flash("Access restricted. Only Admin, Approver, or Reviewer roles can access this page.", "danger")
            return redirect(url_for("student_dashboard"))
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
    contact = (
        ContactDetail.query.join(JournalMaster)
        .filter(JournalMaster.journal_id == "001")
        .order_by(ContactDetail.id.desc())
        .first()
    )
    # Latest 3 issues
    latest_issues = (
        db.session.query(
            ResearchPaper.year,
            ResearchPaper.volume,
            ResearchPaper.issue
        )
        .join(JournalMaster)
        .filter(JournalMaster.journal_id == "001")
        .distinct()
        .order_by(
            ResearchPaper.year.desc(),
            ResearchPaper.volume.desc(),
            ResearchPaper.issue.desc()
        )
        .limit(1)
        .all()
    )

    # Fetch all papers from those 3 issues
    papers = (
        ResearchPaper.query.join(JournalMaster)
        .filter(
            JournalMaster.journal_id == "001",
            tuple_(
                ResearchPaper.year,
                ResearchPaper.volume,
                ResearchPaper.issue
            ).in_(latest_issues)
        )
        .order_by(
            ResearchPaper.year.desc(),
            ResearchPaper.volume.desc(),
            ResearchPaper.issue.desc(),
            ResearchPaper.id.desc()
        )
        .all()
    )
    return render_template(
        "cibdi/Current_issue.html",
        papers=papers,
        contact=contact
    )


@app.route("/cibdi/archive")
def cibdi_archive():
    papers = (
        ResearchPaper.query.join(JournalMaster)
        .filter(
            JournalMaster.journal_id == "001"
        )
        .order_by(
            ResearchPaper.year.desc(),
            ResearchPaper.volume.desc(),
            ResearchPaper.issue.desc(),
            ResearchPaper.id.desc()
        )
        .all()
    )
    contact = (
        ContactDetail.query.join(JournalMaster)
        .filter(JournalMaster.journal_id == "001")
        .order_by(ContactDetail.id.desc())
        .first()
    )
    grouped_papers = defaultdict(list)

    for paper in papers:
        year = paper.year if paper.year else "Unknown"
        volume = paper.volume if paper.volume else "Unknown"
        grouped_papers[(year, volume)].append(paper)

    grouped_papers = dict(
        sorted(
            grouped_papers.items(),
            key=lambda x: x[0] if isinstance(x[0], int) else 0,
            reverse=True
        )
    )

    return render_template(
        "cibdi/archive.html",
        grouped_papers=grouped_papers,
        total_papers=len(papers),
        contact=contact
    )


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
    # Latest 3 issues
    latest_issues = (
        db.session.query(
            ResearchPaper.year,
            ResearchPaper.volume,
            ResearchPaper.issue
        )
        .join(JournalMaster)
        .filter(JournalMaster.journal_id == "002")
        .distinct()
        .order_by(
            ResearchPaper.year.desc(),
            ResearchPaper.volume.desc(),
            ResearchPaper.issue.desc()
        )
        .limit(1)
        .all()
    )

    # Fetch all papers from those 3 issues
    papers = (
        ResearchPaper.query.join(JournalMaster)
        .filter(
            JournalMaster.journal_id == "002",
            tuple_(
                ResearchPaper.year,
                ResearchPaper.volume,
                ResearchPaper.issue
            ).in_(latest_issues)
        )
        .order_by(
            ResearchPaper.year.desc(),
            ResearchPaper.volume.desc(),
            ResearchPaper.issue.desc(),
            ResearchPaper.id.desc()
        )
        .all()
    )
    return render_template(
        "crin/Current_issue.html",
        papers=papers,
        contact=contact
    )


@app.route("/crin/archive")
def crin_archive():
    papers = (
        ResearchPaper.query.join(JournalMaster)
        .filter(
            JournalMaster.journal_id == "002"
        )
        .order_by(
            ResearchPaper.year.desc(),
            ResearchPaper.volume.desc(),
            ResearchPaper.issue.desc(),
            ResearchPaper.id.desc()
        )
        .all()
    )
    contact = (
        ContactDetail.query.join(JournalMaster)
        .filter(JournalMaster.journal_id == "002")
        .order_by(ContactDetail.id.desc())
        .first()
    )
    grouped_papers = defaultdict(list)

    for paper in papers:
        year = paper.year if paper.year else "Unknown"
        volume = paper.volume if paper.volume else "Unknown"
        grouped_papers[(year, volume)].append(paper)

    grouped_papers = dict(
        sorted(
            grouped_papers.items(),
            key=lambda x: x[0] if isinstance(x[0], int) else 0,
            reverse=True
        )
    )

    return render_template(
        "crin/archive.html",
        grouped_papers=grouped_papers,
        total_papers=len(papers),
        contact=contact
    )


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
    # Latest 3 issues
    latest_issues = (
        db.session.query(
            ResearchPaper.year,
            ResearchPaper.volume,
            ResearchPaper.issue
        )
        .join(JournalMaster)
        .filter(JournalMaster.journal_id == "003")
        .distinct()
        .order_by(
            ResearchPaper.year.desc(),
            ResearchPaper.volume.desc(),
            ResearchPaper.issue.desc()
        )
        .limit(1)
        .all()
    )

    # Fetch all papers from those 3 issues
    papers = (
        ResearchPaper.query.join(JournalMaster)
        .filter(
            JournalMaster.journal_id == "003",
            tuple_(
                ResearchPaper.year,
                ResearchPaper.volume,
                ResearchPaper.issue
            ).in_(latest_issues)
        )
        .order_by(
            ResearchPaper.year.desc(),
            ResearchPaper.volume.desc(),
            ResearchPaper.issue.desc(),
            ResearchPaper.id.desc()
        )
        .all()
    )
    return render_template(
        "faai/Current_issue.html",
        papers=papers,
        contact=contact
    )


@app.route("/faai/archive")
def faai_archive():
    papers = (
        ResearchPaper.query.join(JournalMaster)
        .filter(
            JournalMaster.journal_id == "003"
        )
        .order_by(
            ResearchPaper.year.desc(),
            ResearchPaper.volume.desc(),
            ResearchPaper.issue.desc(),
            ResearchPaper.id.desc()
        )
        .all()
    )
    contact = (
        ContactDetail.query.join(JournalMaster)
        .filter(JournalMaster.journal_id == "003")
        .order_by(ContactDetail.id.desc())
        .first()
    )
    grouped_papers = defaultdict(list)

    for paper in papers:
        year = paper.year if paper.year else "Unknown"
        volume = paper.volume if paper.volume else "Unknown"
        grouped_papers[(year, volume)].append(paper)

    grouped_papers = dict(
        sorted(
            grouped_papers.items(),
            key=lambda x: x[0] if isinstance(x[0], int) else 0,
            reverse=True
        )
    )

    return render_template(
        "faai/archive.html",
        grouped_papers=grouped_papers,
        total_papers=len(papers),
        contact=contact
    )


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
    # Latest 3 issues
    latest_issues = (
        db.session.query(
            ResearchPaper.year,
            ResearchPaper.volume,
            ResearchPaper.issue
        )
        .join(JournalMaster)
        .filter(JournalMaster.journal_id == "004")
        .distinct()
        .order_by(
            ResearchPaper.year.desc(),
            ResearchPaper.volume.desc(),
            ResearchPaper.issue.desc()
        )
        .limit(1)
        .all()
    )

    # Fetch all papers from those 3 issues
    papers = (
        ResearchPaper.query.join(JournalMaster)
        .filter(
            JournalMaster.journal_id == "004",
            tuple_(
                ResearchPaper.year,
                ResearchPaper.volume,
                ResearchPaper.issue
            ).in_(latest_issues)
        )
        .order_by(
            ResearchPaper.year.desc(),
            ResearchPaper.volume.desc(),
            ResearchPaper.issue.desc(),
            ResearchPaper.id.desc()
        )
        .all()
    )
    return render_template(
        "feri/Current_issue.html",
        papers=papers,
        contact=contact
    )


@app.route("/feri/archive")
def feri_archive():
    papers = (
        ResearchPaper.query.join(JournalMaster)
        .filter(
            JournalMaster.journal_id == "004"
        )
        .order_by(
            ResearchPaper.year.desc(),
            ResearchPaper.volume.desc(),
            ResearchPaper.issue.desc(),
            ResearchPaper.id.desc()
        )
        .all()
    )
    contact = (
        ContactDetail.query.join(JournalMaster)
        .filter(JournalMaster.journal_id == "004")
        .order_by(ContactDetail.id.desc())
        .first()
    )
    grouped_papers = defaultdict(list)

    for paper in papers:
        year = paper.year if paper.year else "Unknown"
        volume = paper.volume if paper.volume else "Unknown"
        grouped_papers[(year, volume)].append(paper)

    grouped_papers = dict(
        sorted(
            grouped_papers.items(),
            key=lambda x: x[0] if isinstance(x[0], int) else 0,
            reverse=True
        )
    )

    return render_template(
        "feri/archive.html",
        grouped_papers=grouped_papers,
        total_papers=len(papers),
        contact=contact
    )


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
    contact = (
        ContactDetail.query.join(JournalMaster)
        .filter(JournalMaster.journal_id == "005")
        .order_by(ContactDetail.id.desc())
        .first()
    )
    # Latest 3 issues
    latest_issues = (
        db.session.query(
            ResearchPaper.year,
            ResearchPaper.volume,
            ResearchPaper.issue
        )
        .join(JournalMaster)
        .filter(JournalMaster.journal_id == "005")
        .distinct()
        .order_by(
            ResearchPaper.year.desc(),
            ResearchPaper.volume.desc(),
            ResearchPaper.issue.desc()
        )
        .limit(1)
        .all()
    )

    # Fetch all papers from those 3 issues
    papers = (
        ResearchPaper.query.join(JournalMaster)
        .filter(
            JournalMaster.journal_id == "005",
            tuple_(
                ResearchPaper.year,
                ResearchPaper.volume,
                ResearchPaper.issue
            ).in_(latest_issues)
        )
        .order_by(
            ResearchPaper.year.desc(),
            ResearchPaper.volume.desc(),
            ResearchPaper.issue.desc(),
            ResearchPaper.id.desc()
        )
        .all()
    )
    return render_template(
        "fhim/Current_issue.html",
        papers=papers,
        contact=contact
    )


@app.route("/fhim/archive")
def fhim_archive():
    papers = (
        ResearchPaper.query.join(JournalMaster)
        .filter(
            JournalMaster.journal_id == "005"
        )
        .order_by(
            ResearchPaper.year.desc(),
            ResearchPaper.volume.desc(),
            ResearchPaper.issue.desc(),
            ResearchPaper.id.desc()
        )
        .all()
    )
    contact = (
        ContactDetail.query.join(JournalMaster)
        .filter(JournalMaster.journal_id == "005")
        .order_by(ContactDetail.id.desc())
        .first()
    )
    grouped_papers = defaultdict(list)

    for paper in papers:
        year = paper.year if paper.year else "Unknown"
        volume = paper.volume if paper.volume else "Unknown"
        grouped_papers[(year, volume)].append(paper)

    grouped_papers = dict(
        sorted(
            grouped_papers.items(),
            key=lambda x: x[0] if isinstance(x[0], int) else 0,
            reverse=True
        )
    )

    return render_template(
        "fhim/archive.html",
        grouped_papers=grouped_papers,
        total_papers=len(papers),
        contact=contact
    )


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

# Helper to send email OTP
def send_otp_email(to_email, otp_code):
    try:
        msg = Message(
            "Email Verification Code - Curevita Research",
            recipients=[to_email]
        )
        msg.body = f"Hello,\n\nYour OTP for account registration verification is: {otp_code}\nThis OTP is valid for 10 minutes.\n\nThank you,\nCurevita Research Team"
        mail.send(msg)
        return True
    except Exception as e:
        print(f"Mail send error: {e}")
        return False


# ----------------------------------
# Signup Route
# ----------------------------------
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if "username" in session:
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        name = (request.form.get("name") or "").strip()
        username = (request.form.get("username") or "").strip()
        email = (request.form.get("email") or "").strip().lower()
        password = request.form.get("password") or ""

        if not username or not email or not password:
            flash("Username, email, and password are required.", "danger")
            return redirect(url_for("signup"))

        # Check existing user
        existing_user_by_email = User.query.filter_by(email=email).first()
        existing_user_by_username = User.query.filter_by(username=username).first()

        if existing_user_by_email and existing_user_by_email.is_verified:
            flash("An account with this email already exists. Please log in.", "warning")
            return redirect(url_for("login"))

        if existing_user_by_username and (existing_user_by_email is None or existing_user_by_username.id != existing_user_by_email.id):
            flash("Username already taken. Please choose another.", "danger")
            return redirect(url_for("signup"))

        if existing_user_by_email and not existing_user_by_email.is_verified:
            user = existing_user_by_email
            user.name = name or user.name or username
            user.username = username
            user.set_password(password)
        else:
            user = User(
                username=username,
                name=name or username,
                email=email,
                role="user",
                is_verified=False
            )
            user.set_password(password)
            db.session.add(user)

        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            flash("Username or email already exists.", "danger")
            return redirect(url_for("signup"))

        # Generate 6-digit OTP
        otp_code = str(random.randint(100000, 999999))
        expires_at = datetime.now() + timedelta(minutes=10)

        # Deactivate old OTPs
        OTPVerification.query.filter_by(user_id=user.id, is_used=False).update({"is_used": True})

        otp_record = OTPVerification(
            user_id=user.id,
            otp_code=otp_code,
            expires_at=expires_at,
            is_used=False
        )
        db.session.add(otp_record)
        db.session.commit()

        # Send email OTP
        email_sent = send_otp_email(user.email, otp_code)
        session["pending_user_id"] = user.id

        if email_sent:
            flash(f"Verification OTP sent to {user.email}. Please enter it below.", "info")
        else:
            # flash(f"OTP generated: {otp_code} (Mail server offline/dev mode). Please enter OTP to verify.", "warning")
            flash(f"OTP generation Failed (Mail server offline/dev mode).", "danger")

        return redirect(url_for("verify_otp"))

    return render_template("signup.html")


# ----------------------------------
# Verify OTP Route
# ----------------------------------
@app.route("/verify-otp", methods=["GET", "POST"])
def verify_otp():
    user_id = session.get("pending_user_id")
    if not user_id:
        flash("Session expired. Please signup again.", "warning")
        return redirect(url_for("signup"))

    user = User.query.get(user_id)
    if not user:
        flash("User not found.", "danger")
        return redirect(url_for("signup"))

    if request.method == "POST":
        entered_otp = (request.form.get("otp") or "").strip()
        otp_entry = OTPVerification.query.filter_by(
            user_id=user.id,
            otp_code=entered_otp,
            is_used=False
        ).order_by(OTPVerification.created_at.desc()).first()

        if otp_entry and otp_entry.is_valid():
            user.is_verified = True
            otp_entry.is_used = True
            db.session.commit()

            session.pop("pending_user_id", None)
            session["username"] = user.username
            session["user_id"] = user.id
            session["role"] = user.role

            flash("Email verified successfully! Welcome.", "success")
            return redirect(url_for("student_dashboard"))
        else:
            flash("Invalid or expired OTP. Please try again or request a resend.", "danger")

    return render_template("verify_otp.html", user=user)

# =========================================================
# 30 SECOND RESEND COOLDOWN
# =========================================================
COOLDOWN_SECONDS = 30

# ----------------------------------
# Resend OTP Route
# ----------------------------------
@app.route("/resend-otp")
def resend_otp():
    user_id = session.get("pending_user_id")
    if not user_id:
        flash("Session expired. Please signup again.", "warning")
        return redirect(url_for("signup"))

    user = User.query.get(user_id)
    if not user:
        flash("User not found.", "danger")
        return redirect(url_for("signup"))

    now = datetime.now()
    last_resend = session.get("otp_last_resend")
    if last_resend:
        try:
            last_resend_time = datetime.fromisoformat(last_resend)
            elapsed_seconds = (now - last_resend_time).total_seconds()
            if elapsed_seconds < COOLDOWN_SECONDS:
                remaining_seconds = (COOLDOWN_SECONDS - int(elapsed_seconds))
                flash(f"Please wait {remaining_seconds} seconds before requesting another OTP.", "warning")
                return redirect(url_for("verify_otp"))
        except (ValueError, TypeError):
            # Invalid/old session value.
            # Remove it and continue with resend.
            session.pop("otp_last_resend", None)

    OTPVerification.query.filter_by(user_id=user.id, is_used=False).update({"is_used": True})

    otp_code = str(random.randint(100000, 999999))
    expires_at = (now + timedelta(minutes=10))
    otp_record = OTPVerification(
        user_id=user.id,
        otp_code=otp_code,
        expires_at=expires_at,
        is_used=False
    )
    db.session.add(otp_record)
    session["otp_last_resend"] = (now.isoformat())
    db.session.commit()

    email_sent = send_otp_email(user.email, otp_code)
    if email_sent:
        flash(f"A new OTP has been sent to {user.email}.", "info")
    else:
        # flash(f"New OTP generated: {otp_code} (Mail server offline/dev mode).", "warning")
        flash(f"OTP generation Failed (Mail server offline/dev mode).", "danger")

    return redirect(url_for("verify_otp"))


# ----------------------------------
# Login Route
# ----------------------------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if "username" in session:
        return redirect(url_for("student_dashboard"))

    if request.method == "POST":
        login_input = (request.form.get("username") or "").strip()
        password = request.form.get("password") or ""

        user = User.query.filter(
            (User.username == login_input) | (User.email == login_input.lower())
        ).first()

        if user and user.check_password(password):
            session["username"] = user.username
            session["user_id"] = user.id
            session["role"] = user.role
            flash("Login successful!", "success")

            if user.role in ("admin", "approver", "reviewer"):
                return redirect(url_for("admin_papers"))
            return redirect(url_for("student_dashboard"))

        flash("Invalid email/username or password", "danger")
    return render_template("login.html")


@app.route("/logout")
@login_required
def logout():
    session.pop("username", None)
    session.pop("user_id", None)
    session.pop("role", None)
    flash("You have been logged out", "info")
    return redirect(url_for("login"))


@app.route("/forgot_password", methods=["GET", "POST"])
def forgot_password():
    if request.method == "POST":
        email = (request.form.get("email") or "").strip()
        user = User.query.filter_by(email=email).first()
        if not user:
            flash("Email not found.", "danger")
            return redirect(url_for("forgot_password"))

        temp_password = secrets.token_urlsafe(8)
        user.set_password(temp_password)
        db.session.commit()
        try:
            msg = Message("Password Reset", recipients=[email])
            msg.body = f"Your temporary password is: {temp_password}\nPlease change it after login."
            mail.send(msg)
            flash("Temporary password sent to your email.", "success")
        except Exception:
            flash(f"Temporary password generated: {temp_password} (Could not send email).", "warning")
        return redirect(url_for("login"))
    return render_template("forgot_password.html")


# ----------------------------------
# Student Dashboard & Paper Submissions
# ----------------------------------
@app.route("/student/dashboard", methods=["GET", "POST"])
@login_required
def student_dashboard():
    current_user = User.query.filter_by(username=session["username"]).first()
    if delete_session_if_user_not_exists(current_user):
        return redirect(url_for("login"))

    if request.method == "POST":
        title = (request.form.get("title") or "").strip()
        abstract = (request.form.get("abstract") or "").strip()
        journal_id = request.form.get("journal_id", type=int)
        paper_type = (request.form.get("paper_type") or "Original Research").strip()
        orcid = (request.form.get("orcid") or "").strip()
        is_paid = True if request.form.get("is_paid") == "on" else False
        citation = (request.form.get("citation") or "").strip()

        # Extract Authors Details (1 to 10 authors)
        author_names = request.form.getlist("author_name[]")
        author_designations = request.form.getlist("author_designation[]")
        author_affiliations = request.form.getlist("author_affiliation[]")
        author_emails = request.form.getlist("author_email[]")
        corresponding_idx = request.form.get("corresponding_author_index", type=int, default=0)

        authors_list = []
        author_names_clean = []
        corresponding_author_str = ""

        for idx in range(len(author_names)):
            name = (author_names[idx] or "").strip()
            desig = (author_designations[idx] or "").strip() if idx < len(author_designations) else ""
            affil = (author_affiliations[idx] or "").strip() if idx < len(author_affiliations) else ""
            email = (author_emails[idx] or "").strip() if idx < len(author_emails) else ""

            if name:
                author_names_clean.append(name)
                is_corr = (idx == corresponding_idx)
                if is_corr:
                    corresponding_author_str = f"{name} ({email})" if email else name
                
                authors_list.append({
                    "name": name,
                    "designation": desig,
                    "affiliation": affil,
                    "email": email,
                    "is_corresponding": is_corr
                })

        comma_separated_authors = ", ".join(author_names_clean) if author_names_clean else (current_user.name or current_user.username)

        file = request.files.get("paper_file")
        if not title or not abstract or not file:
            flash("Please fill in all required fields and select a PDF file.", "danger")
            return redirect(url_for("student_dashboard"))

        paper_file_size = get_uploaded_file_size(file)
        if paper_file_size > MAX_PAPER_FILE_SIZE_BYTES:
            flash("Paper PDF file must be 5 MB or smaller. Please compress the file and try again.", "danger")
            return redirect(url_for("student_dashboard"))

        # Payment screenshot file handling if paid toggle is on
        payment_filename = None
        if is_paid:
            pay_file = request.files.get("payment_screenshot")
            if pay_file and pay_file.filename:
                pay_file_size = get_uploaded_file_size(pay_file)
                if pay_file_size > MAX_PAYMENT_FILE_SIZE_BYTES:
                    flash("Payment screenshot must be 1 MB or smaller. Please upload a smaller image/receipt.", "danger")
                    return redirect(url_for("student_dashboard"))

                pay_fn = secure_filename(pay_file.filename)
                pay_unique = f"payment_{current_user.id}_{int(datetime.now().timestamp())}_{pay_fn}"
                pay_dir = os.path.join(app.root_path, "static", "assets", "img", "payments")
                os.makedirs(pay_dir, exist_ok=True)
                saved_pay_path = os.path.join(pay_dir, pay_unique)
                pay_file.save(saved_pay_path)
                payment_filename = f"payments/{pay_unique}"
            else:
                flash("Please upload the payment screenshot as the 'Paid' toggle is turned ON.", "danger")
                return redirect(url_for("student_dashboard"))

        if file and file.filename.lower().endswith(".pdf"):
            filename = secure_filename(file.filename)
            unique_filename = f"{current_user.id}_{int(datetime.now().timestamp())}_{filename}"
            upload_dir = os.path.join(app.root_path, "static", "assets", "pdf", "submissions")
            os.makedirs(upload_dir, exist_ok=True)
            saved_path = os.path.join(upload_dir, unique_filename)
            file.save(saved_path)

            rel_pdf_filename = f"submissions/{unique_filename}"
            submission_paper_id = _generate_submission_paper_id()

            new_paper = SubmittedPaper(
                paper_id=submission_paper_id,
                user_id=current_user.id,
                journal_id=journal_id,
                title=title,
                abstract=abstract,
                pdf_filename=rel_pdf_filename,
                authors=comma_separated_authors,
                authors_details_json=json.dumps(authors_list),
                corresponding_author=corresponding_author_str,
                orcid=orcid,
                paper_type=paper_type,
                is_paid=is_paid,
                payment_screenshot=payment_filename,
                citation=citation,
                status="pending",
                workflow_status="under_review"
            )
            db.session.add(new_paper)
            db.session.commit()

            flash("Paper submitted successfully with author details! It is now pending review.", "success")
            return redirect(url_for("student_dashboard"))
        else:
            flash("Only PDF files are allowed for paper upload.", "danger")
            return redirect(url_for("student_dashboard"))

    user_papers = SubmittedPaper.query.filter_by(user_id=current_user.id).order_by(SubmittedPaper.submitted_at.desc()).all()
    journals = JournalMaster.query.filter_by(status=True).all()
    journals_map = {journal.journal_id: f"{journal.short_name.lower()}_current_issue" for journal in journals}

    return render_template("student_dashboard.html", papers=user_papers, journals=journals, user=current_user, journals_map=journals_map, paper_status_labels=PAPER_STATUS_LABELS)


# Edit & Resubmit a Submitted Paper (only allowed when paper.status == 'rejected')
@app.route('/submitted_paper/<int:paper_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_submitted_paper(paper_id):
    current_user = User.query.filter_by(username=session['username']).first()
    if delete_session_if_user_not_exists(current_user):
        return redirect(url_for("login"))
    paper = SubmittedPaper.query.get_or_404(paper_id)

    # Only owner can edit
    if paper.user_id != current_user.id:
        flash('You are not authorized to edit this submission.', 'danger')
        return redirect(url_for('student_dashboard'))

    # Only allow editing when rejected
    if paper.status != 'rejected':
        flash('Only rejected papers can be edited and resubmitted.', 'warning')
        return redirect(url_for('student_dashboard'))

    if request.method == 'POST':
        # Basic fields
        title = (request.form.get('title') or '').strip()
        abstract = (request.form.get('abstract') or '').strip()
        journal_id = request.form.get('journal_id', type=int)
        paper_type = (request.form.get('paper_type') or paper.paper_type or 'Original Research').strip()
        orcid = (request.form.get('orcid') or '').strip()
        is_paid = True if request.form.get('is_paid') == 'on' else False
        citation = (request.form.get('citation') or '').strip()

        # Authors handling (same as submission)
        author_names = request.form.getlist('author_name[]')
        author_designations = request.form.getlist('author_designation[]')
        author_affiliations = request.form.getlist('author_affiliation[]')
        author_emails = request.form.getlist('author_email[]')
        corresponding_idx = request.form.get('corresponding_author_index', type=int, default=0)

        authors_list = []
        author_names_clean = []
        corresponding_author_str = ''
        for idx in range(len(author_names)):
            name = (author_names[idx] or '').strip()
            desig = (author_designations[idx] or '').strip() if idx < len(author_designations) else ''
            affil = (author_affiliations[idx] or '').strip() if idx < len(author_affiliations) else ''
            email = (author_emails[idx] or '').strip() if idx < len(author_emails) else ''
            if name:
                author_names_clean.append(name)
                is_corr = (idx == corresponding_idx)
                if is_corr:
                    corresponding_author_str = f"{name} ({email})" if email else name
                authors_list.append({
                    'name': name,
                    'designation': desig,
                    'affiliation': affil,
                    'email': email,
                    'is_corresponding': is_corr
                })

        comma_separated_authors = ', '.join(author_names_clean) if author_names_clean else (current_user.name or current_user.username)

        # Payment screenshot handling
        payment_filename = paper.payment_screenshot
        if is_paid:
            pay_file = request.files.get('payment_screenshot')
            if pay_file and pay_file.filename:
                pay_file_size = get_uploaded_file_size(pay_file)
                if pay_file_size > MAX_PAYMENT_FILE_SIZE_BYTES:
                    flash("Payment screenshot must be 1 MB or smaller. Please upload a smaller image/receipt.", 'danger')
                    return redirect(request.url)

                pay_fn = secure_filename(pay_file.filename)
                pay_unique = f"payment_{current_user.id}_{int(datetime.now().timestamp())}_{pay_fn}"
                pay_dir = os.path.join(app.root_path, 'static', 'assets', 'img', 'payments')
                os.makedirs(pay_dir, exist_ok=True)
                saved_pay_path = os.path.join(pay_dir, pay_unique)
                pay_file.save(saved_pay_path)
                payment_filename = f"payments/{pay_unique}"

                if paper.payment_screenshot:
                    try:
                        old_pay_path = os.path.join(app.root_path, 'static', 'assets', 'img', paper.payment_screenshot)
                        if os.path.exists(old_pay_path):
                            os.remove(old_pay_path)
                    except Exception:
                        app.logger.exception('Could not remove old payment screenshot')
        else:
            if paper.payment_screenshot:
                try:
                    old_pay_path = os.path.join(app.root_path, 'static', 'assets', 'img', paper.payment_screenshot)
                    if os.path.exists(old_pay_path):
                        os.remove(old_pay_path)
                except Exception:
                    app.logger.exception('Could not remove old payment screenshot')
            payment_filename = None

        # PDF replacement handling
        file = request.files.get('paper_file')
        if file and file.filename:
            file_size = get_uploaded_file_size(file)
            if file_size > MAX_PAPER_FILE_SIZE_BYTES:
                flash("Paper PDF file must be 5 MB or smaller. Please compress the file and try again.", 'danger')
                return redirect(request.url)

        if file and file.filename.lower().endswith('.pdf'):
            filename = secure_filename(file.filename)
            unique_filename = f"{current_user.id}_{int(datetime.now().timestamp())}_{filename}"
            upload_dir = os.path.join(app.root_path, 'static', 'assets', 'pdf', 'submissions')
            os.makedirs(upload_dir, exist_ok=True)
            saved_path = os.path.join(upload_dir, unique_filename)
            file.save(saved_path)
            rel_pdf_filename = f"submissions/{unique_filename}"

            # remove old file if exists
            if paper.pdf_filename:
                try:
                    old_path = os.path.join(app.root_path, 'static', 'assets', 'pdf', paper.pdf_filename)
                    if os.path.exists(old_path):
                        os.remove(old_path)
                except Exception:
                    app.logger.exception('Could not remove old submitted PDF')

            paper.pdf_filename = rel_pdf_filename

        # Update DB fields
        paper.title = title or paper.title
        paper.abstract = abstract or paper.abstract
        paper.journal_id = journal_id or paper.journal_id
        paper.authors = comma_separated_authors
        paper.authors_details_json = json.dumps(authors_list)
        paper.corresponding_author = corresponding_author_str
        paper.orcid = orcid
        paper.paper_type = paper_type
        paper.is_paid = is_paid
        paper.payment_screenshot = payment_filename
        paper.citation = citation

        # Reset status to pending and clear rejection
        paper.status = 'pending'
        paper.workflow_status = 'under_review'
        paper.rejection_reason = None
        db.session.commit()

        flash('Paper updated and resubmitted. It is now pending review.', 'success')
        return redirect(url_for('student_dashboard'))

    # GET -> render edit form
    journals = JournalMaster.query.filter_by(status=True).all()
    try:
        authors_details = json.loads(paper.authors_details_json) if paper.authors_details_json else []
    except Exception:
        authors_details = []

    return render_template('edit_submitted_paper.html', paper=paper, journals=journals, authors_details=authors_details)


# ----------------------------------
# Admin & Approver Panel - Paper Verification & Dropdown User Filter
# ----------------------------------
@app.route("/admin/papers", methods=["GET"])
@paper_moderation_required
def admin_papers():
    page = request.args.get("page", 1, type=int)
    selected_user_id = request.args.get("user_id", type=int)
    search_query = (request.args.get("q") or "").strip()
    status_filter = (request.args.get("status") or "").strip().lower()
    current_user = User.query.filter_by(username=session["username"]).first()

    # Fetch users who submitted papers for dropdown filter
    submitted_users = User.query.join(SubmittedPaper).group_by(User.id).all()
    if not submitted_users:
        submitted_users = User.query.filter(User.role != 'admin').all()

    query = SubmittedPaper.query
    if current_user.role == "reviewer":
        query = query.filter(SubmittedPaper.status != "approved")
    if selected_user_id:
        query = query.filter_by(user_id=selected_user_id)

    if status_filter in PAPER_STATUS_OPTIONS:
        query = query.filter_by(workflow_status=status_filter)
    elif status_filter in ("pending", "approved", "rejected"):
        query = query.filter_by(status=status_filter)

    if search_query:
        query = query.filter(
            (SubmittedPaper.title.ilike(f"%{search_query}%")) |
            (SubmittedPaper.paper_id.ilike(f"%{search_query}%"))
        )

    pagination = query.order_by(SubmittedPaper.submitted_at.desc()).paginate(page=page, per_page=6, error_out=False)

    return render_template(
        "admin_papers.html",
        papers=pagination.items,
        pagination=pagination,
        users_list=submitted_users,
        selected_user_id=selected_user_id,
        status_filter=status_filter,
        search_query=search_query,
        page=page,
        current_user=current_user,
        paper_status_options=PAPER_STATUS_OPTIONS,
        paper_status_labels=PAPER_STATUS_LABELS,
    )


@app.route("/admin/paper/<int:paper_id>/approve", methods=["POST"])
@approver_or_admin_required
def approve_submitted_paper(paper_id):
    paper = SubmittedPaper.query.get_or_404(paper_id)

    if paper.workflow_status == "paper_published" and paper.status == "approved":
        flash("This paper is already published. Its status is final and cannot be changed again.", "warning")
        return redirect(url_for("admin_papers"))

    workflow_status = (request.form.get("workflow_status") or "").strip().lower()
    if workflow_status not in PAPER_STATUS_OPTIONS:
        flash("Please choose a valid paper workflow status.", "warning")
        return redirect(url_for("admin_papers"))

    volume = request.form.get("volume", type=int)
    issue = request.form.get("issue", type=int)

    if workflow_status == "paper_published":
        if not volume or not issue:
            flash("Please provide both Volume and Issue before publishing the paper.", "warning")
            return redirect(url_for("admin_papers"))

        if paper.journal_id:
            existing_rp = ResearchPaper.query.filter_by(
                title=paper.title,
                journal_id=paper.journal_id,
                volume=volume,
                issue=issue,
                year=datetime.now().year,
            ).first()
            if not existing_rp:
                research_paper = ResearchPaper(
                    title=paper.title,
                    authors=(paper.authors if paper.authors else (paper.user.name or paper.user.username)),
                    volume=volume,
                    issue=issue,
                    year=datetime.now().year,
                    abstract=paper.abstract,
                    pdf_filename=paper.pdf_filename,
                    journal_id=paper.journal_id,
                    citation=paper.citation,
                    is_current=True,
                )
                db.session.add(research_paper)

        paper.status = "approved"
        paper.workflow_status = "paper_published"
        paper.rejection_reason = None
    elif workflow_status == "rejected":
        rejection_reason = (request.form.get("rejection_reason") or "Paper does not meet requirements.").strip()
        paper.status = "rejected"
        paper.workflow_status = "rejected"
        paper.rejection_reason = rejection_reason
    else:
        paper.status = "pending"
        paper.workflow_status = workflow_status
        paper.rejection_reason = None

    db.session.commit()
    if workflow_status == "rejected":
        flash(f"Paper '{paper.title}' has been REJECTED. It cannot be approved in the future.", "warning")
    elif workflow_status == "paper_published":
        flash(f"Paper '{paper.title}' has been published successfully.", "success")
    else:
        flash("Paper workflow status updated successfully.", "success")
    return redirect(url_for("admin_papers"))


@app.route("/admin/paper/<int:paper_id>/reject", methods=["POST"])
@approver_or_admin_required
def reject_submitted_paper(paper_id):
    paper = SubmittedPaper.query.get_or_404(paper_id)
    rejection_reason = (request.form.get("rejection_reason") or "Paper does not meet requirements.").strip()

    paper.status = "rejected"
    paper.workflow_status = "rejected"
    paper.rejection_reason = rejection_reason
    db.session.commit()

    flash(f"Paper '{paper.title}' has been REJECTED. It cannot be approved in the future.", "warning")
    return redirect(url_for("admin_papers"))


@app.route("/admin/paper/<int:paper_id>/update-status", methods=["POST"])
@paper_moderation_required
def update_submitted_paper_status(paper_id):
    paper = SubmittedPaper.query.get_or_404(paper_id)
    current_user = User.query.filter_by(username=session["username"]).first()
    # workflow_status = (request.form.get("workflow_status") or "").strip().lower()

    if current_user.role == "reviewer":
        reviewer_comment = (request.form.get("reviewer_comment") or "").strip()
        if reviewer_comment:
            new_comment = PaperReviewComment(
                paper_id=paper.id,
                reviewer_id=current_user.id,
                comment=reviewer_comment
            )
            db.session.add(new_comment)
            paper.reviewer_comment = reviewer_comment
        db.session.commit()
        flash("Reviewer comment saved successfully.", "success")
        return redirect(url_for("admin_papers"))
    flash("You do not have permission to update the paper status.", "danger")
    return redirect(url_for("admin_papers"))


# ----------------------------------
# Published Approved Papers View (Restricted to Admin & Approver roles with search, filter, pagination)
# ----------------------------------
@app.route("/approved_papers", methods=["GET"])
@paper_moderation_required
def approved_papers():
    page = request.args.get("page", 1, type=int)
    search_query = (request.args.get("q") or "").strip()
    selected_user_id = request.args.get("user_id", type=int)

    query = SubmittedPaper.query.filter_by(status="approved")

    if selected_user_id:
        query = query.filter_by(user_id=selected_user_id)

    if search_query:
        query = query.filter(
            (SubmittedPaper.title.ilike(f"%{search_query}%")) |
            (SubmittedPaper.paper_id.ilike(f"%{search_query}%"))
        )

    # Fetch users who have approved papers for dropdown
    approved_authors = User.query.join(SubmittedPaper).filter(SubmittedPaper.status == "approved").group_by(User.id).all()

    pagination = query.order_by(SubmittedPaper.updated_at.desc()).paginate(page=page, per_page=6, error_out=False)

    return render_template(
        "approved_papers.html",
        papers=pagination.items,
        pagination=pagination,
        approved_authors=approved_authors,
        selected_user_id=selected_user_id,
        search_query=search_query
    )




# ----------------------------------
# Dashboard + User Management
# ----------------------------------
@app.route("/dashboard")
@login_required
def dashboard():
    current_user = User.query.filter_by(username=session["username"]).first()
    if delete_session_if_user_not_exists(current_user):
        return redirect(url_for("login"))
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
        role=role if role in ("admin", "approver", "reviewer", "user") else "user",
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
        user.role = role if role in ("admin", "approver", "reviewer", "user") else "user"
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
    page = request.args.get("page", 1, type=int)
    per_page = 10

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

    pagination = query.order_by(EditorBoard.id.asc()).paginate(page=page, per_page=per_page, error_out=False)
    boards = pagination.items

    return render_template(
        "listedi.html",
        boards=boards,
        journals=journals,
        selected_journal=selected_journal,
        selected_category=selected_category,
        pagination=pagination,
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
    print(f"Contacts fetched: {len(contacts)}")  # Debugging line
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
    page = request.args.get("page", 1, type=int)
    per_page = 10
    current_user = User.query.filter_by(username=session["username"]).first()
    is_admin = current_user.role == "admin"

    pagination = ResearchPaper.query.order_by(ResearchPaper.id.desc()).paginate(page=page, per_page=per_page, error_out=False)
    papers = pagination.items

    return render_template("list_papers.html", papers=papers, pagination=pagination, current_user=current_user, is_admin=is_admin)

# -------------------------
# Research Paper: CRUD (improved)
# -------------------------
import os
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

        # ---------------- Save to DB ----------------
        new_paper = ResearchPaper(
            title=title,
            authors=authors,
            journal_id=journal_id,  # Foreign key
            volume=volume,
            issue=issue,
            year=year,
            abstract=abstract,
            pdf_filename=pdf_filename,
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


@app.route("/api/feedback", methods=["POST"])
def add_feedback():
    data = request.get_json()

    name = data.get("name")
    email = data.get("email")
    subject = data.get("subject", "")
    message = data.get("message", "")

    if not name.strip() or not email.strip() or not message.strip():
        return jsonify({"error": "All required fields must be filled."}), 400

    # Check if user has sent feedback in the last 1 hour
    one_hour_ago = datetime.now() - timedelta(hours=1)
    recent_feedback = UserFeedback.query.filter(
        UserFeedback.email == email,
        UserFeedback.created_at >= one_hour_ago
    ).first()

    if recent_feedback:
        return jsonify({"error": "You can only send feedback once in a hour."}), 429

    # Save feedback in database
    new_feedback = UserFeedback(
        name=name,
        email=email,
        subject=subject,
        message=message
    )
    db.session.add(new_feedback)
    db.session.commit()

    # Send confirmation mail
    try:
        msg = Message(
            subject="Your Contact Request Has Been Received",
            sender="no-reply@yourdomain.com",
            recipients=[email],
        )
        msg.body = f"""
            Dear {name},

            Thank you for reaching out to us!

            We have successfully received your query:
            "{message}"

            Our support team will review it and get back to you shortly.

            Best regards,
            Support Team
            Curevita Journals
        """
        mail.send(msg)
        new_feedback.status = True
        db.session.commit()
    except Exception as e:
        print("Mail sending failed:", e)

    return jsonify({"success": "Query received successfully."}), 201