from sqlalchemy import(
    Column, Integer, String,
    ForeignKey, DateTime, Enum
)
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database import Base
from enum import Enum as PyEnum

#-------------------
# User
#-------------------
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key= True, index = True)
    username = Column(String, unique = True, index = True)
    password_hashed  = Column(String)

    # Relations
    games = relationship("Game", back_populates="user")

#-------------------
# Game
#-------------------
class GameStatus(str, PyEnum):
    WON = "won"
    LOST = "lost"
    IN_PROGRESS = "in_progress"

class DifficultyStatus(str, PyEnum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"
    HARDCORE = "hardcore"

class Game (Base):
    __tablename__ = "games"
    id = Column(Integer, primary_key= True, index = True)
    user_id = Column(Integer, ForeignKey("users.id"), index = True)
    status = Column(Enum(GameStatus), default = GameStatus.IN_PROGRESS, nullable = False)
    solution = Column(String)
    difficulty = Column(Enum(DifficultyStatus), nullable = False)
    score = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable = False)

    # Relations
    user = relationship("User", back_populates="games")
    moves = relationship("Move", back_populates="game")
#-------------------
# Move
#-------------------
class Move(Base):
    __tablename__ = "moves"
    id = Column(Integer, primary_key= True, index = True)
    game_id = Column(Integer, ForeignKey("games.id"), index = True)
    turn_number = Column(Integer, nullable = False)
    guess = Column(String)
    correct_positions = Column(Integer)
    wrong_positions = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable = False)

    #Relation
    game = relationship("Game", back_populates="moves")
