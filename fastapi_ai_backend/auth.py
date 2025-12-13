from fastapi import HTTPException
from jose import jwt

SECRET = "SECRET123"

users = {
  "admin": {"password": "admin", "role": "Admin"},
  "user": {"password": "user", "role": "User"}
}

def login(username, password):
    if username in users and users[username]["password"] == password:
        token = jwt.encode(
          {"username": username, "role": users[username]["role"]},
          SECRET,
          algorithm="HS256"
        )
        return token
    raise HTTPException(401)
