from fastapi import Depends, HTTPException, Header
from auth import decode_token
from models.auth import TokenData

def get_current_user(authorization: str = Header(...)) -> TokenData:
    print(f"get_current_user received: {authorization}")  # Debug print
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization header")
    token = authorization.split(" ", 1)[1]
    print(f"Token extracted: {token}")  # Debug print
    payload = decode_token(token)
    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    return TokenData(username=payload.get("sub"), role=payload.get("role"))

def require_role(required_roles: list[str]):
    print(" now calling require role ")
    def role_checker(user: TokenData = Depends(get_current_user)):
        if user.role not in required_roles:
            raise HTTPException(status_code=403, detail="Insufficient permissions")
        return user
    return role_checker
