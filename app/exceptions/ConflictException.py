from fastapi import HTTPException

#Exception raised when a conflict occurs in the database.
class ConflitException(HTTPException):
    def __init__(self, detail: str ="Conflict"):
        super().__init__(
            status_code=409,
            detail=detail
        )