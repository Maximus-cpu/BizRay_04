from app import db
import uuid
import re
from datetime import datetime, timedelta, timezone
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import validates

class User(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    email = db.Column(db.String(120), unique=True, nullable=False)
    first_name = db.Column(db.String(80), unique=False, nullable=True)
    last_name = db.Column(db.String(80), unique=False, nullable=True)
    password_hash = db.Column(db.String(255), nullable=False)
    failed_login_attempts = db.Column(db.Integer, default=0)
    account_locked_until = db.Column(db.DateTime(timezone=True), nullable=True)
    created_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    @validates('first_name')
    def validate_first_name(self, key, first_name):
        if first_name is None:
            return None
        if len(first_name) > 80:
            raise ValueError("First name cannot exceed 80 characters")
        return first_name.strip()

    @validates('last_name')
    def validate_last_name(self, key, last_name):
        if last_name is None:
            return None
        if len(last_name) > 80:
            raise ValueError("Last name cannot exceed 80 characters")
        return last_name.strip()

    @validates('email')
    def validate_email(self, key, email):
        """Validate email format"""
        if not email or not email.strip():
            raise ValueError("Email cannot be empty")

        # Email regex validation
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email.strip()):
            raise ValueError("Invalid email format")

        return email.strip().lower()

    def set_password(self, password):
        """Hash and set the user's password with strong validation"""
        # Validate password strength
        if not password:
            raise ValueError("Password cannot be empty")

        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters long")

        if not re.search(r'[A-Z]', password):
            raise ValueError("Password must contain at least one uppercase letter")

        if not re.search(r'[0-9]', password):
            raise ValueError("Password must contain at least one number")

        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            raise ValueError("Password must contain at least one special character")

        # Salted hashing for better security
        self.password_hash = generate_password_hash(password, method='pbkdf2:sha256')

    def check_password(self, password):
        """Check if the provided password matches the hash"""
        return check_password_hash(self.password_hash, password)

    def is_account_locked(self):
        """Check if the account is currently locked"""
        if self.account_locked_until is None:
            return False

        if datetime.now(timezone.utc) < self.account_locked_until:
            return True

        # Lock period expired, reset
        self.account_locked_until = None
        self.failed_login_attempts = 0
        db.session.commit()
        return False

    def record_failed_login(self):
        """Record a failed login attempt and lock if necessary"""
        self.failed_login_attempts += 1

        if self.failed_login_attempts >= 3:
            # Lock account for 15 minutes
            self.account_locked_until = datetime.now(timezone.utc) + timedelta(minutes=15)

        db.session.commit()

    def reset_failed_attempts(self):
        """Reset failed login attempts after successful login"""
        self.failed_login_attempts = 0
        self.account_locked_until = None
        db.session.commit()

    def __repr__(self):
        return f"<User {self.email}>"