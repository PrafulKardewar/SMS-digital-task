from typing import List
import uvicorn
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
import crud, models, schemas
from database import SessionLocal, engine
from fastapi.security import OAuth2PasswordRequestForm
from jwt_user import JwtUser
from authentication import authenticate_user, create_jwt_token, check_jwt_token
from starlette.status import HTTP_401_UNAUTHORIZED
from data_initialisation import add_basic_info
app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/elements/", response_model=List[schemas.ChemicalElement])
async def read_all_available_elements(skip: int = 0, db: Session = Depends(get_db),jwt: bool =Depends(check_jwt_token)):
    elements = crud.get_all_chemical_elements(db, skip=skip)
    return elements


@app.get("/commodity/{commodity_id}", response_model=schemas.Commodity)
async def read_commodity(commodity_id: int, db: Session = Depends(get_db),jwt: bool =Depends(check_jwt_token)):
    db_commodity = crud.get_commodity_by_id(db, commodity_id=commodity_id)
    if db_commodity is None:
        raise HTTPException(status_code=404, detail="Commodity  not found")
    return db_commodity


@app.post("/add/concentration/", response_model=schemas.Commodity)
async def add_concentration_to_commodity(commodity: schemas.AddElement, db: Session = Depends(get_db),jwt: bool =Depends(check_jwt_token)):
    result = {**commodity.dict()}
    return crud.add_chemical_concentration(result,db)


@app.delete("/remove/concentration/", response_model=schemas.Commodity)
async def remove_concentration_from_commodity(commodity: schemas.RemoveElement, db: Session = Depends(get_db),jwt: bool =Depends(check_jwt_token)):
    result = {**commodity.dict()}
    return crud.remove_chemical_concentration(db, result)


@app.patch("/commodity/update/", response_model=schemas.Commodity)
async def update_commodity_by_id(commodity: schemas.CommodityUpdate, db: Session = Depends(get_db)):#,jwt: bool =Depends(check_jwt_token)):
   result = {**commodity.dict()}
   return crud.update_commodity(db, result)



@app.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    jwt_user_dict = {"username": form_data.username, "password": form_data.password }
    jwt_user = JwtUser(**jwt_user_dict)
    user = authenticate_user(jwt_user)
    if user is False:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED)
    jwt_token = create_jwt_token(user)
    return {"token": jwt_token}




if __name__ == "__main__":
    models.Base.metadata.create_all(bind=engine)
    add_basic_info()
    uvicorn.run('main:app', host="127.0.0.1", port=8000,reload=True)

