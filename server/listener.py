import threading
import logging
import json
from flask_socketio import emit

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class Listener(threading.Thread):
    def __init__(self, r, channels, app):
        threading.Thread.__init__(self)
        self.daemon = True
        self.redis = r
        self.pubsub = self.redis.pubsub()
        self.pubsub.psubscribe(channels)
        self.app = app

    def work(self, item):
        with self.app.app_context():
            if isinstance(item['data'], bytes):
                try:
                    msg = item['data'].decode('utf-8')
                    decode_msg = json.loads(msg)
                    print(decode_msg)
                    if decode_msg['type'] == 'UPDATE_TASK':
                        emit('CHAT_MESSAGE', json.dumps(
                            {'groupId': '066f0fcd014d48a5aec08b36bcce99d5',
                             'message': {'author': 'admin', 'type': 'text', 'data': {'text': 'service'}},
                             'tag': 'admin',
                             'unread': 0,
                             'uid': 'dc96dcec4bf54b5797e701370ba899e8'}
                        ), room=decode_msg['room'], namespace='/')
                    #_send_task_message()
                except ValueError as e:
                    print("Error decoding msg to microservice: %s", str(e))

    def run(self):
        for item in self.pubsub.listen():

            self.work(item)
