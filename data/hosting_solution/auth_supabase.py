import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()  # load environment variables from .env file

# Initializes a new Supabase client
url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_SERVICE_KEY")  # Don't you dare expose the service role API KEY!
supabase: Client = create_client(url, key)

# Getting the Email and Password from the .env file:
db_user = os.environ.get("SUPABASE_USER")
db_pass = os.environ.get("SUPABASE_USER_PASS")

USER_CREATED = True
if not USER_CREATED:
    try:
        dev_user_signup = supabase.auth.sign_up(
            {
                "email": db_user,
                "password": db_pass,
            }
        )
        print(f"User with email {db_user} created successfully")
    except Exception as e:
        print(e)

try:
    dev_user_sign_in = supabase.auth.sign_in_with_password(  # Signing in to supabase with email + password
        {
            "email": db_user,
            "password": db_pass,
        }
    )
    print(f"Successfully logged in to supabase as user with email {db_user}")
    print(dev_user_sign_in)
except Exception as e:
    print(e)





