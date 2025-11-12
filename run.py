from app import create_app, db
from app.models.company import Company
from app.models.user import User
from sqlalchemy import inspect
from app.utils.seed_companies import seed_companies

app = create_app()
with app.app_context():
    #db.create_all()

    inspector = inspect(db.engine)
    tables = inspector.get_table_names()
    print(f"Tables found in database: {tables}")

    #Company seeder
    #seed_companies()

if __name__ == "__main__":
    app.run(debug=True)