from database import db
import enum
from sqlalchemy import Enum
from datetime import datetime

class TypesMessages(enum.Enum):
    string = "string"
    file = "file"


class Conversation(db.Model):
    __tablename__ = 'conversation'

    id = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    participants = db.Column(db.PickleType, index=True)
    last_message = db.Column(db.DateTime, nullable=False)

    @classmethod
    def add_conversation(cls, participants):
        conv = Conversation()
        conv.participants = participants
        conv.last_message = datetime.now()
        conv.save()
        return conv
    
    @classmethod
    def get_conversations_user(cls, user):
        all_conv = Conversation.query.order_by(Conversation.last_message.desc()).all()
        liste_conv = []
        for conv in all_conv:
            if int(user) in conv.participants:
                liste_conv.append(conv.to_dict())
        return {"Conversations" : liste_conv}, 200
    
    


class Message(db.Model):
    __tablename__ = 'message'

    id_conversation = db.Column(db.Integer, db.ForeignKey('conversation.id'), nullable=False, primary_key=True)
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    expediteur = db.Column(db.Integer, nullable=False)
    type_message = db.Column(Enum(TypesMessages), nullable=False, default="string")
    message = db.Column(db.String, nullable=False)

    def to_dict(self):
        dict = {}
        for c in self.__table__.columns:
            if c.name != "message":
                if c.name == "type_message":
                    dict[c.name] = self.__dict__[c.name].value
                    if c.type.python_type(self.__dict__[c.name]).name == "file":
                        dict["file_id"] = self.message.split("//")[1]
                        dict["message"] = self.message.split("//")[0]
                    else:
                        dict["message"] = self.message
                else:
                    dict[c.name] = self.__dict__[c.name]

        return dict

    @classmethod
    def add_message(cls, id_conversation, date, expediteur, type_message, message):
        conv = Conversation.get(id_conversation)
        if expediteur not in conv.participants:
            return False, "erreur, expediteur non présent dans la conversation"
        if type_message not in TypesMessages._member_map_.values():
            return False, "Type de message non existant"
        msg = Message()
        msg.id_conversation = id_conversation
        last_msg = Message.query.filter_by(id_conversation=id_conversation).order_by(Message.id.desc()).first()
        msg.id = last_msg.id+1 if last_msg else 0
        msg.date = date
        msg.expediteur = expediteur
        msg.type_message = type_message
        msg.message = message
        msg.save()
        conv.last_message = date
        conv.save()
        return True

    @classmethod
    def get_conversation(cls, id, page):
        conv = Conversation.get(id)
        if not conv:
            return {}, 404
        messages = Message.query.filter_by(id_conversation=id).order_by(Message.id.desc()).paginate(page=page, per_page=10)
        liste_msg = []
        for message in messages:
            liste_msg.append(message.to_dict())
        return {"Messages": liste_msg}, 200

