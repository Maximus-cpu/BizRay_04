from app import db
from sqlalchemy.orm import validates
import re

class Company(db.Model):
    id = db.Column(db.String(7), primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    @validates('id')
    def validate_id(self, key, company_id):
        """Validate company id: must be max 7 characters long and only a single letter at the end"""

        if not company_id:
            raise ValueError("Company ID cannot be empty")

        if len(company_id) > 7:
            raise ValueError("Company ID cannot exceed 7 characters")

        # 1-6 digits followed by 1 letter
        if not re.match(r'^\d{1,6}[A-Za-z]$', company_id):
            raise ValueError("Company ID must be 1-6 digits followed by 1 letter")

        return company_id

    @validates('name')
    def validate_name(self, key, name_value):
        """Validate company name: must be max 100 characters long and not empty"""
        if not name_value or not name_value.strip():
            raise ValueError("Company name cannot be empty")

        if len(name_value) > 100:
            raise ValueError("Company name cannot exceed 100 characters")

        return name_value.strip()

    def __repr__(self):
        return f"<Company {self.name}>"