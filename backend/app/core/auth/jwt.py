"""Creating and handling jwt token"""

from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt

from app.config import settings

def create_access_token(user_id: str)-> str:
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )

    payload = {
        "sub": user_id,
        "exp": expire
    }

    return jwt.encode(
        payload,
        settings.JWT_SECRET,
        algorithm=settings.ALGORITHM
    )

def decode_access_token(token: str):
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=settings.ALGORITHM,
        )
        return payload
    except JWTError:
        return None