from flask import jsonify, request
import logging
from flask_cors import CORS
from flask_socketio import SocketIO, emit, join_room, leave_room, rooms, close_room
import json
from chatbot.utils.update_db import (update_group, update_chat, update_leads, inquiry_leads,
                                     create_lead_from_intent, update_lead_from_intent)
from chatbot.utils.update_appt import update_appt_from_intent
from server.server import app
from flask_restful import Api
import random


logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M',
                    filename='bm-bot-middleware.log',
                    filemode='a')

logger = logging.getLogger()
logger.setLevel(logging.INFO)

app.config['SECRET_KEY'] = 'secret!'
CORS(app)
socketio = SocketIO(app, cors_allowed_origins='*')

api = Api(app)

'''
room map format: 
{
room_key: {user: [session_id], bot: [session_id], admin: [session_id], muted: True}
}
'''
room_map = {}

user_room_map = {}

admin_room_map = {}

daemon_room_map = {}

bot_sid = []
admin_sid = []

daemon_bot_sid = []


@app.route('/hello')
def hello():
    return 'Hello World'


@app.route('/api/inquiry_stock', methods=['POST'])
def inquiry_stock():
    dealerId = request.form.get('dealerId', 'dthonda')
    customer = request.form.get('customer', 'customer')
    email = request.form.get('email', '')
    phone = request.form.get('phone', '')
    zipcode = request.form.get('zipcode', '')
    vin = request.form.get('vin', '')
    stock = request.form.get('stock', '')
    sessionId = request.form.get('sessionId', '')
    new_message = {
        'dealerId': dealerId,
        'customer': customer,
        'email': email,
        'phone': phone,
        'note': '',
        'zipcode': zipcode,
        'vin': vin,
        'stock': stock,
        'sessionId': sessionId
    }

    print(new_message)

    inquiry_leads(new_message)

    for key in admin_room_map:
        socketio.emit('LEADS_NOTIFICATION', json.dumps(new_message), room=key)

    return json.dumps({
               'isError': False,
               'message': 'leads has been created',
               'statusCode': 200
           })


@app.route('/api/create_lead', methods=['POST'])
def create_lead_bot():
    dealerId = request.form.get('dealerId', 'dthonda')
    customer = request.form.get('customer', 'customer')
    email = request.form.get('email', '')
    phone = request.form.get('phone', '')
    note = request.form.get('note', '')
    sessionId = request.form.get('sessionId', '')
    new_message = {
        'dealerId': dealerId,
        'customer': customer,
        'email': email,
        'phone': phone,
        'note': note,
        'sessionId': sessionId
    }

    print(new_message)

    update_leads(new_message)

    for key in admin_room_map:
        socketio.emit('LEADS_NOTIFICATION', json.dumps(new_message), room=key)

    return json.dumps({
               'isError': False,
               'message': 'leads has been created',
               'statusCode': 200
           })


@app.route('/api/create_new_lead')
def create_new_leads():
    print(request)
    customer = request.args.get('customer')
    # email = request.args.get('email')
    # phone = request.args.get('phone')
    session_id = request.args.get('sessionId')

    department = request.args.get('department')
    message = {}
    if customer:
        message['customer'] = customer

    if session_id:
        message['sessionId'] = session_id

    if department:
        message['department'] = department
    create_lead_from_intent(message)

    return json.dumps({
               'isError': False,
               'message': 'leads has been created',
               'statusCode': 200
           })


@app.route('/api/update_new_lead')
def update_new_leads():
    print(request)
    email = request.args.get('email')
    phone = request.args.get('phone')
    session_id = request.args.get('sessionId')
    department = request.args.get('department')
    customer = request.args.get('customer')
    message = {}
    if phone:
        message['phone'] = phone
    if email:
        message['email'] = email
    if session_id:
        message['sessionId'] = session_id
    if department:
        message['department'] = department
    if customer:
        message['customer'] = customer
    print(message)
    update_lead_from_intent(message)

    for key in admin_room_map:
        socketio.emit('LEADS_NOTIFICATION', json.dumps(message), room=key)

    return json.dumps({
               'isError': False,
               'message': 'leads has been created',
               'statusCode': 200
           })


@app.route('/api/create_new_appt', methods=['POST'])
def create_new_appt():
    logger.info(request)

    keys = {
        "VehicleType": "VehicleType",
        "VehicleDrivetrain": "VehicleDrivetrain",
        "VehicleBudget": "VehicleBudget",
        "VehicleColor": "VehicleColor",
        "VehicleMake": "VehicleMake",
        "VehicleModel": "VehicleModel",
        "VehicleFeatures": "VehicleFeatures",  # list
        "VehicleYear": "VehicleYear",
        "test_drive_date": "test_drive_date",
        "test_drive_time": "test_drive_time",
        "person": "person",  # dict
        "email": "email",
        "phone-number": "phone-number",
        "sessionId": "sessionId"
    }

    message = {}
    for key in keys:
        val = request.form.get(key)
        if val:
            message[key] = val

    update_appt_from_intent(message)

    for key in admin_room_map:
        socketio.emit('LEADS_NOTIFICATION', message, room=key)

    return json.dumps({
        'isError': False,
        'message': 'leads has been created',
        'statusCode': 200
    })


@socketio.on('connect')
def handle_connect():
    # print('Client: {} connected. Rooms: {}'.format(request.sid, rooms()))
    logger.info('Client: {} connected. Rooms: {}'.format(request.sid, rooms()))
    emit('ON_CONNECTION', 'you have connected..........')


@socketio.on('disconnect')
def handle_disconnect():
    # print('Client: {} disconnected'.format(request.sid))
    logger.info('Client: {} disconnected'.format(request.sid))

    # close room
    sid = request.sid

    # Allow multiple users in the same room: mimic open multiple pages
    if sid in user_room_map:
        room = user_room_map[sid]
        del user_room_map[sid]

        if room in room_map and sid in room_map[room]['user']:
            room_map[room]['user'].remove(sid)

        if len(room_map[room]['user']) == 0:

            del room_map[room]

            # update_group(room, 0)

            update_chat(room, close=True)

            close_room(room)
            emit('MUTE_STATE', json.dumps([{'groupId': room, 'online': False, 'muted': False}]), room='admin')

    elif sid in bot_sid:
        bot_sid.remove(sid)
        for key, value in room_map.items():
            if 'bot' in value and sid in value['bot']:
                leave_room(key, sid=sid)
                if len(bot_sid) > 0:
                    new_sid = random.choice(bot_sid)
                    join_room(key, sid=new_sid)
                    value['bot'].remove(sid)
                    value['bot'].append(new_sid)
                else:
                    value['bot'].remove(sid)
    elif sid in admin_sid:
        admin_sid.remove(sid)
        for key, value in room_map.items():
            if 'admin' in value and sid in value['admin']:
                value['admin'].remove(sid)
                leave_room(key, sid=sid)
        if 'admin' in admin_room_map and sid in admin_room_map['admin']:
            admin_room_map['admin'].remove(sid)
    elif sid in daemon_bot_sid:
        daemon_bot_sid.remove(sid)
        for key, value in room_map.items():
            if 'daemon' in value and sid in value['daemon']:
                leave_room(key, sid=sid)
                if len(daemon_bot_sid) > 0:
                    new_sid = random.choice(daemon_bot_sid)
                    join_room(key, sid=new_sid)
                    value['daemon'].remove(sid)
                    value['daemon'].append(new_sid)
                else:
                    value['daemon'].remove(sid)


@socketio.on('redis_test')
def redis_test(message):
    print(message)


@socketio.on('join')
def customer_join(message):
    # print(message)
    # print('Received message from: {}, content: {}'.format(request.sid, message))
    logger.info('Received message from: {}, content: {}'.format(request.sid, message))
    data = json.loads(message)
    room = data['room']

    flag = False
    if room in room_map:
        room_map[room]['user'].append(request.sid)
    else:
        room_map[room] = {'user': [request.sid], 'bot': [], 'admin': [], 'daemon': [], 'muted': False}
        flag = True

    user_room_map[request.sid] = room
    join_room(room)

    if len(room_map[room]['bot']) == 0 and len(bot_sid) > 0:
        room_map[room]['bot'].append(random.choice(bot_sid))
        room_map[room]['muted'] = False

        join_room(room, sid=room_map[room]['bot'][0])

    if len(room_map[room]['daemon']) == 0 and len(daemon_bot_sid) > 0:
        room_map[room]['daemon'].append(random.choice(daemon_bot_sid))
        join_room(room, sid=room_map[room]['daemon'][0])

    if len(room_map[room]['admin']) == 0 and len(admin_sid) > 0:
        for admin in admin_sid:
            room_map[room]['admin'].append(admin)
            join_room(room, sid=admin)

    if flag:
        update_group(room, 1)
        update_chat(room, close=False)
        emit('MUTE_STATE', json.dumps([{'groupId': room, 'online': True, 'muted': False}]), room='admin')

    logger.info('Update Group: {}, Update Chat: {}'.format(room, room))
    # print('Update Group: {}, Update Chat: {}'.format(room, room))


@socketio.on('admin_join')
def admin_join(message):
    data = json.loads(message)
    username = data['username']
    admin_sid.append(request.sid)
    # print(request.sid)
    for key in room_map:
        # print('Room Key: {} Value: {}'.format(key, room_map[key]))
        if 'admin' not in room_map[key]:
            room_map[key]['admin'] = [request.sid]
            join_room(key, sid=request.sid)
        elif request.sid not in room_map[key]['admin']:
            room_map[key]['admin'].append(request.sid)
            join_room(key, sid=request.sid)

    if 'admin' not in admin_room_map:
        admin_room_map['admin'] = [request.sid]
        join_room('admin', sid=request.sid)
    elif request.sid not in admin_room_map['admin']:
        admin_room_map['admin'].append(request.sid)
        join_room('admin', sid=request.sid)

    messages = []
    for key in room_map:
        messages.append({
            'groupId': key,
            'online': True,
            'muted': room_map[key]['muted']
        })

    emit('MUTE_STATE', json.dumps(messages), room='admin')


@socketio.on('bot_join')
def bot_join(message):
    data = json.loads(message)
    username = data['username']
    bot_sid.append(request.sid)
    join_room('admin', sid=request.sid)
    for key in room_map:
        # print('Room Key: {} Value: {}'.format(key, room_map[key]))
        if 'bot' not in room_map[key]:
            room_map[key]['bot'] = [request.sid]
            join_room(key, sid=request.sid)
        elif len(room_map[key]['bot']) == 0:
            room_map[key]['bot'].append(request.sid)
            join_room(key, sid=request.sid)


@socketio.on('daemon_join')
def daemon_join(message):
    data = json.loads(message)
    username = data['username']
    daemon_bot_sid.append(request.sid)
    for key in room_map:
        # print('Room Key: {} Value: {}'.format(key, room_map[key]))
        if 'daemon' not in room_map[key]:
            room_map[key]['daemon'] = [request.sid]
            join_room(key, sid=request.sid)
        elif len(room_map[key]['daemon']) == 0:
            room_map[key]['daemon'].append(request.sid)
            join_room(key, sid=request.sid)


@socketio.on('leave')
def on_leave(data):
    username = data['username']
    room = data['room']
    leave_room(room)


@socketio.on('mute_bot')
def on_mute_bot(data):
    data = json.loads(data)
    room = data['room']
    room_members = room_map.get(room)
    # print('Room {} Mute Bot'.format(room))
    logger.info('Room {} Mute Bot'.format(room))
    if room_members:
        bot = room_members.get('bot', [])

        if len(bot) > 0:
            room_map[room]['muted'] = True
            for bot_id in room_map[room]['bot']:
                logger.info('Bot {} deleted from room {}'.format(bot_id, room))
                # print('Bot {} deleted from room {}'.format(bot_id, room))
                leave_room(room, sid=bot_id)
            room_map[room]['bot'] = []

    emit('MUTE_STATE', json.dumps([{'groupId': room, 'online': True, 'muted': True}]), room='admin')
    print('Available Bots: {}, Available admin: {}, Room Map: {}'.format(bot_sid, admin_sid, room_map))
    logger.info('Available Bots: {}, Available admin: {}, Room Map: {}'.format(bot_sid, admin_sid, room_map))


@socketio.on('unmute_bot')
def on_unmute_bot(data):
    data = json.loads(data)
    room = data['room']
    # print('Room {} UnMute Bot'.format(room))
    logger.info('Room {} UnMute Bot'.format(room))
    room_members = room_map.get(room)
    if room_members:
        bot = room_members.get('bot', [])
        if len(bot) == 0 and len(bot_sid) > 0:
            room_map[room]['muted'] = False
            new_sid = random.choice(bot_sid)
            room_map[room]['bot'].append(new_sid)
            logger.info('Bot {} joined room {}'.format(new_sid, room))
            join_room(room, sid=new_sid)

    emit('MUTE_STATE', json.dumps([{'groupId': room, 'online': True, 'muted': False}]), room='admin')
    print('Available Bots: {}, Available admin: {}, Room Map: {}'.format(bot_sid, admin_sid, room_map))

    logger.info('Available Bots: {}, Available admin: {}, Room Map: {}'.format(bot_sid, admin_sid, room_map))


@socketio.on('end_session')
def on_end_session(data):
    data = json.loads(data)
    room = data['room']

    if room in room_map:
        update_chat(room, close=True)
        # del room_map[room]
        # for key in list(user_room_map):
        #     if user_room_map[key] == room:
        #         del user_room_map[key]
        # close_room(room)
        data['message']['author'] = 'admin'
        emit('CHAT_MESSAGE', json.dumps(data), room=room)


@socketio.on('customer_message')
def handle_customer_message(message):
    '''
    :param message:
    :return:
    '''
    message = json.loads(message)
    print('Received Message from customer: {}, message: {}'.format(request.sid, message))

    logger.info('Received Message from customer: {}, message: {}'.format(request.sid, message))
    to_room_id = message['groupId']

    if request.sid in user_room_map:
        if to_room_id not in room_map:
            room_map[to_room_id] = {'user': [request.sid], 'bot': [], 'daemon': [], 'admin': [], 'muted': False}
            if len(bot_sid) > 0:
                bot_id = random.choice(bot_sid)
                room_map[to_room_id]['bot'].append(bot_id)
                join_room(to_room_id, sid=bot_id)
            if len(daemon_bot_sid) > 0:
                daemon_id = random.choice(daemon_bot_sid)
                room_map[to_room_id]['daemon'].append(daemon_id)
                join_room(to_room_id, sid=daemon_id)
            if len(admin_sid) > 0:
                for admin_id in admin_sid:
                    room_map[to_room_id]['admin'].append(admin_id)
                    join_room(to_room_id, sid=admin_id)
        else:
            if len(room_map[to_room_id]['admin']) == 0:
                if len(admin_sid) > 0:
                    for admin_id in admin_sid:
                        room_map[to_room_id]['admin'].append(admin_id)
                        join_room(to_room_id, sid=admin_id)
            if not room_map[to_room_id]['muted'] and len(room_map[to_room_id]['bot']) == 0:
                if len(bot_sid) > 0:
                    bot_id = random.choice(bot_sid)
                    room_map[to_room_id]['bot'].append(bot_id)
                    join_room(to_room_id, sid=bot_id)

    message['message']['author'] = 'user'
    # print('Available Bots: {}, Available admin: {}, Room Map: {}'.format(bot_sid, admin_sid, room_map))
    logger.info('Available Bots: {}, Available admin: {}, Room Map: {}'.format(bot_sid, admin_sid, room_map))

    emit('CHAT_MESSAGE', json.dumps(message), room=to_room_id)


@socketio.on('admin_message')
def handle_admin_message(message):
    # print(message)

    message = json.loads(message)

    to_room_id = message['groupId']

    message['message']['author'] = 'admin'

    emit('CHAT_MESSAGE', json.dumps(message), room=to_room_id)


@socketio.on('bot_message')
def handle_bot_message(message):
    # print(message)

    new_message = json.loads(message)

    to_room_id = new_message['groupId']

    emit('CHAT_MESSAGE', message, room=to_room_id)


@socketio.on('dialogflow_message')
def handle_dialogflow_message(message):
    message = json.loads(message)
    # print('Received Message from customer: {}, message: {}'.format(request.sid, message))

    logger.info('Received Message from customer: {}, message: {}'.format(request.sid, message))
    to_room_id = message['groupId']

    if request.sid in user_room_map:
        if to_room_id not in room_map:
            room_map[to_room_id] = {'user': [request.sid], 'bot': [], 'admin': [], 'muted': False}
            if len(bot_sid) > 0:
                bot_id = random.choice(bot_sid)
                room_map[to_room_id]['bot'].append(bot_id)
                room_map[to_room_id]['muted'] = False
                join_room(to_room_id, sid=bot_id)
        elif len(room_map[to_room_id]['admin']) == 0:
            if len(bot_sid) > 0:
                bot_id = random.choice(bot_sid)
                room_map[to_room_id]['bot'].append(bot_id)
                room_map[to_room_id]['muted'] = False
                join_room(to_room_id, sid=bot_id)
        elif room_map[to_room_id]['muted'] == False and len(room_map[to_room_id]['bot']) == 0:
            if len(bot_sid) > 0:
                bot_id = random.choice(bot_sid)
                room_map[to_room_id]['bot'].append(bot_id)
                join_room(to_room_id, sid=bot_id)

    message['message']['author'] = 'user'
    # print('Available Bots: {}, Available admin: {}, Room Map: {}'.format(bot_sid, admin_sid, room_map))
    logger.info('Available Bots: {}, Available admin: {}, Room Map: {}'.format(bot_sid, admin_sid, room_map))

    emit('CHAT_MESSAGE', json.dumps(message), room=to_room_id)


@socketio.on('create_leads')
def create_leads(message):
    print(message)

    new_message = json.loads(message)

    update_leads(new_message)

    for key in admin_room_map:
        emit('LEADS_NOTIFICATION', message, room=key)


@socketio.on('create_new_lead')
def create_new_lead(message):
    print(message)

    new_message = json.loads(message)

    update_lead_from_intent(new_message)

    for key in admin_room_map:
        emit('LEADS_NOTIFICATION', message, room=key)

# @socketio.on('send_meta')
# def update_meta(message):
#     print(message)
#
#     ip_addr = request.remote_addr
#     print(ip_addr)
#     new_message = json.loads(message)
#     new_message['ip_addr'] = ip_addr
#     update_user(new_message, request.sid)


# if __name__ == '__main__':
#     socketio.run(app=app, debug=True)
