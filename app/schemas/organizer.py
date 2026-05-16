from typing import Optional

from pydantic import BaseModel

class OrganizerBase(BaseModel):
    """
    Base organizer schema.

    Contains the fields used in organizer creation, response, and update schemas.
    """
    organizer_name: str

class OrganizerCreate(OrganizerBase):
    #Schema used to create an organizer.
    organizer_name: str

class OrganizerResponse(OrganizerBase):
    #Schema used when requesting organizer information.
    organizer_id: int

    class Config:
        from_attributes = True

class OrganizerUpdate(BaseModel):
    """
    Schema used to update an existing organizer.
    All fields are optional.
    """
    organizer_name: Optional[str] = None

OrganizerResponse.model_rebuild()