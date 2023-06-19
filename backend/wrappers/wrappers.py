from functools import wraps
from fastapi import status, HTTPException

def check_token(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        token = kwargs.get("token")
        if not token:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token")
        return func(*args, **kwargs)
    return wrapper