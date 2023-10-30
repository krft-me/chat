from flask import Blueprint, request, jsonify
from database.model import Conversation, Message


def get_conversations_user(id_user):
    return Conversation.get_conversations_user(id_user)


def get_messages_conversation(id_conversation, page):
    return Message.get_conversation(id_conversation, page)

def post_conversation():
    participants = request.get_json()["participants"]
    return {"Id": Conversation.add_conversation(participants).id}, 200



class Api(Blueprint):
    def __init__(self, name='api', import_name=__name__, *args, **kwargs):
        Blueprint.__init__(self, name, import_name,
                           template_folder='templates', *args, **kwargs)

        # GET
        self.add_url_rule('/conversations/<int:id_user>',
                          'get_conversations_user', get_conversations_user, methods=['GET'])
        self.add_url_rule('/messages/<int:id_conversation>/<int:page>',
                          'get_messages_conversation', get_messages_conversation, methods=['GET'])

        # POST
        self.add_url_rule('/conversations', 'conversations_user',
                          post_conversation, methods=['POST'])


    def register(self, app, options):
        try:
            Blueprint.register(self, app, options)
        except Exception:
            app.logger.error("init API on register is failed")
