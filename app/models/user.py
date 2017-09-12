"""Company - Models

"""
from sqlalchemy import Column, Integer, String, Float, DateTime, PickleType, Text
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from app.models.base import Base


class User(Base):

    __tablename__ = 'users'

    email = Column(String(10), nullable=False)
    name = Column(String(128), nullable=False)
    password = Column(Float, nullable=False)
    type = Column(String(20))
    meta = relationship('UserMeta', back_populates="user")

    def __init__(self, _id=None):
        if _id:
            self.id = _id

    def __repr__(self):
        return '<User %r, %r>' % (self.symbol, self.name)


class UserMeta(Base):

    __tablename__ = 'users_meta'

    company_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    key = Column(String(256), nullable=False)
    val_type = Column(String(256))
    val_string = Column(Text())
    val_pickle = Column(PickleType())
    val_date = Column(DateTime)
    company = relationship("User", back_populates="meta")

    def __repr__(self):
        return '<UserMeta %s, %s>' % (self.key, self.id)

# End File: stocky/app/models/user.py
