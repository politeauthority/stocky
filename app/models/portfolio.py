"""Portfolio - Models

"""
from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship

from app.models.base import Base


class Portfolio(Base):

    __tablename__ = 'portfolios'

    events = relationship('PortfolioEvent', back_populates="events")
    user_id = Column(Integer, nullable=False)
    name = Column(String(20), nullable=False)

    def __init__(self, id):
        self.id = id

    def __repr__(self):
        return '<Portfolio %r, %r>' % (self.symbol, self.name)


class PortfolioEvent(Base):

    __tablename__ = 'portfolios_events'

    portfolio_id = Column(Integer, ForeignKey("portfolios.id"), nullable=False)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    price = Column(Float, nullable=False)
    count = Column(Integer, nullable=False)
    date = Column(DateTime, nullable=False)
    type = Column(String(10), nullable=False)
    date = Column(DateTime, nullable=False)

    def __init__(self, id):
        self.id = id

    def __repr__(self):
        return '<PortfolioEvent %r, %r>' % (self.id, self.price)


# End File: stocky/app/models/portfolio.py