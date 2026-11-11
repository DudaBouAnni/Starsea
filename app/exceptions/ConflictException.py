from fastapi import HTTPException


# Exceção para conflitos com os dados existentes no banco.
class ConflictException(HTTPException):
    def __init__(self, detail: str = "Conflict"):
        super().__init__(status_code=409, detail=detail)
