"""
Import all SQLAlchemy models here.

Alembic imports this module so every model gets
registered with Base.metadata.
"""
from app.models.user import User
from app.models.account import Account
from app.models.transaction import Transaction
from app.models.goals import Goal

