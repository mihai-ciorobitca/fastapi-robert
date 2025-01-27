from requests import post
from dotenv import load_dotenv
from os import getenv

load_dotenv()

API = getenv("API")
response = post("http://fastapi-robert.vercel.app/delete-unverified-users", headers={"KEY","password"})
print(response.json())
print(response.status_code)