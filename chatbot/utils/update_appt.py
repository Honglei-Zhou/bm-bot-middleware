import os
from ..models import Lead, Message
from datetime import datetime, timezone
from .send_email import send_email
import pytz
import json
from dateutil.parser import parse
from sqlalchemy import desc
from sqlalchemy import and_
from .create_appt_email_body import create_appt_email_body


local_tz = pytz.timezone('America/Chicago')

dirpath = os.path.dirname(os.path.realpath(__file__))

serive_recipients = [
    'joel.adames@dthondachicago.com',
    # 'lisa.pagan@dthondachicago.com',
    'ben.scribner@dthondachicago.com',
    'nick.neessen@dthondachicago.com',
    'davie.anderson@dthondachicago.com',
    'raffayhussain@blissmotors.com'
]

sales_recipients = [
    'gary.wexler@dthondachicago.com',
    # 'lisa.pagan@dthondachicago.com',
    'davie.anderson@dthondachicago.com',
    'ben.scribner@dthondachicago.com',
    'nick.neessen@dthondachicago.com',
    'Olivia.Almarales@BrickellMotors.com',
    'raffayhussain@blissmotors.com'
]


def utc_to_local(utc_dt):
    return utc_dt.replace(tzinfo=timezone.utc).astimezone(local_tz)


def update_appt_from_intent(data):
    try:
        print(data)
        dealer_id = data.get('dealerId', 'dthonda')

        customer_name = data.get('person', 'customer')

        email = data.get('email', '')
        phone = data.get('phone', '')
        session_id = data.get('sessionId', '')

        appointment = data.get('test_drive_time', None)

        department = data.get('department', 'sales')
        handler = data.get('handleBy', 'not available')

        priority = data.get('importance', 1)

        status = data.get('status', 'New')

        leads = Lead(
            dealer_id=dealer_id,
            customer_name=customer_name,
            created=datetime.utcnow(),
            email=email,
            phone=phone,
            department=department,
            handler=handler,
            priority=priority,
            status=status,
            session_id=session_id
        )

        if appointment:
            leads.appointment = parse(appointment)
            data['test_drive_time'] = leads.appointment

        print(leads)

        leads.save_to_db()

        body = ''
        messages = Message.query.filter(Message.session_id == session_id).order_by(desc(Message.id)).all()

        # message_list = []
        for message in messages:
            content = json.loads(message.message)
            if message.direction == 'incoming':
                content = content['data']['text']
                body += '[{}] {}\t {}\n'.format(utc_to_local(message.created_time).strftime("%Y-%m-%d %I:%M %p"),
                                                message.message_owner, content)
            else:
                for d in content:
                    if 'text' in d:
                        body += '[{}] {}\t {}\n'.format(
                            utc_to_local(message.created_time).strftime("%Y-%m-%d %I:%M %p"),
                            message.message_owner, d['text']['text'][0])
                    elif 'quickReplies' in d:
                        body += '[{}] {}\t {}\n'.format(
                            utc_to_local(message.created_time).strftime("%Y-%m-%d %I:%M %p"),
                            message.message_owner, d['quickReplies']['title'])
                    else:
                        body += '[{}] {}\t {}\n'.format(
                            utc_to_local(message.created_time).strftime("%Y-%m-%d %I:%M %p"),
                            message.message_owner, 'multimedia message')

        new_body = create_appt_email_body(data, body)
        if department == 'sales':
            send_email(sales_recipients, 'Message details - Downtown honda of Chicago', body=body)
        else:
            send_email(serive_recipients, 'Message details - Downtown honda of Chicago', body=body)

        send_email(['sales@downtownchicagohonda.edealerhub.com'],
                   'Honda of Downtown Chicago', body=new_body, bcc=['raffayhussain@blissmotors.com', 'hzhou@blissmotors.com'])

    except Exception as e:
        print(e)
