from sqlalchemy.orm import declarative_base

Base = declarative_base()
"""
Base class for all SQLAlchemy models.

All entities must inherit from this class.
It provides what is necessary for classes to be mapped
to database tables, allowing creating, querying, updating, and
deleting records using SQLAlchemy.
"""