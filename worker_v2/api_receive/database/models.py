"""Models to use with database."""

from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.dialects.postgresql import TEXT, UUID
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class TblStock(Base):
    """Class to describe tblStock."""

    __tablename__ = 'tblStock'

    lclientorderitemid = Column('lClientOrderItemID', Integer, primary_key=True)
    lvouchernumber = Column('lVoucherNumber', Integer, primary_key=True)
    lvouchertypeid = Column('lVoucherTypeID', Integer)
    stock_strbarcode = Column('Stock_strBarcode', String(50))
    expiry_date = Column('dExpiryDate', Date)


class Template(Base):
    """Class to describer additional template info."""

    __tablename__ = 'template'
    __table_args__ = ({'schema': 'voucher_app'})

    id = Column('id', UUID, primary_key=True)
    template = Column('template_content', TEXT)
    logo_image = Column('logo_image', String(100))
    voucher_image = Column('voucher_image', String(100))
