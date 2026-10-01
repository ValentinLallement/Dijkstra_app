from sqlalchemy import Integer,String,Column,Float,JSON
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

class Ligne(Base):
    __tablename__ = "lignes"

    id = Column(Integer, primary_key=True, index=True)

    nom = Column(
        String,
        nullable=False,
        index=True
    )

    sommets = Column(
        JSON,
        nullable=False
    )

    aretes = Column(
        JSON,
        nullable=False
    )