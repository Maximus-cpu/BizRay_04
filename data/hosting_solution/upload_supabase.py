import os
from dotenv import load_dotenv
from supabase import create_client, Client
from user_test_data import test_users

load_dotenv()  # load environment variables from .env file

"""Adam's Docs:
    - The supabase rest API expects JSON, but the python Client (supabase package) converts the dictionaries written in
    python to JSON before its sent to the API. 
"""

# Initializes a new Supabase client
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_SERVICE_KEY")  # Don't you dare expose the service_role API KEY!
supabase: Client = create_client(url, key)


def insert_bulk_data(table_name, data_list):
    """Function to insert bulk data into the database"""
    try:
        response = (
            supabase.table(table_name)
            .insert([data_list], count="exact", returning="minimal") # inserts a list of dictionaries into the db, count parameter counts rows changed, returning parameter changes the amount of information in the response variable.
            .execute()
        )
        print(f"Inserted {response.count} rows into {table_name}.")
        return response
    except Exception as e:
        return e


insert_bulk_data("Users", test_users)


