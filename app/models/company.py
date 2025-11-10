from app import db
from sqlalchemy.orm import validates
import re

class Company(db.Model):
    id = db.Column(db.String(7), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    region = db.Column(db.String(100), nullable=False) # region would not be a data field (Could be extracted fro Postal Code)
    address = db.Column(db.String(255), nullable=False) # business address could be null (Postal Code, Country Code, Street)
    legal_form = db.Column(db.String(20), nullable=False) # could be null
    # would add European Unique Identifier EUID (corresponds to FNR with FNR being included inside of it)
    # Optional: short description of company
    # Management: Unlimited liable partner, Limited Partner, Authorized Signatory
    
    # Financial Data: (Not optional)
    revenue = db.Column(db.Float, nullable=False)
    risk_score = db.Column(db.Float, nullable=False)
    industry = db.Column(db.String(50), nullable=False) # would not be a data field
    branch = db.Column(db.String(100), nullable=False) # would not be a data field
    employees_count = db.Column(db.Integer, nullable=False) # optional

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
