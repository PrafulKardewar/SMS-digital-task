from pydantic import BaseModel


class JwtUser(BaseModel):
    username: str
    password: str
    is_active: bool = False
    role: str = None

