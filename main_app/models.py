import os
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from main_app.extensions import db


class JournalMaster(db.Model):
    __tablename__ = "journal_master"

    id = db.Column(db.Integer, primary_key=True)
    journal_id = db.Column(
        db.String(50), unique=True, nullable=False
    )
    full_name = db.Column(db.String(250), nullable=False, unique=True)
    short_name = db.Column(db.String(100), nullable=True)
    logo_filename = db.Column(db.String(200), nullable=True)
    contact_email = db.Column(db.String(200), nullable=True)
    status = db.Column(db.Boolean, default=True)
    about = db.Column(db.Text, nullable=True)
    url = db.Column(db.String(300), nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now())

    def __repr__(self):
        return f"<JournalMaster {self.journal_id} - {self.full_name}>"


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    name = db.Column(db.String(150), nullable=True)
    email = db.Column(db.String(200), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(50), default="user")  # 'admin' ya 'user'
    is_verified = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now())

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.username}>"


class OTPVerification(db.Model):
    __tablename__ = 'otp_verifications'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    otp_code = db.Column(db.String(6), nullable=False)
    expires_at = db.Column(db.DateTime, nullable=False)
    is_used = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.now)

    user = db.relationship('User', backref=db.backref('otps', lazy=True, cascade="all, delete-orphan"))

    def is_valid(self):
        return not self.is_used and datetime.now() <= self.expires_at


class SubmittedPaper(db.Model):
    __tablename__ = 'submitted_papers'

    id = db.Column(db.Integer, primary_key=True)
    paper_id = db.Column(db.String(50), unique=True, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    journal_id = db.Column(db.Integer, db.ForeignKey('journal_master.id'), nullable=True)
    title = db.Column(db.String(300), nullable=False)
    abstract = db.Column(db.Text, nullable=False)
    pdf_filename = db.Column(db.String(250), nullable=False)
    
    # Author & Paper Meta Fields
    authors = db.Column(db.Text, nullable=True)  # Comma-separated names of all authors
    authors_details_json = db.Column(db.Text, nullable=True)  # JSON representation of authors
    corresponding_author = db.Column(db.String(250), nullable=True)
    orcid = db.Column(db.String(100), nullable=True)
    paper_type = db.Column(db.String(100), nullable=True)  # 'Original Research', 'Review Paper', 'Short Communication'
    is_paid = db.Column(db.Boolean, default=False)
    payment_screenshot = db.Column(db.String(250), nullable=True)
    citation = db.Column(db.Text, nullable=True)

    status = db.Column(db.String(20), default='pending', nullable=False)  # 'pending', 'approved', 'rejected'
    workflow_status = db.Column(db.String(80), default='under_review', nullable=False)
    reviewer_comment = db.Column(db.Text, nullable=True)
    rejection_reason = db.Column(db.Text, nullable=True)
    final_pdf_filename = db.Column(db.String(250), nullable=True)
    final_approval_requested = db.Column(db.Boolean, default=False)
    author_approval_state = db.Column(db.String(20), default='pending', nullable=True)
    author_approval_comment = db.Column(db.Text, nullable=True)
    submitted_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    user = db.relationship('User', backref=db.backref('submitted_papers', lazy=True, cascade="all, delete-orphan"))
    journal = db.relationship('JournalMaster', backref=db.backref('submitted_papers', lazy=True))
    review_comments = db.relationship('PaperReviewComment', backref='paper', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f"<SubmittedPaper {self.id} - {self.title} ({self.status})>"


class PaperReviewComment(db.Model):
    __tablename__ = 'paper_review_comments'

    id = db.Column(db.Integer, primary_key=True)
    paper_id = db.Column(db.Integer, db.ForeignKey('submitted_papers.id'), nullable=False)
    reviewer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    comment = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    reviewer = db.relationship('User', backref=db.backref('review_comments', lazy=True, cascade='all, delete-orphan'))

    def __repr__(self):
        return f"<PaperReviewComment {self.id} - paper {self.paper_id}>"


class EditorBoard(db.Model):
    __tablename__ = "editor_board"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    designation = db.Column(db.String(250))
    link = db.Column(db.String(250))
    quote = db.Column(db.Text)
    code = db.Column(db.String(500))
    journal_id = db.Column(
        db.Integer, db.ForeignKey("journal_master.id"), nullable=False
    )
    journal = db.relationship("JournalMaster", backref=db.backref("editors", lazy=True))

    def __repr__(self):
        return f"<Editor {self.name} - Journal {self.journal_id}>"


class ContactDetail(db.Model):
    __tablename__ = "contact_detail"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(200), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(500))
    linkedin = db.Column(db.String(500))
    instagram = db.Column(db.String(500))
    facebook = db.Column(db.String(500))
    twitter = db.Column(db.String(500))
    company_website = db.Column(db.String(500))
    youtube_url = db.Column(db.String(500))
    journal_id = db.Column(
        db.Integer, db.ForeignKey("journal_master.id"), nullable=False
    )
    journal = db.relationship(
        "JournalMaster", backref=db.backref("contacts", lazy=True)
    )

    def __repr__(self):
        return f"<ContactDetail {self.id} - {self.name} - Journal {self.journal.full_name}>"


class ResearchPaper(db.Model):
    __tablename__ = "research_paper"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300), nullable=False)
    authors = db.Column(db.String(300), nullable=False)
    volume = db.Column(db.String(50), nullable=True)
    issue = db.Column(db.String(50), nullable=True)
    year = db.Column(db.Integer, nullable=True)
    abstract = db.Column(db.Text, nullable=False)
    pdf_filename = db.Column(db.String(200), nullable=True)
    citation = db.Column(db.Text, nullable=True)
    image_filename = db.Column(db.String(200), nullable=True)
    is_current = db.Column(db.Boolean, default=True)
    is_archive = db.Column(db.Boolean, default=False)
    journal_id = db.Column(
        db.Integer, db.ForeignKey("journal_master.id"), nullable=False
    )
    journal = db.relationship(
        "JournalMaster", backref=db.backref("research_papers", lazy=True)
    )
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now())

    def pdf_path(self):
        if not self.pdf_filename:
            return None
        return os.path.join("static", "assets", "pdf", self.pdf_filename)

    def image_path(self):
        if not self.image_filename:
            return "static/assets/img/default.png"  # fallback default image
        return os.path.join("static", "assets", "img", self.image_filename)

    def __repr__(self):
        return f"<ResearchPaper id={self.id} title={self.title!r}>"


class UserFeedback(db.Model):
    __tablename__ = 'user_feedback'
    
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.Text, nullable=False)
    status = db.Column(db.Boolean, default=False)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    subject = db.Column(db.String(500), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())
    
    def __repr__(self):
        return f"<UserFeedback {self.id} - {self.name} - Email {self.email}>"