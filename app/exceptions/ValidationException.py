from fastapi import HTTPException

#Validation exception raised when invalid data is provided.
class ValidationException(HTTPException):
    def __init__(self, detail: str ="Validation Error"):
        super().__init__(
            status_code=422,
            detail=detail
        )