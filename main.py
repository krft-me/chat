import os
import logging
from flask import Flask, render_template

__prg_version__ = "0.0.1"
__prg_name__ = "chat"

CHAT_PORT = 5000
CHAT_HOST = "0.0.0.0"
CHAT_DEBUG = True

app = Flask(__name__)
app.config["VERSION"] = __prg_version__
app.config["APP_PORT"] = CHAT_PORT
app.config["APP_HOST"] = CHAT_HOST
app.config["APP_DEBUG"] = CHAT_DEBUG
app.config['APP_NAME'] = "Chat :)"


# Db sqlite
#CHAT_DIR = os.path.dirname(os.path.abspath(__file__))
#database_file = "sqlite:///{}".format(os.path.join(CHAT_DIR, "chat.db"))
#app.config["SQLALCHEMY_DATABASE_URI"] = database_file
#app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

@app.route("/", methods=["GET", "POST"])
def accueil_vendeur():
    return render_template('home.html')


def create_app():
    # db.init_app(app)
    # with app.app_context():
    # db.create_all()
    with app.app_context():
        for bp in app.blueprints:
            if 'init_db' in dir(app.blueprints[bp]):
                app.blueprints[bp].init_db()
    app.logger.setLevel(logging.DEBUG)
    return app


app = create_app()
if __name__ == "__main__":
    app.run(host=CHAT_HOST, port=CHAT_PORT, debug=CHAT_DEBUG)
