from pdpyras import APISession
import os

api_token = os.getenv('SOURCE_API_TOKEN')
session = APISession(api_token)

for user in session.iter_all('teams'):
    print(user)