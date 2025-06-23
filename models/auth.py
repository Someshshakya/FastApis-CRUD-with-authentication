from pydantic import BaseModel

class TokenData(BaseModel):
    username: str
    role: str

class UserLogin(BaseModel):
    username: str
    password: str
