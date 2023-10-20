from datetime import datetime
from flask import request
from flask_socketio import SocketIO

from database.model import Conversation, Message, TypesMessages

socketio = SocketIO()

active_clients = {}


@socketio.on('message')
def handle_message(message):
    #{'id_conversation': 1, 'id_user_source': 12, 'message': "gnagnagna"}
    print('Message reçu:', message)
    id_conv = message["id_conversation"]
    id_user_source = message["id_user_source"]
    msg = message["msg"]

    Message.add_message(id_conv, datetime.now(), id_user_source, TypesMessages.string, msg)
    conversation = Conversation.query.filter_by(id=id_conv).first()
    for user in conversation.participants:
        if user != id_user_source and user in active_clients.keys():
            send_message(message, user)


@socketio.on('connect')
def handle_connect():
    source_id_user = request.args.get('id_user')
    if not source_id_user:
        raise Exception("Pas d'id utilisateur")
    source_sid_user = request.sid

    # Stockez l'identifiant de session du client dans le dictionnaire
    if source_id_user not in active_clients.keys():
        active_clients[source_id_user] = []
    active_clients[source_id_user].append(source_sid_user)
    print("ID = ", source_id_user)
    print("liste de ses SID : ", active_clients[source_id_user])


@socketio.on('disconnect')
def handle_disconnect():
    source_id_user = request.args.get('id_user')
    if not source_id_user:
        raise Exception("Pas d'id utilisateur")
    source_sid_user = request.sid

    active_clients[source_id_user].remove(source_sid_user)
    if active_clients[source_id_user] == []:
        active_clients.pop(source_id_user, None)
    print("liste des sid restant :", active_clients[source_id_user])
    print('Un client s\'est déconnecté')


def send_message(message, id_user=-1):
    if id_user==-1:
        socketio.emit('response', message)
    else:
        for sid in active_clients[str(id_user)]:
            socketio.emit('response', message, room=sid)
