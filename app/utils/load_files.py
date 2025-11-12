


def load_companies(data):
    """Creates and commits a Company object from a dictionary. May not function with edge-cases and the dictionary needs to be structured like the Company Model"""

    company = Company(**data)  # uses python's built in unpacking operator
    db.session.add(company)  # adds the company to the flask database session
    db.session.commit()
    print(f"company {company.name} has been commited to the database.")