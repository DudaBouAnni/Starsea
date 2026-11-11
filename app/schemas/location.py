from typing import Annotated

from pydantic import BaseModel, Field, model_validator

Latitude = Annotated[float, Field(ge=-90, le=90, allow_inf_nan=False)]
Longitude = Annotated[float, Field(ge=-180, le=180, allow_inf_nan=False)]
RadiusKm = Annotated[float, Field(gt=0, le=1000, allow_inf_nan=False)]


class OptionalCoordinates(BaseModel):
    latitude: Latitude | None = None
    longitude: Longitude | None = None

    @model_validator(mode="after")
    def validate_coordinate_pair(self):
        supplied = self.model_fields_set
        if ("latitude" in supplied) != ("longitude" in supplied):
            raise ValueError("Envie latitude e longitude juntas.")
        if (self.latitude is None) != (self.longitude is None):
            raise ValueError("Latitude e longitude devem ser preenchidas ou removidas juntas.")
        return self


class UserLocationUpdate(BaseModel):
    latitude: Latitude
    longitude: Longitude


class NotificationPreferences(BaseModel):
    notification_radius_km: RadiusKm = 50
    nearby_notifications_enabled: bool = True
    personalized_notifications_only: bool = False


class NotificationPreferencesUpdate(BaseModel):
    notification_radius_km: RadiusKm | None = None
    nearby_notifications_enabled: bool | None = None
    personalized_notifications_only: bool | None = None

    @model_validator(mode="after")
    def reject_explicit_nulls(self):
        if any(getattr(self, field) is None for field in self.model_fields_set):
            raise ValueError("As preferências não podem ser nulas.")
        return self
