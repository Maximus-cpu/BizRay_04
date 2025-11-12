import random
import string
from faker import Faker
from app import db
from app.models.company import Company

fake = Faker('de_AT')  # Austrian locale

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

LEGAL_FORMS = ["GmbH", "AG", "OG", "KG", "GmbH & Co KG", "e.U."]

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


def generate_financials():
    """Generate random financial data for a company."""

    # Scale company size
    scale = random.uniform(0.5, 20)  # 0.5 small, 20 large corporation

    # Base totals
    balance_sheet_total = random.uniform(1_000_000, 500_000_000) * scale

    # Split into fixed and current assets
    fixed_assets = balance_sheet_total * random.uniform(0.3, 0.7)
    current_assets = balance_sheet_total - fixed_assets

    # Break down fixed assets
    intangible_assets = fixed_assets * random.uniform(0.05, 0.25)
    tangible_assets = fixed_assets * random.uniform(0.5, 0.8)
    financial_assets = fixed_assets - intangible_assets - tangible_assets

    # Break down current assets
    stockpiles = current_assets * random.uniform(0.05, 0.3)
    receivables = current_assets * random.uniform(0.2, 0.4)
    securities_and_shares = current_assets * random.uniform(0.05, 0.2)
    cash_and_bank_balances = current_assets - stockpiles - receivables - securities_and_shares

    prepaid_expenses = balance_sheet_total * random.uniform(0.005, 0.02)

    # Liabilities and equity split
    equity = balance_sheet_total * random.uniform(0.3, 0.7)
    liabilities = balance_sheet_total - equity

    # Break down equity
    required_share_capital = equity * random.uniform(0.1, 0.3)
    capital_reserves = equity * random.uniform(0.05, 0.25)
    retained_earnings = equity * random.uniform(0.1, 0.4)
    balance_sheet_profit = equity * random.uniform(0.01, 0.1)
    profit_carried_forward = equity - (
        required_share_capital + capital_reserves + retained_earnings + balance_sheet_profit
    )

    # Break down liabilities
    long_term_liabilities = liabilities * random.uniform(0.3, 0.7)
    accruals = liabilities * random.uniform(0.05, 0.15)

    return dict(
        balance_sheet_total=round(balance_sheet_total, 2),
        fixed_assets=round(fixed_assets, 2),
        intangible_assets=round(intangible_assets, 2),
        tangible_assets=round(tangible_assets, 2),
        financial_assets=round(financial_assets, 2),
        current_assets=round(current_assets, 2),
        stockpiles=round(stockpiles, 2),
        receivables=round(receivables, 2),
        securities_and_shares=round(securities_and_shares, 2),
        cash_and_bank_balances=round(cash_and_bank_balances, 2),
        prepaid_expenses=round(prepaid_expenses, 2),
        equity=round(equity, 2),
        required_share_capital=round(required_share_capital, 2),
        capital_reserves=round(capital_reserves, 2),
        retained_earnings=round(retained_earnings, 2),
        balance_sheet_profit=round(balance_sheet_profit, 2),
        profit_carried_forward=round(profit_carried_forward, 2),
        accruals=round(accruals, 2),
        liabilities=round(liabilities, 2),
        long_term_liabilities=round(long_term_liabilities, 2),
    )


def seed_companies(count=100000):
    """Seed mock company data into the database with realistic financials."""
    if Company.query.first():
        print("Companies exist — skipping seeding.")
        return

    print(f"Seeding {count} companies...")

    existing_ids = set()
    companies = []

    for _ in range(count):
        # Unused fields for now
        industry = random.choice(list(INDUSTRY_BRANCHES.keys()))
        branch = random.choice(INDUSTRY_BRANCHES[industry])
        region = random.choice(list(AUSTRIAN_REGIONS.keys()))
        city = random.choice(AUSTRIAN_REGIONS[region])
        street_address = fake.street_address()
        address = f"{street_address}, {city}, {region}, Austria"

        # Generate financials
        financials = generate_financials()

        company = Company(
            id=generate_company_id(existing_ids),
            name=fake.company(),
            legal_form=random.choice(LEGAL_FORMS),
            **financials
        )
        companies.append(company)

    db.session.bulk_save_objects(companies)
    db.session.commit()

    print(f"Successfully seeded {count} companies.")