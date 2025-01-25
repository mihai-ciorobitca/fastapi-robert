from fastapi import FastAPI, Request , HTTPException
from supabase import create_client
from dotenv import load_dotenv
from os import getenv
from datetime import datetime, timezone

load_dotenv()

SUPA_KEY = getenv("SECRET")
SUPA_URL = getenv("URL")
API = getenv("API")

supabase_client = create_client(SUPA_URL, SUPA_KEY)

app = FastAPI()

def check_user(user):
    if not user["verification"]:
        print(user)
        created_at = user["created_at"]
        created_at_dt = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
        print(created_at_dt)
        now = datetime.now(timezone.utc)
        difference = (now - created_at_dt).days
        print(difference)
        if difference > 3:
            return True
    return False

@app.get("/")
def index():
    return {"message": "Api is running"}

@app.post("/delete-unverified-users")
async def delete_unverified_users(request: Request):
    try:
        api_request = await request.json()
        api_key = api_request["api_key"]
        if api_key != API:
            raise HTTPException(status_code=401, detail="Unauthorized")
        users = supabase_client.table("users").select("username", "created_at", "verification").execute().data
        print(users)
        users_to_delete = [user for user in users if check_user(user)]
        for user in users_to_delete:
            supabase_client.table("users").delete().eq("username", user["username"]).execute()
        return users_to_delete

    except Exception as e:
        return str(e)