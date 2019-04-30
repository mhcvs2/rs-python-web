from app import db


class BaseModel(object):

    @classmethod
    def get_by_id(cls, _id):
        return db.session.query(cls).filter_by(id=_id).first()
