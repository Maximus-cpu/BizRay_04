import random
import string
from faker import Faker
from app import db
from app.models.company import Company

fake = Faker('de_AT')  # Austrian locale

# Define Austrian regions with representative cities
AUSTRIAN_REGIONS = {
    "Vienna": ["Vienna"],
    "Lower Austria": ["St. Pölten", "Krems", "Amstetten", "Wr. Neustadt"],
    "Upper Austria": ["Linz", "Wels", "Steyr"],
    "Styria": ["Graz", "Leoben", "Kapfenberg"],
    "Tyrol": ["Innsbruck", "Kufstein", "Lienz"],
    "Carinthia": ["Klagenfurt", "Villach", "Spittal an der Drau"],
    "Salzburg": ["Salzburg", "Hallein", "Zell am See"],
    "Vorarlberg": ["Bregenz", "Dornbirn", "Feldkirch"],
    "Burgenland": ["Eisenstadt", "Oberwart", "Neusiedl am See"]
}

LEGAL_FORMS = ["GmbH", "AG", "KG", "OG", "e.U."]

INDUSTRY_BRANCHES = {
    "Technology": [
        "Software Development", "Mobile Development", "Artificial Intelligence",
        "Cybersecurity", "Cloud Computing", "IT Consulting", "Data Analytics", "E-commerce Solutions"
    ],
    "Finance": [
        "Banking Services", "Investment Management", "Insurance",
        "FinTech Solutions", "Accounting", "Financial Consulting", "Wealth Management"
    ],
    "Healthcare": [
        "Pharmaceuticals", "Medical Devices", "Health IT Systems",
        "Biotechnology", "Clinical Research", "Hospital Management"
    ],
    "Retail": [
        "E-commerce", "Fashion & Apparel", "Food & Beverage",
        "Consumer Electronics", "Home Goods", "Automotive Retail"
    ]
}


def generate_company_id(existing_ids):
    """Generate a unique 1–6 digit + 1 letter company ID."""
    while True:
        num_part = str(random.randint(1, 999999))
        letter_part = random.choice(string.ascii_lowercase)
        company_id = f"{num_part}{letter_part}"
        if company_id not in existing_ids:
            existing_ids.add(company_id)
            return company_id


def seed_companies(count=10100):
    """Seed mock company data into the database."""
    if Company.query.first():
        print("Companies exist — skipping seeding.")
        return

    print(f"Seeding {count} companies...")

    existing_ids = set()
    companies = []

    for _ in range(count):
        # Choose industry and branch
        industry = random.choice(list(INDUSTRY_BRANCHES.keys()))
        branch = random.choice(INDUSTRY_BRANCHES[industry])

        # Choose the region and city consistently
        region = random.choice(list(AUSTRIAN_REGIONS.keys()))
        city = random.choice(AUSTRIAN_REGIONS[region])

        # Build an address that matches that city
        street_address = fake.street_address()
        address = f"{street_address}, {city}, {region}, Austria"

        # Create company
        company = Company(
            id=generate_company_id(existing_ids),
            name=fake.company(),
            region=region,
            address=address,
            legal_form=random.choice(LEGAL_FORMS),
            revenue=round(random.uniform(50000.00, 5000000.00), 2),
            risk_score=round(random.uniform(0.00, 100.00), 2),
            industry=industry,
            branch=branch,
            employees_count=random.randint(5, 5000)
        )
        companies.append(company)

    db.session.bulk_save_objects(companies)
    db.session.commit()

    print(f"Successfully seeded {count} companies.")