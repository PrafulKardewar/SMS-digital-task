from typing import List
from pydantic import BaseModel


class ChemicalElement(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class ChemicalCompositionBase(BaseModel):
    pass


class ChemicalComposition(ChemicalCompositionBase):
    element: ChemicalElement
    percentage: int

    class Config:
        orm_mode = True


class AddElement(ChemicalCompositionBase):
    cid: int
    eid: int
    percentage : int


class RemoveElement(ChemicalCompositionBase):
    eid: int
    cid: int


class CommodityUpdate(BaseModel):
    id: int
    name: str
    price: float


class Commodity(CommodityUpdate):
    id: int
    inventory: float

    chemical_composition: List[ChemicalComposition] = []

    class Config:
        orm_mode = True

