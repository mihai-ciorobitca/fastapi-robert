from requests import post
from dotenv import load_dotenv
from os import getenv

load_dotenv()

response = post("http://localhost:8000/delete-unverified-users", headers={"Authorization": "ApiKey password"})
print(response.json())
print(response.status_code)