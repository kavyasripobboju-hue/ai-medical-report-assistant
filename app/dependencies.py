from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError

SECRET_KEY = "my_super_secret_key"
ALGORITHM = "HS256"

security = HTTPBearer()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials

    print("========== JWT DEBUG ==========")
    print("Received Token:", token)

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        print("Decoded Payload:", payload)

        email = payload.get("sub")

        if email is None:
            raise HTTPException(status_code=401, detail="Invalid Token")

        return email

    except JWTError as e:
        print("JWT ERROR:", str(e))
        raise HTTPException(status_code=401, detail="Invalid Token")