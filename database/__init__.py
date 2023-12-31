from flask_sqlalchemy import SQLAlchemy, Model
import enum


class GenericModel(Model):

    @classmethod
    def get(cls, id):
        try:
            return cls.query.filter_by(id=id).first()
        except Exception:
            return None

    @classmethod
    def all(cls, sortby=None):
        if sortby:
            return cls.query.order_by(sortby).all()
        return cls.query.all()

    @classmethod
    def remove(cls, id):
        try:
            cls.query.filter_by(id=id).first().remove()
            return True
        except Exception:
            return False

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception:
            db.session.commit()
            return False

    def remove(self):
        db.session.delete(self)
        db.session.commit()

    def to_dict(self):
        dict = {}
        for c in self.__table__.columns:
            if issubclass(getattr(self, c.name).__class__, enum.Enum):
                dict[c.name] = getattr(self, c.name).value
            else:
                dict[c.name] = getattr(self, c.name)

        return dict



db = SQLAlchemy(model_class=GenericModel)
