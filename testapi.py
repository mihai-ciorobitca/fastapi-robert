from requests import post

api_key = "743c1f4e-1dfb-4f39-828a-a2e96343b8b4"
url  = "http://localhost:8000/delete-unverified-users"

response = post(url, json={"api_key": api_key})
print(response.json())