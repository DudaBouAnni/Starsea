from fastapi import HTTPException


# Exceção para dados que não atendem às regras de validação.
class ValidationException(HTTPException):
    def __init__(self, detail: str = "Validation Error"):
        super().__init__(status_code=422, detail=detail)
