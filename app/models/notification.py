from datetime import datetime, timezone

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship

from app.database.base import Base


class Notification(Base):
    __tablename__ = "notifications"
    __table_args__ = (UniqueConstraint("user_id", "event_id", name="uq_notification_user_event"),)

    notification_id = Column(Integer, primary_key=True)
    user_id = Column(
        Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False, index=True
    )
    event_id = Column(
        Integer, ForeignKey("events.event_id", ondelete="CASCADE"), nullable=False, index=True
    )
    message = Column(String(500), nullable=False)
    distance_km = Column(Float, nullable=False)
    is_read = Column(Boolean, nullable=False, default=False)
    # Armazena o horário UTC em uma coluna sem fuso para manter compatibilidade com MySQL.
    created_at = Column(
        DateTime, nullable=False, default=lambda: datetime.now(timezone.utc).replace(tzinfo=None)
    )

    user = relationship("User", back_populates="notifications")
    event = relationship("Event", back_populates="notifications")
