from sqlalchemy.orm import Session


class BaseRepository:

    def __init__(self, model):
        self.model = model

    def create(self, db: Session, data):
        db_object = self.model(**data.dict())
        db.add(db_object)
        db.commit()
        db.refresh(db_object)
        return db_object

    def get(self, db: Session, object_id: int):
        return db.query(self.model).filter(self.model.id == object_id).first()

    def list(self, db: Session, skip: int = 0, limit: int = 10):
        return db.query(self.model).offset(skip).limit(limit).all()

    def update(self, db: Session, db_object, data):

        for key, value in data.dict().items():
            setattr(db_object, key, value)

        db.commit()
        db.refresh(db_object)

        return db_object

    def delete(self, db: Session, db_object):

        db.delete(db_object)
        db.commit()