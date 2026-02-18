from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from database import get_db
import models
from auth import hash_password, verify_password, create_access_token, decode_access_token
from schemas import (
    UserSignup,
    UserResponse,
    UserLogin,
    TokenOut
)

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to MASTERMIND"}

# ----------------------
# SÉCURITÉ JWT
# ----------------------
security = HTTPBearer()

def get_current_user(
        credentials: HTTPAuthorizationCredentials = Depends(security),
        db: Session = Depends(get_db)
):
    """Dependency to get the current authenticated user."""
    token = credentials.credentials

    # decode_access_token lance déjà une HTTPException si problème
    payload = decode_access_token(token)

    user_id = payload.get("user_id")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload"
        )

    user = db.query(models.User).filter(models.User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )

    return user
#---------------
# AUTH ROUTES
#-------------
@app.post(
    "/auth/signup",
    response_model=UserResponse,
    status_code = status.HTTP_201_CREATED
)
def signup(user: UserSignup, db: Session = Depends(get_db)):
    """Create a new user account."""
    existing_user = db.query(models.User).filter(
        models.User.username ==user.username
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken"
        )

    hashed = hash_password(user.password)

    db_user = models.User(
        username=user.username,
        password_hashed = hashed
    )
    db.add (db_user)
    db.commit()
    db.refresh(db_user)

    return db_user

@app.post(
    "/auth/login",
    response_model=TokenOut,
    status_code=status.HTTP_200_OK
)
def login(
        credentials: UserLogin,
        db: Session = Depends (get_db)
):
    """Log in and receive a JWT token."""
    user = db.query(models.User).filter(
        models.User.username == credentials.username
    ).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )
    if not verify_password(credentials.password, user.password_hashed):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )
    token = create_access_token({"user_id": user.id})

    return TokenOut(access_token=token)

#----------------------
# PROTECTED ROUTE EXAMPLE
# ----------------------
@app.get(
    "/me",
    response_model=UserResponse
)
def get_me(current_user: models.User = Depends(get_current_user)):
    """Get current user info (requires authentication)."""
    return current_user

