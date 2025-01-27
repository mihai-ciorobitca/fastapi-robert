from fastapi import FastAPI, Request, HTTPException
from supabase import create_client
from dotenv import load_dotenv
from os import getenv
from datetime import datetime, timezone
import logging

load_dotenv()

SUPA_KEY = getenv("SECRET")
SUPA_URL = getenv("URL")
API = getenv("API")

supabase_client = create_client(SUPA_URL, SUPA_KEY)

app = FastAPI()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def check_user(user):
    if not user["verification"]:
        logger.info(f"Checking user: {user}")
        created_at = user["created_at"]
        created_at_dt = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
        logger.info(f"User created at: {created_at_dt}")
        now = datetime.now(timezone.utc)
        difference = (now - created_at_dt).days
        logger.info(f"Difference in days: {difference}")
        if difference > 3:
            return True
    return False

@app.get("/")
def index():
    return {"message": "Api is running"}

@app.post("/delete-unverified-users")
async def delete_unverified_users(request: Request):
    try:
        api_request = await request.headers.get("api_key")
        logger.info(f"API Request: {api_request}")
        api_key = api_request["api_key"]
        if api_key != API:
            raise HTTPException(status_code=401, detail="Unauthorized")
        users = supabase_client.table("users").select("username", "created_at", "verification").execute().data
        logger.info(f"Users fetched: {users}")
        users_to_delete = [user for user in users if check_user(user)]
        for user in users_to_delete:
            supabase_client.table("users").delete().eq("username", user["username"]).execute()
            logger.info(f"Deleted user: {user['username']}")
        return users_to_delete

    except Exception as e:
        logger.error(f"Error occurred: {e}")
        return str(e)