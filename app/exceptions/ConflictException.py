from fastapi import HTTPException

class ConflitException(HTTPException):
    def __init__(self, detail: str ="Conflict"):
        super().__init__(
            status_code=409,
            detail=detail
        )