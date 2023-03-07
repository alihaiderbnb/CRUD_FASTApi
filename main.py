from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

import crud, models, schemas
from database import SessionLocal, engine

from fastapi.security import OAuth2PasswordBearer
from passlib.hash import bcrypt

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

#pwd_context= CryptContext(schemes=["bcrypt"], deprecated='auto')


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def verify_password(plain_password, hashed_password):
    return bcrypt.verify(plain_password, hashed_password)


def get_password_hash(password):
    return bcrypt.hash(password)


#create user
@app.post("/users/", response_model=schemas.User)
def create_user(myuser: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=myuser.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    myuser.password = get_password_hash(myuser.password)
    return crud.create_user(db=db, user=myuser)

#login
@app.post("/user/login", response_model=schemas.User)
def login_user(myuser: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=myuser.email)
    if db_user is None:
        raise HTTPException(status_code=404, detail="No user exist")
    verify_password(myuser.password, db_user.hashed_password)
    return db_user
   


    


@app.get("/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

# get single user by id
@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    #Now here we will call a fucntion
    ##to decode the token
    ## that function will decode the token retrive the information
    # and send it back to the caller function


    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

#delete a user by email
@app.delete("/user/{user_email}")
def delete_user(user_email:str, db: Session = Depends(get_db)):
    return crud.del_user(db=db, email=user_email)


#update a user details by its ID

@app.put("/user/{user_id}", response_model=schemas.UserCreate)
def update_item(user_id: int ,details : schemas.UserCreate,db:Session=Depends(get_db)):
    db_user= crud.get_user(db=db,user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="No user")
    return crud.update_user(db=db,details=details,user_id=user_id)

    
 


#create items for the user
@app.post("/users/{user_id}/items/", response_model=schemas.Item)
def create_item_for_user(
    user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)
):
    return crud.create_user_item(db=db, item=item, user_id=user_id)

#get list of items

@app.get("/items/", response_model=list[schemas.Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_items(db, skip=skip, limit=limit)
    return items