"""Company - Models

"""
from sqlalchemy import Column, Integer, String, Float, DateTime, PickleType, Text
from sqlalchemy import UniqueConstraint, ForeignKey
from sqlalchemy.orm import relationship

from app.models.base import Base


class Company(Base):

    __tablename__ = 'companies'

    symbol = Column(String(10), nullable=False)
    name = Column(String(128), nullable=False)
    price = Column(Float)
    market_cap = Column(Float)
    ipo_date = Column(DateTime)
    sector = Column(String(128))
    industry = Column(String(128))
    exchange = Column(String(128))
    high_52_weeks = Column(Float)
    high_52_weeks_date = Column(DateTime)
    low_52_weeks = Column(Float)
    low_52_weeks_date = Column(DateTime)
    meta = relationship('CompanyMeta', back_populates="company")
    dividend = relationship('CompanyDividend', back_populates="company")

    __table_args__ = (
        UniqueConstraint('symbol', 'exchange', name='uix_1'),
    )

    def __init__(self, _id=None):
        if _id:
            self.id = _id
            c = self.query.filter(Company.id == self.id).one()
            if c:
                self.__build_obj__(c)

    def __repr__(self):
        return '<Company %r, %r>' % (self.id, self.symbol)

    def __build_obj__(self, obj):
        self.id = int(obj.id)
        self.symbol = obj.symbol
        self.name = obj.name
        self.market_cap = obj.market_cap
        self.ipo_date = obj.ipo_date
        self.sector = obj.sector
        self.industry = obj.industry
        self.exchange = obj.exchange
        self.high_52_weeks = obj.high_52_weeks
        self.high_52_weeks_date = obj.high_52_weeks_date
        self.low_52_weeks = obj.low_52_weeks
        self.low_52_weeks_date = obj.low_52_weeks_date
        self.meta = obj.meta


class CompanyMeta(Base):

    __tablename__ = 'companies_meta'

    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    key = Column(String(256), nullable=False)
    val_type = Column(String(256))
    val_string = Column(Text())
    val_pickle = Column(PickleType())
    val_int = Column(Integer)
    val_date = Column(DateTime)
    company = relationship("Company", back_populates="meta")

    def __repr__(self):
        return '<CompanyMeta %s, %s>' % (self.key, self.id)


class CompanyDividend(Base):

    __tablename__ = 'companies_dividend'

    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    eff_date = Column(DateTime)
    declaration_date = Column(DateTime)
    record_date = Column(DateTime)
    pay_date = Column(DateTime)
    price = Column(Float, nullable=False)
    company = relationship("Company", back_populates="dividend")

    def __repr__(self):
        return '<CompanyDividend %s, %s>' % (self.price, self.pay_date)

# End File: stocky/app/models/company.py
