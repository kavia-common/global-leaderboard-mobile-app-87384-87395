from __future__ import annotations

from marshmallow import Schema, fields, validate


# PUBLIC_INTERFACE
class UserCreateSchema(Schema):
    """Payload to create a new user."""
    username = fields.String(required=True, validate=validate.Length(min=3, max=64), description="Unique username")
    email = fields.Email(required=True, description="Unique email")
    region = fields.String(required=False, allow_none=True, validate=validate.Length(max=32), description="Region code")


# PUBLIC_INTERFACE
class UserUpdateSchema(Schema):
    """Payload to update existing user."""
    username = fields.String(validate=validate.Length(min=3, max=64))
    email = fields.Email()
    region = fields.String(allow_none=True, validate=validate.Length(max=32))


# PUBLIC_INTERFACE
class UserSchema(Schema):
    """User response representation."""
    id = fields.Integer()
    username = fields.String()
    email = fields.Email()
    region = fields.String(allow_none=True)
    created_at = fields.DateTime()
    updated_at = fields.DateTime()


# PUBLIC_INTERFACE
class GameCreateSchema(Schema):
    """Payload to create a game."""
    name = fields.String(required=True, validate=validate.Length(min=2, max=120))
    description = fields.String(required=False, allow_none=True)


# PUBLIC_INTERFACE
class GameUpdateSchema(Schema):
    """Payload to update a game."""
    name = fields.String(validate=validate.Length(min=2, max=120))
    description = fields.String(allow_none=True)


# PUBLIC_INTERFACE
class GameSchema(Schema):
    """Game response representation."""
    id = fields.Integer()
    name = fields.String()
    description = fields.String(allow_none=True)
    created_at = fields.DateTime()
    updated_at = fields.DateTime()


# PUBLIC_INTERFACE
class ScoreCreateSchema(Schema):
    """Payload to create a score."""
    user_id = fields.Integer(required=True, description="User ID")
    game_id = fields.Integer(required=True, description="Game ID")
    value = fields.Integer(required=True, validate=validate.Range(min=0), description="Score value")
    region = fields.String(required=False, allow_none=True, validate=validate.Length(max=32))
    achieved_at = fields.DateTime(required=False)


# PUBLIC_INTERFACE
class ScoreSchema(Schema):
    """Score response representation."""
    id = fields.Integer()
    user_id = fields.Integer()
    game_id = fields.Integer()
    value = fields.Integer()
    region = fields.String(allow_none=True)
    achieved_at = fields.DateTime()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()


# PUBLIC_INTERFACE
class LeaderboardQuerySchema(Schema):
    """Query params for leaderboard endpoints."""
    limit = fields.Integer(load_default=20, validate=validate.Range(min=1, max=200), metadata={"description": "Max items"})
    region = fields.String(load_default=None, allow_none=True, metadata={"description": "Region code filter"})
    since = fields.DateTime(load_default=None, allow_none=True, metadata={"description": "Only scores after this time"})
