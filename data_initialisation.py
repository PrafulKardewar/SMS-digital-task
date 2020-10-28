



import models
from database import SessionLocal


def add_basic_info(skip: int = 0, limit: int = 100,db=SessionLocal()):
    all_elements = ["C", "N", "O", "AI", "Unknown", "Fe", "Cu"]

    for i in all_elements:
        db_item = models.ChemicalElement(name=i)
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
    db_item = models.Commodity(id=10, name="Plate & Structural", inventory=200.1, price=334.44)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    db_item= db.query(models.Commodity).filter(models.Commodity.id == 10).first()
    elements = db.query(models.ChemicalElement).offset(skip).limit(limit).all()
    elements=list(elements)
    percentages=[25,15,10,15]
    for i in range(4):
        composition = models.ChemicalComposition(eid=elements[i].id, cid=db_item.id, percentage=percentages[i])
        db.add(composition)
        db.commit()
        db.refresh(composition)