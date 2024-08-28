import datetime
from flask import render_template


def create_email_body(session_id, name, email, phone, message):
    # print('******************************')
    timestamp = datetime.datetime.now()
    body = '''
        <?xml version="1.0" encoding="UTF-8"?>
        <?ADF VERSION="1.0"?>
            <adf>
              <prospect>
                <requestdate>{}</requestdate>
                <customer>
                    <contact>
                    <name part="full">{}</name>
                    <email>{}</email>
                    <phone type="mobile">{}</phone>
                    </contact>
                    <comments>{}</comments>
                </customer>

                <provider>
                        <name part="full">Telle AI</name>
                        <service>Chatbot Service</service>
                        <url>https://telle.ai</url>
                        <email>telle@telle.ai</email>
                        <contact primarycontact="1">
                        <name part="full">Telle AI</name>
                        <email>telle@telle.ai</email>
                        <address>
                        <street line="1">160 E Grand Ave</street>
                        <city>Chicago</city>
                        <regioncode>IL</regioncode>
                        <postalcode>60611</postalcode>
                        <country>US</country>
                        </address>
                        </contact>
                    </provider>
             </prospect>
            </adf>
    '''.format(timestamp, name, email, phone, message)
    # print(body)
    return body
