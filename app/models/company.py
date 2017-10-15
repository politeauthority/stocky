"""Company - MODELS

"""
from sqlalchemy import Column, Integer, String, Float, DateTime, PickleType, Text
from sqlalchemy import UniqueConstraint, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm.exc import NoResultFound

from app import app
from app import db
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
    dividend = relationship(
        'CompanyDividend',
        back_populates="company",
        order_by="desc(CompanyDividend.eff_date)",
        primaryjoin="Company.id==CompanyDividend.company_id")

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

    def get_by_symbol(self, symbol):
        """
        Get a Company obj by the symbol.
        @todo: Should expand this out to take an exchange as well.

        :param symbol: The companies symbol
        :type symbol: str
        :return: Company
        :rtype: Company obj
        """
        try:
            company = self.query.filter(Company.symbol == symbol).one()
            self.__build_obj__(company)
            return self
        except NoResultFound:
            app.logger.warning('Could not find Company by symbol "%s"' % symbol)
            return False


class CompanyMeta(Base):
    """
    CompanyMeta Model.
    This model allows for storage of strings, ints, dates and pickles by a company_id.
    The keying "concept" currently is company_id, key, val_type

    """

    __tablename__ = 'companies_meta'

    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    key = Column(String(256), nullable=False)
    val_type = Column(String(256))
    val_string = Column(Text())
    val_pickle = Column(PickleType())
    val_int = Column(Integer)
    val_date = Column(DateTime)
    company = relationship("Company", back_populates="meta")

    __table_args__ = (
        UniqueConstraint('company_id', 'key', 'val_type', name='uix_1'),
    )
    value = None

    def __repr__(self):
        return '<CompanyMeta %s, %s>' % (self.key, self.id)

    def save(self):
        if self.val_type == 'str':
            self.val_string = self.value
        elif self.val_type == 'date':
            self.val_date = self.value
        elif self.val_type == 'pickle':
            self.val_pickle = self.value
        elif self.val_type == 'int':
            self.val_pickle = self.value
        elif self.val_type == 'date':
            self.val_date = self.value

        # Update meta data if it exists
        duplicate_filter = [
            CompanyMeta.company_id == self.company_id,
            CompanyMeta.key == self.key,
            CompanyMeta.val_type == self.val_type
        ]
        existing_meta = self.query.filter(duplicate_filter).all()
        if existing_meta:
            db.session.commit()
            return

        if not self.id:
            db.session.add(self)
        db.session.commit()


class CompanyDividend(Base):

    __tablename__ = 'companies_dividend'

    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    eff_date = Column(DateTime)                         # This is sometimes reffered to as ex
    declaration_date = Column(DateTime)
    record_date = Column(DateTime)
    pay_date = Column(DateTime)
    price = Column(Float, nullable=False)
    company = relationship("Company", back_populates="dividend")

    def __repr__(self):
        return '<CompanyDividend %s, %s>' % (self.price, self.pay_date)

# End File: stocky/app/models/company.py
