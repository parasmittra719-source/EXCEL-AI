from fastapi import HTTPException
from jose import jwt

SECRET = "SECRET123"

users = {
  "admin": {"password": "admin", "role": "Admin", "org_id": 1, "org_name": "Demo Corp"},
  "user": {"password": "user", "role": "User", "org_id": 1, "org_name": "Demo Corp"}
}

def login(username, password):
    if username in users and users[username]["password"] == password:
        user = users[username]
        token = jwt.encode(
          {
              "username": username, 
              "role": user["role"], 
              "org_id": user["org_id"],
              "org_name": user["org_name"]
          },
          SECRET,
          algorithm="HS256"
        )
        return token
    raise HTTPException(401)
