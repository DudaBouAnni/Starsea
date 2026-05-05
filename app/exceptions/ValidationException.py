from fastapi import HTTPException


class BadRequestException(HTTPException):
    def __init__(self, detail: str ="Validation Error"):
        super().__init__(
            status_code=422,
            detail=detail
        )