


def load_companies(company_dict):
    # Dictionary needs to be structured like the Company Model

    company = Company(**company_dict)  # uses python's built in unpacking operator
    db.session.add(company)  # adds the company to the flask database session
    db.session.commit()
    print(f"Company {company.name} has been commited to the database.")