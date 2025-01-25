from fastapi import FastAPI, Request , HTTPException
from supabase import create_client
from dotenv import load_dotenv
from os import getenv
from functions import check_user

load_dotenv()

SUPA_KEY = getenv("SECRET")
SUPA_URL = getenv("URL")

supabase_client = create_client(SUPA_URL, SUPA_KEY)

app = FastAPI()

@app.get("/")
def index():
    return {"message": "Api is running"}

@app.post("/delete-unverified-users")
def delete_unverified_users():
    api_key = request.headers.get("api_key")
    if api_key != getenv("API"):
        raise HTTPException(status_code=401, detail="Unauthorized")
    users = supabase_client.table("users").select("username", "created_at", "verification").execute().data
    print(users)
    users_to_delete = [user for user in users if check_user(user)]
    print(users_to_delete)
    return users_to_delete


