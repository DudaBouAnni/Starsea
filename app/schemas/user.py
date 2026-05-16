from typing import Optional

from pydantic import BaseModel

class UserBase(BaseModel):
    """
    Base user schema.

    Contains the fields used in user creation, response, and update schemas.
    """
    username: str
    email: str
    user_password: str

class UserCreate(BaseModel):
    #Schema used to create a user.
    username: str
    email: str
    user_password: str

class UserResponse(BaseModel):
    #Schema used when requesting user information.
    user_id: int
    username: str
    email: str

class UserUpdate(BaseModel):
    """
    Schema used to update an existing user.
    All fields are optional.
    """
    username: Optional[str] = None
    email: Optional[str] = None
    user_password: Optional[str] = None

    class Config:
        from_attributes = True