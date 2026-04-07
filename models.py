from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

# ---------------------------------------------------------------------------
# USERS
# ---------------------------------------------------------------------------
class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id         = db.Column(db.Integer, primary_key=True)
    username   = db.Column(db.String(80), unique=True, nullable=False)
    email      = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    role       = db.Column(db.String(20), nullable=False, default='user')  # 'user' | 'admin'
    is_active  = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    reports    = db.relationship('Report', backref='submitter', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def is_admin(self):
        return self.role == 'admin'

    def __repr__(self):
        return f'<User {self.username} [{self.role}]>'


# ---------------------------------------------------------------------------
# DISEASE REFERENCE REGISTRY
# ---------------------------------------------------------------------------
class Disease(db.Model):
    __tablename__ = 'diseases'

    id            = db.Column(db.Integer, primary_key=True)
    name          = db.Column(db.String(120), unique=True, nullable=False)
    category      = db.Column(db.String(50))   # viral/bacterial/fungal/parasitic/other
    description   = db.Column(db.Text)
    is_notifiable = db.Column(db.Boolean, default=False)  # mandatory government reporting
    created_at    = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Disease {self.name}>'


# ---------------------------------------------------------------------------
# REPORTS (core entity)
# ---------------------------------------------------------------------------
class Report(db.Model):
    __tablename__ = 'reports'

    id               = db.Column(db.Integer, primary_key=True)
    user_id          = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    patient_name     = db.Column(db.String(120), nullable=False)
    age              = db.Column(db.Integer, nullable=False)
    disease          = db.Column(db.String(120), nullable=False)
    symptoms         = db.Column(db.Text, nullable=False)
    severity         = db.Column(db.String(20), nullable=False, default='mild')
    location_city    = db.Column(db.String(100))
    location_state   = db.Column(db.String(100))
    location_country = db.Column(db.String(100), default='India')
    latitude         = db.Column(db.Float)
    longitude        = db.Column(db.Float)
    report_date      = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    status           = db.Column(db.String(20), default='pending')  # pending/verified/rejected
    notes            = db.Column(db.Text)
    created_at       = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at       = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def severity_class(self):
        return {
            'mild':     'badge-mild',
            'moderate': 'badge-moderate',
            'severe':   'badge-severe',
            'critical': 'badge-critical',
        }.get(self.severity, 'badge-mild')

    def status_class(self):
        return {
            'pending':  'badge-pending',
            'verified': 'badge-verified',
            'rejected': 'badge-rejected',
        }.get(self.status, 'badge-pending')

    def __repr__(self):
        return f'<Report {self.id} — {self.disease} @ {self.location_city}>'


# ---------------------------------------------------------------------------
# ALERT THRESHOLDS
# ---------------------------------------------------------------------------
class AlertThreshold(db.Model):
    __tablename__ = 'alert_thresholds'

    id        = db.Column(db.Integer, primary_key=True)
    disease   = db.Column(db.String(120), nullable=False)
    location  = db.Column(db.String(200))   # city/state/country — blank = global
    threshold = db.Column(db.Integer, nullable=False, default=10)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Alert {self.disease} >{self.threshold} @ {self.location or "Global"}>'


# ---------------------------------------------------------------------------
# AUDIT LOG
# ---------------------------------------------------------------------------
class AuditLog(db.Model):
    __tablename__ = 'audit_log'

    id           = db.Column(db.Integer, primary_key=True)
    admin_id     = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    action       = db.Column(db.String(50), nullable=False)   # CREATE/UPDATE/DELETE/VERIFY/REJECT
    target_table = db.Column(db.String(50))
    target_id    = db.Column(db.Integer)
    details      = db.Column(db.Text)   # human-readable description
    timestamp    = db.Column(db.DateTime, default=datetime.utcnow)

    admin = db.relationship('User', backref='audit_actions', foreign_keys=[admin_id])

    def __repr__(self):
        return f'<AuditLog {self.action} on {self.target_table}#{self.target_id}>'
