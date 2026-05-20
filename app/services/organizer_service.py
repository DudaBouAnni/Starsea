from sqlalchemy.orm import Session

from app.exceptions.ConflictException import ConflictException
from app.exceptions.NotFoundException import NotFoundException
from app.models import Organizer
from app.schemas.organizer import OrganizerCreate, OrganizerUpdate

#Create Organizer
def create_organizer_service(organizer: OrganizerCreate, db: Session):
    exists = db.query(Organizer).filter_by(organizer_name=organizer.organizer_name).first()

    if exists:
        raise ConflictException("Organizer already exists")

    db_organizer = Organizer(organizer_name=organizer.organizer_name)

    db.add(db_organizer)

    db.commit()
    db.refresh(db_organizer)

    return db_organizer

#List Organizers
def list_organizers_service(db: Session):
    return db.query(Organizer).all()

#Get Organizer Events
def get_organizer_events_service(organizer_id: int, db: Session):
    organizer = db.get(Organizer, organizer_id)

    if not organizer:
        raise NotFoundException("Organizer does not exist")

    update_data = updated_data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(organizer, key, value)

    db.commit()
    db.refresh(organizer)

    return organizer

#Update Organizer
def update_organizer_service(organizer_id: int, updated_data: OrganizerUpdate, db: Session):
    organizer = db.get(Organizer, organizer_id)

    if not organizer:
        raise NotFoundException("Organizer does not exist")

    update_data = updated_data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(organizer, key, value)

        db.commit()
        db.refresh(organizer)

        return organizer

#Delete Organizer
def delete_organizer_service(organizer_id: int, db: Session):
    organizer = db.get(Organizer, organizer_id)

    if not organizer:
        raise NotFoundException("Organizer does not exist")

    organizer.events.clear()

    db.delete(organizer)

    db.commit()

    return {"message": "Organizer deleted successfully!"}