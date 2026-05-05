from typing import Optional

from pydantic import BaseModel

class UserBase(BaseModel):
    """
        Schema base do usuário.

        Contém os campos utilizados nos schemas de criação,
        retorno e atualização de usuários.
    """
    username: str
    email: str
    user_password: str

class UserCreate(BaseModel):
    """
      Schema usada para criar o usuário.
    """
    username: str
    email: str
    user_password: str

class UserResponse(BaseModel):
    """
      Schema usada ao requisitar informações do usuário.
    """
    user_id: int
    username: str
    email: str

class UserUpdate(BaseModel):
    """
      Schema usada para atualizar um usuário existente.
      Todos os campos são opcionais
    """
    username: Optional[str] = None
    email: Optional[str] = None
    user_password: Optional[str] = None

    class Config:
        from_attributes = True