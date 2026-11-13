# models.py
from datetime import UTC, datetime

from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class Blob(Base):
    __tablename__ = "blobs"

    digest: Mapped[str] = mapped_column(primary_key=True)
    size_bytes: Mapped[int]
    path: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(UTC))


class Image(Base):
	__tablename__ = "Image Records"

class Tags(Base):
	__tablename__ = "tags"