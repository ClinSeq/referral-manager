# coding=utf-8
from datetime import datetime

from sqlalchemy import Column
from sqlalchemy.types import Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class AlasccaBloodReferral(Base):
    __tablename__ = "alascca_bloodreferrals"
    crid = Column(Integer, primary_key=True, nullable=False)
    pnr = Column(String, nullable=False)
    collection_date = Column(Date, nullable=False)
    collection_time = Column(Integer)
    signed = Column(Integer)
    hospital_code = Column(Integer)
    county = Column(String)
    barcode1 = Column(Integer)
    barcode2 = Column(Integer)
    barcode3 = Column(Integer)
    file_name = Column(String)
    type_string = 'ALASCCA_blod'

    def __init__(self, line, separator=";"):
        """ Create an object from a single line in a csv file
        Element order:
        pnr;rid;datum;tid;sign;hospital;county;blood1;blood2;blood3;filnamn
        """
        elm = line.strip("\n").split(separator)
        (self.pnr, self.crid, self.collection_date, self.collection_time, self.signed, self.hospital_code, self.county,
         self.barcode1, self.barcode2, self.barcode3, self.file_name) = elm

        self.collection_date = datetime.strptime(self.collection_date, "%Y%m%d")


class AlasccaTissueReferral(Base):
    __tablename__ = "alascca_tissuereferrals"
    crid = Column(Integer, primary_key=True, nullable=False)
    pnr = Column(String, nullable=False)
    collection_date = Column(Date, nullable=False)
    radiotherapy = Column(Integer)
    sectioning_date = Column(Date)
    pad = Column(String)
    hospital_code = Column(Integer)
    county = Column(String)
    barcode1 = Column(Integer)
    barcode2 = Column(Integer)
    comments = Column(String)
    file_name = Column(String)
    type_string = 'ALASCCA_colon_rektum'

    def __init__(self, line, separator=";"):
        """ Create an object from a single line in a csv file
        Element order:
        pnr;rid;datum;strål_radio;snittningsdatum;PAD-nummer;sjukhus;län;tissue1;tissue2;kommentar;filnamn
        """
        elm = line.strip("\n").split(separator)
        (self.pnr, self.crid, self.collection_date, self.radiotherapy, self.sectioning_date, self.pad,
         self.hospital_code, self.county, self.barcode1, self.barcode2, self.comments, self.file_name) = elm

        self.collection_date = datetime.strptime(self.collection_date, "%Y%m%d")
        if self.sectioning_date == "0":
            self.sectioning_date = None
        else:
            self.sectioning_date = datetime.strptime(self.sectioning_date, "%Y%m%d")
