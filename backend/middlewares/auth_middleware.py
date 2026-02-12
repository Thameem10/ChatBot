from fastapi import Request, HTTPException , Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
import os
from dotenv import load_dotenv

load_dotenv()

ACCESS_SECRET = os.getenv("ACCESS_SECRET")

security = HTTPBearer()

async def auth_middleware(
    request: Request, 
    credentials: HTTPAuthorizationCredentials = Depends(security)
):

    token = credentials.credentials

    try:
        decoded = jwt.decode(token, ACCESS_SECRET, algorithms=["HS256"])
        request.state.user = decoded  # save user data for routes
        return decoded
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
