from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from flask import abort, Response


from . import db

class ShortenedURL(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(String(6), unique=True)
    url: Mapped[str]
    created_at: Mapped[datetime]
    updated_at: Mapped[datetime]
    access_count: Mapped[int]

    def __init__(self, code: str, url: str, created_at: datetime):
        self.code = code
        self.url = url
        self.created_at = created_at
        self.updated_at = created_at
        self.access_count = 0
    
    def __repr__(self):
        return f"ShortenedURL(id={self.id!r}, code={self.code!r}, url={self.url!r}, created_at={self.created_at!r}, updated_at={self.updated_at!r})"
    
    def info_dict(self) -> dict:
        return {
            'id':       str(self.id),
            'url':      self.url,
            'shortCode':self.code,
            'createdAt':self.created_at.strftime(r"%Y-%m-%dT%H:%M:%SZ"),
            'updatedAt':self.updated_at.strftime(r"%Y-%m-%dT%H:%M:%SZ"),
        }
    
    def info_dict_full(self) -> dict:
        return {**self.info_dict(), 'accessCount': self.access_count}
    
    @staticmethod
    def find_by_code(code: str) -> 'ShortenedURL | None':
        return db.session.execute(db.select(ShortenedURL).where(ShortenedURL.code == code)).scalar()
    
    @staticmethod
    def find_by_code_or_404(code: str) -> 'ShortenedURL':
        this = ShortenedURL.find_by_code(code)
        if this is None:
            res = Response('No URL corresponds to this code')
            res.status_code = 404
            abort(res)
        return this
