from passlib.context import CryptContext
from jwt_user import JwtUser
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
from const import JWT_EXPIRY_TIME, JWT_ALGORITHM, JWT_SECRET_KEY
import jwt
from fastapi import Depends, HTTPException
from starlette.status import HTTP_401_UNAUTHORIZED
import time

oauth_schema = OAuth2PasswordBearer(tokenUrl="/token")
pwd_context = CryptContext(schemes=["bcrypt"])


def get_hashed_password(password):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except Exception as e:
        return False


password = get_hashed_password("pass")


fake_jwt_user = {"username": "user",
                 "password": password,
                 "is_active": False, "role": "admin"}

jwt_user = JwtUser(**fake_jwt_user)


def authenticate_user(user: JwtUser):
    if jwt_user.username ==user.username:
        if verify_password(user.password,jwt_user.password):
            user.role="admin"
            return user
    return False

def create_jwt_token(user:JwtUser):
    expiration_time = datetime.utcnow()+timedelta(minutes = JWT_EXPIRY_TIME)
    user.role = "admin"
    jwt_payload = {"sub": user.username,
                   "role": user.role,
                   "exp": expiration_time}
    jwt_token = jwt.encode(jwt_payload,JWT_SECRET_KEY,algorithm = JWT_ALGORITHM)
    return jwt_token

def check_jwt_token(token: str=Depends(oauth_schema)):
    try:
        jwt_payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=JWT_ALGORITHM)
        username = jwt_payload.get("sub")
        role = jwt_payload.get("role")
        expiration = jwt_payload.get("exp")
        if time.time() < expiration:
            if jwt_user.username == username:
                return final_check(role)
    except Exception as e:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED)
    raise HTTPException(status_code=HTTP_401_UNAUTHORIZED)

def final_check(role: str):
    if role == "admin":
        return True
    else:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED)


