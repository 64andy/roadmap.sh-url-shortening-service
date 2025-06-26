from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime


from . import db

class ShortenedURL(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(String(6), unique=True)
    url: Mapped[str]
    created_at: Mapped[datetime]
    updated_at: Mapped[datetime]

    def __init__(self, code: str, url: str, created_at: datetime):
        self.code = code
        self.url = url
        self.created_at = created_at
        self.updated_at = created_at
    
    def __repr__(self):
        return f"ShortenedURL({self.id=!r}, {self.code=!r}, {self.url=!r}, {self.created_at=!r}, {self.updated_at=!r})"