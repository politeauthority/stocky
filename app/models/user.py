"""User - Models

"""
from sqlalchemy import Column, Integer, String, DateTime, PickleType, Text
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash

from app import db
from app.models.base import Base


class User(Base):

    __tablename__ = 'users'

    email = Column(String(256), nullable=False)
    name = Column(String(256))
    password = Column(String(256), nullable=False)
    last_login = Column(DateTime, nullable=False)
    type = Column(String(20))
    meta = relationship('UserMeta', back_populates="user")

    def __init__(self, _id=None):
        if _id:
            self.id = _id

    def __repr__(self):
        return '<User %r, %r>' % (self.id, self.email)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()


class UserMeta(Base):

    __tablename__ = 'users_meta'

    company_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    key = Column(String(256), nullable=False)
    val_type = Column(String(256))
    val_string = Column(Text())
    val_pickle = Column(PickleType())
    val_date = Column(DateTime)
    company = relationship("User", back_populates="meta")
    user = relationship('User', back_populates="meta")

    def __repr__(self):
        return '<UserMeta %s, %s>' % (self.key, self.id)

# End File: stocky/app/models/user.py
