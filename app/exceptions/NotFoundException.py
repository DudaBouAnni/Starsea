from fastapi import HTTPException

#Exception raised when the requested resource is not found.
class NotFoundException(HTTPException):
    def __init__(self, detail: str ="Not Found"):
        super().__init__(
            status_code=404,
            detail=detail
        )