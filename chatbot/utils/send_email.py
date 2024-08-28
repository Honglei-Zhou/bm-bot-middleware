from flask_mail import Mail, Message
from server.server import app
from flask import render_template

mail = Mail(app)


def send_email(recipients, subject, body=None, html=None, bcc=None):
    with app.app_context():
        msg = Message(subject=subject,
                      sender=("No-Reply Telle", "noreply@telle.ai"),
                      recipients=recipients,
                      bcc=bcc,
                      body=body,
                      html=html)

        # msg.body = body
        # msg.html = render_template('/templates/notification.html',
        #                            lead_number=len(leads),
        #                            leads=leads,
        #                            messages=messages,
        #                            TITLE="New Lead Notification",
        #                            APP_NAME="Telle AI", APP_URL="https://www.telle.ai",
        #                            url="https://www.telle.ai")
        # print(msg.html)
        mail.send(msg)
