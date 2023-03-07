from sqlalchemy.orm import Session
import models, schemas



#get user
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

#by email
def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

#list
def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

#create user

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(email=user.email, hashed_password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


#del user

def del_user(db:Session,email:str):
    response = db.query(models.User).filter(models.User.email==email).first()
    db.delete(response)
    db.commit()
    return {"ok": True}

def update_user(db:Session,details:schemas.UserCreate,user_id:int):
    user= db.query(models.User).filter(models.User.id==user_id).first()
    


    user.email=details.email
    user.hashed_password=details.password
    
    
    db.commit()
    return user


    

def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()


def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
    db_item = models.Item(**item.dict(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item