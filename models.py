# models.py
from datetime import UTC, datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class Blob(Base):
	__tablename__ = "blobs"

	digest: Mapped[str] = mapped_column(primary_key=True)
	size_bytes: Mapped[int]
	path: Mapped[str]
	created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(UTC))


class Image(Base):
	__tablename__ = "images"
	id: Mapped[int] = mapped_column(primary_key=True)
	filename: Mapped[str]
	digest: Mapped[str] = mapped_column(ForeignKey("blobs.digest"), index=True)
	exif_datetime: Mapped[datetime | None]
	exif_lon: Mapped[float | None]
	exif_lat: Mapped[float | None]
	size_bytes: Mapped[int]
	created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(UTC))
	tags: Mapped[list[Tag]] = relationship("Tag", cascade="all, delete-orphan", passive_deletes=True)


class Tag(Base):
	__tablename__ = "tags"
	image_id: Mapped[int] = mapped_column(ForeignKey("images.id", ondelete="CASCADE"), primary_key=True)
	key: Mapped[str] = mapped_column(primary_key=True)
	value: Mapped[str] = mapped_column(primary_key=True)


