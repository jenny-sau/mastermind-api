from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from starlette.status import HTTP_201_CREATED

from database import get_db
import models
from auth import hash_password, verify_password, create_access_token, decode_access_token
from schemas import (
    UserSignup,
    UserResponse,
    UserLogin,
    TokenOut,
    GameCreate, GameResponse,
    MoveCreate, MoveResponse
)
from game_logic import generate_solution, check_guess, is_game_won, calculate_score

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
# Endpoint GAME
# ----------------------
@app.post(
    "/game/create",
    response_model=GameResponse,
    status_code=status.HTTP_201_CREATED
    )
def create_game(
        game_data: GameCreate,
        current_user: models.User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    """Create a game"""
    solution = generate_solution(game_data.difficulty)

    new_game = models.Game(
        user_id = current_user.id,
        difficulty = game_data.difficulty,
        solution = solution,
        status = "in_progress"
    )
    db.add(new_game)
    db.commit()
    db.refresh(new_game)

    return new_game

@app.post(
    "/game/{game_id}/move",
    response_model = MoveResponse,
    status_code = status.HTTP_201_CREATED
    )
def play_move(
        game_id:int,
        move_data: MoveCreate,
        current_user: models.User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    """Play a move in a game"""
    game = db.query(models.Game).filter(
        models.Game.id == game_id,
        models.Game.user_id == current_user.id #as a security
    ).first()
    if not game:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail ="Game not found")
    if game.status != "in_progress":
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail ="Game is already finished")
    correct, wrong = check_guess(game.solution, move_data.guess)

    turn_number = db.query(models.Move).filter(
        models.Move.game_id == game_id
    ).count() +1

    new_move = models.Move(
        game_id= game_id,
        turn_number= turn_number,
        guess= move_data.guess,
        correct_positions= correct,
        wrong_positions= wrong
    )
    db.add(new_move)
    if is_game_won(game.solution, move_data.guess):
        game.status = "won"
        game.score = calculate_score(game.difficulty, turn_number)
    elif turn_number >= 12:
        game.status = "lost"

    db.commit()
    db.refresh(new_move)
    return new_move





