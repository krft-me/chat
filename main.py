import os
import logging
from flask import Flask, render_template

from flask import Flask

from api.main import Api

import uuid


# ----------------------------------------

from database import db
from database.model import Conversation, Message

__prg_version__ = "0.0.1"
__prg_name__ = "chat"

CHAT_PORT = 5000
CHAT_HOST = "0.0.0.0"
CHAT_DEBUG = True

global app
app = Flask(__name__)
app.config["VERSION"] = __prg_version__
app.config["APP_PORT"] = CHAT_PORT
app.config["APP_HOST"] = CHAT_HOST
app.config["APP_DEBUG"] = CHAT_DEBUG
app.config['APP_NAME'] = "Chat :)"


# Db sqlite
CHAT_DIR = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(CHAT_DIR, "chat.db"))
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


# register AccessDB
app.register_blueprint(Api(url_prefix="/api"))


@app.route("/", methods=["GET", "POST"])
def accueil_vendeur():
    # conv = Conversation()
    # conv.participants = [10,20]
    # conv.save()
    # Message.add_message(1, datetime.now(), 10, TypesMessages.string, get_random_string(8))
    return render_template('home.html', conversations=Conversation.all(), messages=Message.query.order_by(Message.id_conversation.asc()).all())


# def get_random_string(length):
    # choose from all lowercase letter
    # letters = string.ascii_lowercase
    # result_str = ''.join(random.choice(letters) for i in range(length))
    # return result_str

def create_app():
    db.init_app(app)
    with app.app_context():
        db.create_all()
    with app.app_context():
        for bp in app.blueprints:
            if 'init_db' in dir(app.blueprints[bp]):
                app.blueprints[bp].init_db()
    app.logger.setLevel(logging.DEBUG)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', '123456789')
    return app


app = create_app()
if __name__ == "__main__":
    app.run(host=CHAT_HOST, port=CHAT_PORT, debug=CHAT_DEBUG)
