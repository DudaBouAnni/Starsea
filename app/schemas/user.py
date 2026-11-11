from typing import Optional

from pydantic import BaseModel, ConfigDict


class UserBase(BaseModel):
    """
    Esquema base de usuário.

    Define os campos utilizados na criação, nas respostas e na atualização de usuários.
    """

    username: str
    email: str
    user_password: str
    profile_image: Optional[str] = None
    country: Optional[str] = None


class UserCreate(UserBase):
    """Esquema para criar um usuário."""

    pass


class UserResponse(BaseModel):
    """Esquema de resposta com os dados públicos do usuário."""

    user_id: int
    username: str
    email: str
    profile_image: Optional[str] = None
    country: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class UserUpdate(BaseModel):
    """
    Esquema para atualizar um usuário existente.
    Todos os campos são opcionais.
    """

    username: Optional[str] = None
    email: Optional[str] = None
    user_password: Optional[str] = None
    profile_image: Optional[str] = None
    country: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
