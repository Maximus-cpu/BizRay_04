from app import db
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import validates

class User(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    @validates('username')
    def validate_username(self, username):
        """Validate that the username is not empty"""
        if not username or not username.strip():
            raise ValueError("Username cannot be empty")
        return username.strip()

    def set_password(self, password):
        """Hash and set the user's password"""
        if not password or len(password) < 6:
            raise ValueError("Password must be at least 6 characters long")
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Check if the provided password matches the hash"""
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.username}>"