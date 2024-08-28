from server.config import project_id
import dialogflow_v2 as dialogflow
from google.protobuf.json_format import MessageToDict
import json
import os
from ..models import Message
from database.db_instance import db

dirpath = os.path.dirname(os.path.realpath(__file__))

google_key_file = dirpath + '/' + 'newagent-c47af-491a39984c48.json'
# google_key_file = dirpath + '/' + 'telle-ai-dev-rdgebu-64f1c788f7c9.json'


def detect_intent_texts(sid, message):
    message_dict = json.loads(message)
    texts = [message_dict['data']['text']]
    language_code = message_dict.get('language_code', 'en-US')

    session_client = dialogflow.SessionsClient.from_service_account_json(google_key_file)

    session = session_client.session_path(project_id, sid)
    print('Session path: {}\n'.format(session))

    in_message = Message()

    in_message.direction = 'incoming'
    # in_message.message = json.dumps({'messages': texts})
    in_message.message = message
    in_message.session_id = sid
    in_message.from_bot = 0
    in_message.is_read = 0
    in_message.message_owner = 'customer'

    db.session.add(in_message)
    db.session.commit()

    for text in texts:
        text_input = dialogflow.types.TextInput(
            text=text, language_code=language_code)

        query_input = dialogflow.types.QueryInput(text=text_input)

        response = session_client.detect_intent(
            session=session, query_input=query_input)

        print(response)
        response_dict = MessageToDict(response)
        # print(MessageToJson(response))

        text_message = response_dict['queryResult'].get('fulfillmentText')
        messages = response_dict['queryResult'].get('fulfillmentMessages')
        out_message = Message()
        out_message.direction = 'outgoing'
        out_message.message = json.dumps(messages)
        out_message.dialogflow_resp = json.dumps(text_message)
        # out_message.message = json.dumps({'messages': [text_message]})
        out_message.session_id = sid
        out_message.from_bot = 1
        out_message.is_read = 0
        out_message.message_owner = 'bot'

        db.session.add(out_message)
        db.session.commit()

        return messages
