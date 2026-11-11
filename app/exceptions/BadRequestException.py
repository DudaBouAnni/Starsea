from fastapi import HTTPException


# Exceção para requisições com dados inválidos ou malformados.
class BadRequestException(HTTPException):
    def __init__(self, detail: str = "Bad Request"):
        super().__init__(status_code=400, detail=detail)
