from requests import post
from dotenv import load_dotenv
from os import getenv

load_dotenv()

response = post("http://localhost:3000/delete-unverified-users", headers={"api_key","password"})
print(response.json())
print(response.status_code)