from requests import post
from dotenv import load_dotenv
from os import getenv

load_dotenv()

API = getenv("API")
response = post("http://localhost:8000/delete-unverified-users", json={"api_key": API})
print(response.json())
print(response.status_code)