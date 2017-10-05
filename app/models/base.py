"""Base - Model

"""
from sqlalchemy import Column, Integer, DateTime, func

from app import db


class Base(db.Model):

    __abstract__ = True

    id = Column(Integer, primary_key=True)
    ts_created = Column(DateTime, default=func.current_timestamp())
    ts_updated = Column(DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp())

    def __init__(self, _id=None):
        if _id:
            self.id = _id
            self.__build_obj__()

    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()

# End File: stocky/app/models/base.py
