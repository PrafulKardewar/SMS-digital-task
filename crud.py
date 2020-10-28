from sqlalchemy.orm import Session
from fastapi import HTTPException
import models


def get_all_chemical_elements(db: Session, skip: int = 0):
    elements = db.query(models.ChemicalElement).offset(skip).all()
    return elements


def get_commodity_by_id(db, commodity_id: int):
    return db.query(models.Commodity).filter(models.Commodity.id == commodity_id).first()


def update_commodity(db, result):
    db_commodity = get_commodity_by_id(db, commodity_id=result['id'])
    if db_commodity is None:
        raise HTTPException(status_code=404, detail="Commodity  not found")
    else:
        db_commodity.name = result['name']
        db_commodity.price = result['price']
        db.commit()
        db.refresh(db_commodity)
        db_commodity = get_commodity_by_id(db, commodity_id=result['id'])
        return db_commodity


def add_chemical_concentration(result, db):
    sum = 0
    element = db.query(models.ChemicalElement).filter(models.ChemicalElement.id == result["eid"]).first()
    if element:
        perecntage = db.query(models.ChemicalComposition.percentage).filter(models.Commodity.id == result["cid"]).all()
        for item in perecntage:
            sum = sum + item[0]
        sum = sum + result["percentage"]
        unknown = 100 - sum
        if sum < 100:
            composition1 = models.ChemicalComposition(eid=result["eid"], cid=result["cid"], percentage=result["percentage"])
            db.add(composition1)
            db.commit()
            db.refresh(composition1)
            composition2 = models.ChemicalComposition(eid=5, cid=result["cid"], percentage=unknown)
            db.add(composition2)
            db.commit()
            db.refresh(composition2)
        else:
            composition = models.ChemicalComposition(eid=result["eid"], cid=result["cid"], percentage=result["percentage"])
            db.add(composition)
            db.commit()
            db.refresh(composition)
    else:
        raise HTTPException(status_code=400, detail="element with this id is not present")
    return get_commodity_by_id(db, commodity_id=result["cid"])


def remove_chemical_concentration(db, result):
    is_commodity = db.query(models.Commodity).filter(models.Commodity.id == result["cid"]).first()
    if is_commodity:
        element = db.query(models.ChemicalComposition).filter(models.ChemicalComposition.eid == result["eid"]).first()
        if element:
            db.query(models.ChemicalComposition).filter(models.ChemicalComposition.eid == result["eid"]).delete()
            db.commit()
        else:
            raise HTTPException(status_code=404, detail="element not found")
    else:
        raise HTTPException(status_code=404, detail="commodity not found")
    return is_commodity
