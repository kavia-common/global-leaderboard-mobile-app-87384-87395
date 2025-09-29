from __future__ import annotations

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class TimestampMixin:
    """Mixin for created/updated timestamps."""
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow
    )


class User(TimestampMixin, db.Model):
    """User profile model."""
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    region = db.Column(db.String(32), nullable=True, index=True)

    scores = db.relationship("Score", back_populates="user", cascade="all, delete-orphan")


class Game(TimestampMixin, db.Model):
    """Game model representing a game title."""
    __tablename__ = "games"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False, index=True)
    description = db.Column(db.Text, nullable=True)

    scores = db.relationship("Score", back_populates="game", cascade="all, delete-orphan")


class Score(TimestampMixin, db.Model):
    """Score model for leaderboard entries."""
    __tablename__ = "scores"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    game_id = db.Column(db.Integer, db.ForeignKey("games.id", ondelete="CASCADE"), nullable=False, index=True)
    value = db.Column(db.Integer, nullable=False, index=True)
    region = db.Column(db.String(32), nullable=True, index=True)
    achieved_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, index=True)

    user = db.relationship("User", back_populates="scores")
    game = db.relationship("Game", back_populates="scores")

    __table_args__ = (
        db.Index("ix_scores_game_value_desc", "game_id", "value"),
        db.Index("ix_scores_game_region_value", "game_id", "region", "value"),
        db.UniqueConstraint("user_id", "game_id", "value", "achieved_at", name="uq_score_dedup"),
    )
