from datetime import datetime
from flask import request
from flask_socketio import SocketIO, join_room, leave_room
from database.model import Conversation, Message, TypesMessages

socketio = SocketIO(logger=True, engeineio_logger=True)


@socketio.on('message')
def handle_message(message):
    try:
        #{'type_message': "string", 'id_conversation': 1, 'id_user_source': 12, 'message': "gnagnagna", ('file_id' : 0)}
        print('Message reçu:', message)
        id_conv = message["id_conversation"]
        id_user_source = message["id_user_source"]
        msg = message["message"]
        type_message = TypesMessages[message["type_message"]]
        if type_message == TypesMessages.file:
            msg += "//" + message["file_id"]
        
        Message.add_message(id_conv, datetime.now(), id_user_source, type_message, msg)
        send_message(message, id_conv)
    except Exception as e:
        print(e)

@socketio.on('connect')
def handle_connect():
    source_id_user = request.args.get('id_user')
    if not source_id_user:
        raise Exception("Pas d'id utilisateur")
    conversations, _ = Conversation.get_conversations_user(source_id_user)

    for conversation in conversations["Conversations"]:
        join_room(str(conversation["id"]))

@socketio.on('disconnect')
def handle_disconnect():
    source_id_user = request.args.get('id_user')
    print("Disconnect : " + source_id_user)
    if not source_id_user:
        raise Exception("Pas d'id utilisateur")
    conversations, _ = Conversation.get_conversations_user(source_id_user)
    for conversation in conversations["Conversations"]:
        leave_room(str(conversation["id"]))

def send_message(message, room):
    socketio.emit('response',message, to=str(room))
