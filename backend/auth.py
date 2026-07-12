"""
auth.py — Authentication + Role-Based Access Control (RBAC) for the prototype.

Deliberately minimal for a 1-day hackathon build:
  - Passwords hashed with bcrypt (via passlib) — never stored in plaintext
  - JWT access tokens (python-jose) carrying {sub: username, role: citizen|officer}
  - Two FastAPI dependencies: get_current_user (any logged-in user) and
    require_role("officer") (blocks citizens from officer-only endpoints)

This is enough to visually and functionally prove RBAC in a demo — a citizen
token hitting an officer-only endpoint gets a 403, on camera, in real time.
"""

import os
from datetime import datetime, timedelta, timezone
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

from database import db_cursor

SECRET_KEY = os.getenv("JWT_SECRET_KEY", "hackathon-demo-secret-change-in-real-deployment")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 120

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


def create_access_token(username: str, role: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {"sub": username, "role": role, "exp": expire}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def authenticate_user(username: str, password: str) -> Optional[dict]:
    with db_cursor() as cur:
        cur.execute("SELECT * FROM users WHERE username = ?", (username,))
        row = cur.fetchone()
    if row is None:
        return None
    if not verify_password(password, row["password_hash"]):
        return None
    return {"username": row["username"], "role": row["role"]}


def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        role: str = payload.get("role")
        if username is None or role is None:
            raise credentials_exception
        return {"username": username, "role": role}
    except JWTError:
        raise credentials_exception


def require_role(required_role: str):
    """
    Usage: @app.get(...) def endpoint(user = Depends(require_role("officer")))
    Raises 403 if the logged-in user's role doesn't match. This is the line
    of code that makes RBAC real rather than just a UI toggle.
    """
    def role_checker(user: dict = Depends(get_current_user)) -> dict:
        if user["role"] != required_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"This action requires '{required_role}' role. "
                       f"Your role is '{user['role']}'."
            )
        return user
    return role_checker
