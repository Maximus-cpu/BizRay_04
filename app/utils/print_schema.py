# from sqlalchemy import create_engine, inspect
# from app.config import os # assuming config.py imports os and uses os.environ.get

# def print_database_schema():
#     # Get database URL from environment variable
#     database_url = os.environ.get("DATABASE_URL")

#     if not database_url:
#         raise ValueError("DATABASE_URL environment variable is not set.")

#     # Create database engine
#     engine = create_engine(database_url)

#     # Reflect database schema
#     inspector = inspect(engine)

#     print("\n=== Database Schema ===\n")

#     for schema in inspector.get_schema_names():
#         print(f"Schema: {schema}")
#         print("-" * (8 + len(schema)))

#         tables = inspector.get_table_names(schema=schema)
#         for table in tables:
#             print(f"  Table: {table}")
#             columns = inspector.get_columns(table, schema=schema)
#             for col in columns:
#                 print(f"    {col['name']:20} {col['type']}")
#             print()
#         print()

# if __name__ == "__main__":
#     print_database_schema()
