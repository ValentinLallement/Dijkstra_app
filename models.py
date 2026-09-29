from sqlalchemy import Integer,String,Column,Float
from sqlalchemy.orm import Mapped
from sqlalchemy.dialects.postgresql import ARRAY

from database import Base

class Chemin(Base):
    __tablename__ = "chemins"

    id = Column(Integer, primary_key=True)
    depart = Column(String, index=True)
    arrivee = Column(String, index=True)
    arrets = Column(ARRAY(String))
    temps_total = Column(Float)