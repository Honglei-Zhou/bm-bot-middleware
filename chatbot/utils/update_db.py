import os
from ..models import Group, Chat, Lead, WebUserModel, Message, Car
from datetime import datetime, timezone
from sqlalchemy import desc
from sqlalchemy import and_
from .send_email import send_email
import ipinfo
from server.config import ipinfo_access_token
import pytz
import json
from .create_email_body import create_email_body

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


def update_group(sid, alive):

    group = Group.query.filter(Group.session_id == sid).first()

    if group is None:

        new_group = Group()
        new_group.session_id = sid

        new_group.alive = alive

        new_group.created = datetime.utcnow()

        new_group.save_to_db()

    else:
        group.alive = alive
        group.save_to_db()


def update_chat(sid, close=True):

    chat = Chat.query.filter(and_(Chat.session_id == sid, Chat.alive == 1)).order_by(desc(Chat.id)).first()

    if chat is None and not close:

        new_chat = Chat()
        new_chat.session_id = sid

        new_chat.alive = 1

        new_chat.started = datetime.utcnow()

        new_chat.dealer_name = 'dthonda'
        new_chat.department = 'sales'
        # new_chat.lead = 2
        new_chat.handler = 'BM Bot'
        new_chat.device_type = 'Desktop'
        new_chat.customer_name = 'Customer'
        new_chat.missed = 'answered'

        duration = datetime.utcnow() - new_chat.started
        new_chat.duration = str(duration)

        new_chat.save_to_db()

    elif chat is not None and close:
        print(chat)
        chat.alive = 0
        duration = datetime.utcnow() - chat.started
        chat.duration = str(duration)
        chat.save_to_db()


def update_leads(message):
    dealer_id = message.get('dealerId', 'dthonda')
    customer_name = message.get('customer', 'customer')
    email = message.get('email', '')
    phone = message.get('phone', '')
    notes_offer = message.get('note', 'Submitted from SMS text.')
    appointment = message.get('appointment', None)

    session_id = message.get('sessionId', '')

    department = message.get('department', 'sales')
    handler = message.get('handleBy', 'not available')

    priority = message.get('importance', 1)

    status = message.get('status', 'New')

    leads = Lead(
        dealer_id=dealer_id,
        customer_name=customer_name,
        created=datetime.utcnow(),
        email=email,
        phone=phone,
        notes_offer=notes_offer,
        department=department,
        handler=handler,
        priority=priority,
        status=status,
        session_id=session_id
    )

    if appointment:
        leads.appointment = appointment

    print(leads)

    leads.save_to_db()

    if leads.phone == '8008008000':
        body = 'Customer: {}\nEmail: {}\n\n'.format(leads.customer_name, leads.email)
    elif leads.email == 'default@telle.ai':
        body = 'Customer: {}\nPhone: {}\n\n'.format(leads.customer_name, leads.phone)
    else:
        body = 'Customer: {}\nEmail: {}\nPhone: {}\n\n'.format(leads.customer_name, leads.email, leads.phone)

    messages = Message.query.filter(Message.session_id == session_id).order_by(desc(Message.id)).all()

    message_body = ''

    for message in messages:
        content = json.loads(message.message)
        if message.direction == 'incoming':
            content = content['data']['text']
            message_body += '[{}] {}\t {}\n'.format(utc_to_local(message.created_time).strftime("%Y-%m-%d %I:%M %p"), message.message_owner, content)

        else:
            for d in content:
                if 'text' in d:
                    message_body += '[{}] {}\t {}\n'.format(utc_to_local(message.created_time).strftime("%Y-%m-%d %I:%M %p"),
                                                  message.message_owner, d['text']['text'][0])
                elif 'quickReplies' in d:
                    message_body += '[{}] {}\t {}\n'.format(utc_to_local(message.created_time).strftime("%Y-%m-%d %I:%M %p"),
                                                  message.message_owner, d['quickReplies']['title'])
                else:
                    message_body += '[{}] {}\t {}\n'.format(utc_to_local(message.created_time).strftime("%Y-%m-%d %I:%M %p"),
                                                  message.message_owner, 'multimedia message')

    body += message_body

    if department == 'sales':
        send_email(sales_recipients, 'Message details - Downtown honda of Chicago', body=body)
    else:
        send_email(serive_recipients, 'Message details - Downtown honda of Chicago', body=body)

    # recipient email should be available to set dynamically !
    # send_email(['hzhou@blissmotors.com',
    #             'raffayhussain@blissmotors.com'],
    #             'New Leads Created',
    #             'Name: {}'
    #             'Email: {}'
    #             'Phone: {}'
    #             'note: {}'
    #             'Created: {}'.format(
    #                             leads.customer_name,
    #                             leads.email,
    #                             leads.phone,
    #                             leads.notes_offer,
    #                             utc_to_local(leads.created)))

    if leads.phone == '8008008000':
        new_body = create_email_body(session_id, leads.customer_name, leads.email, '', message_body)
    elif leads.email == 'default@telle.ai':
        new_body = create_email_body(session_id, leads.customer_name, '', leads.phone, message_body)
    else:
        new_body = create_email_body(session_id, leads.customer_name, leads.email, leads.phone, message_body)
    # print(new_body)
    send_email(['sales@downtownchicagohonda.edealerhub.com'],
               'Honda of Downtown Chicago', body=new_body, bcc=['raffayhussain@blissmotors.com'])


def create_lead_from_intent(message):
    dealer_id = message.get('dealerId', 'dthonda')
    customer_name = message.get('customer', 'customer')
    email = message.get('email', '')
    phone = message.get('phone', '')
    notes_offer = message.get('note', '')
    appointment = message.get('appointment', None)

    session_id = message.get('sessionId', '')

    department = message.get('department', 'sales')
    handler = message.get('handleBy', 'not available')

    priority = message.get('importance', 1)

    status = message.get('status', 'Invalid')

    new_leads = Lead(
        dealer_id=dealer_id,
        customer_name=customer_name,
        created=datetime.utcnow(),
        email=email,
        phone=phone,
        notes_offer=notes_offer,
        department=department,
        handler=handler,
        priority=priority,
        status=status,
        session_id=session_id
    )

    if appointment:
        new_leads.appointment = appointment

    print(new_leads)

    new_leads.save_to_db()


def update_lead_from_intent(message):
    email = message.get('email')
    phone = message.get('phone')

    session_id = message.get('sessionId', '')
    dealer_id = message.get('dealerId', '201978945124789')
    department = message.get('department', 'sales')
    customer = message.get('customer', 'new customer')

    if session_id != '':

        leads = Lead.find_by_session(session_id, 'Invalid')
        if leads is not None:
            if email is not None:
                leads.email = email
            if phone is not None:
                leads.phone = phone
            if customer != 'new customer':
                leads.customer_name = customer

            leads.status = 'New'

            leads.save_to_db()
        else:

            leads = Lead(
                dealer_id=dealer_id,
                customer_name=customer,
                created=datetime.utcnow(),
                email=email,
                phone=phone,
                notes_offer='',
                department=department,
                handler='',
                priority=1,
                status='New',
                session_id=session_id
            )

            leads.save_to_db()

        if leads.phone == '8008008000':
            body = 'Customer: {}\nEmail: {}\n\n'.format(leads.customer_name, leads.email)
        elif leads.email == 'default@telle.ai':
            body = 'Customer: {}\nPhone: {}\n\n'.format(leads.customer_name, leads.phone)
        else:
            body = 'Customer: {}\nEmail: {}\nPhone: {}\n\n'.format(leads.customer_name, leads.email, leads.phone)

        messages = Message.query.filter(Message.session_id == session_id).order_by(desc(Message.id)).all()

        message_body = ''
        # message_list = []
        for message in messages:
            content = json.loads(message.message)
            if message.direction == 'incoming':
                content = content['data']['text']
                message_body += '[{}] {}\t {}\n'.format(utc_to_local(message.created_time).strftime("%Y-%m-%d %I:%M %p"),
                                              message.message_owner, content)
            else:
                for d in content:
                    if 'text' in d:
                        message_body += '[{}] {}\t {}\n'.format(utc_to_local(message.created_time).strftime("%Y-%m-%d %I:%M %p"),
                                                      message.message_owner, d['text']['text'][0])
                    elif 'quickReplies' in d:
                        message_body += '[{}] {}\t {}\n'.format(utc_to_local(message.created_time).strftime("%Y-%m-%d %I:%M %p"),
                                                      message.message_owner, d['quickReplies']['title'])
                    else:
                        message_body += '[{}] {}\t {}\n'.format(utc_to_local(message.created_time).strftime("%Y-%m-%d %I:%M %p"),
                                                      message.message_owner, 'multimedia message')

        body += message_body
        if department == 'sales':
            send_email(sales_recipients, 'Message details - Downtown honda of Chicago', body=body)
        else:
            send_email(serive_recipients, 'Message details - Downtown honda of Chicago', body=body)


        if leads.phone == '8008008000':
            new_body = create_email_body(session_id, leads.customer_name, leads.email, '', message_body)
        elif leads.email == 'default@telle.ai':
            new_body = create_email_body(session_id, leads.customer_name, '', leads.phone, message_body)
        else:
            new_body = create_email_body(session_id, leads.customer_name, leads.email, leads.phone, message_body)
        # print(new_body)
        send_email(['sales@downtownchicagohonda.edealerhub.com'],
                   'Honda of Downtown Chicago', body=new_body, bcc=['raffayhussain@blissmotors.com'])


def update_user(message, sid):
    device_type = message.get('deviceType', 'Desktop')
    device_detail = message.get('deviceDetail', 'Desktop')
    session_id = message.get('sessionId', sid)

    dealer_id = message.get('dealerId', 'dthonda')
    dealer_name = message.get('dealerName', 'dthonda')

    ip_addr = message.get('ip_addr', '127.0.0.1')

    ip_details = get_ip_address(ip_addr)
    city = ip_details.get('city', 'NA')
    state = ip_details.get('region', 'NA')

    new_user = WebUserModel(dealer_id=dealer_id,
                            dealer_name=dealer_name,
                            device_detail=device_detail,
                            device_type=device_type,
                            created=datetime.utcnow(),
                            ip_addr=ip_addr,
                            city=city,
                            state=state,
                            session_id=session_id)

    new_user.save_to_db()


def get_ip_address(ip):
    handler = ipinfo.getHandler(ipinfo_access_token)
    details = handler.getDetails(ip)
    return details.all


def inquiry_leads(message):
    try:
        dealer_id = message.get('dealerId', 'dthonda')
        title = message.get('title', '')
        price = message.get('price', '')
        customer_name = message.get('customer', 'customer')
        email = message.get('email', '')
        phone = message.get('phone', '')
        notes_offer = message.get('note', '')
        appointment = message.get('appointment', None)

        vin = message.get('vin', '')
        stock = message.get('stock', '')

        notes_offer = '{} Inquiry: {} vin# {} stock# {}'.format(notes_offer, title, vin, stock)

        session_id = message.get('sessionId', '')

        department = message.get('department', '')
        handler = message.get('handleBy', 'not available')

        priority = message.get('importance', 1)

        status = message.get('status', 'New')

        leads = Lead(
            dealer_id=dealer_id,
            customer_name=customer_name,
            created=datetime.utcnow(),
            email=email,
            phone=phone,
            notes_offer=notes_offer,
            department=department,
            handler=handler,
            priority=priority,
            status=status,
            session_id=session_id
        )

        if appointment:
            leads.appointment = appointment

        print(leads)

        leads.save_to_db()

        body = 'Dear {}\nThank you for choosing Honda of Downtown Chicago. Your price is ${}. Attached is your personalized {} Savings Certificate.\n' \
               'This document contains valuable information that will help guide your car buying decision, while helping you save time and money.'.format(customer_name, price, title)

        send_email([email],
                   title, body=body, bcc=sales_recipients)

        if leads.phone == '':
            new_body = create_email_body(session_id, leads.customer_name, leads.email, '', body)
        elif leads.email == '':
            new_body = create_email_body(session_id, leads.customer_name, '', leads.phone, body)
        else:
            new_body = create_email_body(session_id, leads.customer_name, leads.email, leads.phone, body)
        # print(new_body)
        send_email(['sales@downtownchicagohonda.edealerhub.com'],
                   'Honda of Downtown Chicago', body=new_body, bcc=['raffayhussain@blissmotors.com'])

    except Exception as e:
        print(e)

