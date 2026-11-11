from fastapi import HTTPException


# Exceção para recursos não encontrados.
class NotFoundException(HTTPException):
    def __init__(self, detail: str = "Not Found"):
        super().__init__(status_code=404, detail=detail)
