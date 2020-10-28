from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class ChemicalElement(Base):
    __tablename__ = "chemical_element"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True)
    chem_comp = relationship("ChemicalComposition", back_populates="element")

class Commodity(Base):
    __tablename__ = "commodity"

    id=Column(Integer, primary_key=True, index=True)
    name=Column(String(100), unique=True)
    inventory=Column(Float)
    price=Column(Float)
    chemical_composition=relationship("ChemicalComposition")


class ChemicalComposition(Base):
    __tablename__ = "chemical_composition"

    id = Column(Integer, primary_key=True, index=True)
    eid =Column(Integer, ForeignKey("chemical_element.id"))
    percentage=Column(Integer)
    cid =Column(Integer, ForeignKey("commodity.id"))
    element = relationship("ChemicalElement", back_populates="chem_comp")

