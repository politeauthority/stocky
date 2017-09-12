"""Quote - Models

"""
from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey, func, UniqueConstraint

from app import db
from app.models.base import Base


class Quote(Base):

    __tablename__ = 'quotes'

    id = Column(Integer, primary_key=True)
    ts_created = Column(DateTime, default=func.current_timestamp())
    ts_updated = Column(DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp())
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    date = Column(DateTime, nullable=False)
    close = Column(Float, nullable=False)
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    volume = Column(Float)

    __table_args__ = (
        UniqueConstraint('company_id', 'date', name='uix_1'),
    )

    def __init__(self, _id=None):
        if _id:
            self.id = _id

    def __repr__(self):
        return '<Quote %r, %r>' % (self.id, self.company_id)

    def save(self):
        """
        """
        exists = None
        if not self.id:
            exists = self.query.filter(
                Quote.company_id == self.company_id,
                Quote.date == self.date).one_or_none()
        if not self.id and not exists:
            db.session.add(self)
        db.session.commit()

# End File: stocks/app/models/quote.py
