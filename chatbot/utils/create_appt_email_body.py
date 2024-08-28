import datetime


def create_appt_email_body(data, body):
    timestamp = datetime.datetime.now()
    body = '''
            <?xml version="1.0" encoding="UTF-8"?>
            <?ADF VERSION="1.0"?>
                <adf>
                  <prospect>
                    <requestdate>{}</requestdate>
                    <vehicle>
                        <year>{}</year>
                        <make>{}</make>
                        <model>{}</model>
                        <trim>{}</trim>
                        <bodystyle>{}</bodystyle>
                        <colorcombination>
                            <interiorcolor>{}</interiorcolor>
                            <exteriorcolor>{}</exteriorcolor>
                            <preference>1</preference>
                        </colorcombination>
                        <price></price>
                        <comments>{}</comments>
                    </vehicle>
                    <customer>
                        <contact>
                        <name part="full">{}</name>
                        <email>{}</email>
                        <phone type="mobile">{}</phone>
                        </contact>
                        <timeframe>
                         <description>Test Drive Time: {}</description>
                        </timeframe>
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
        '''.format(timestamp, data.get('VehicleYear', 'any'), data.get('VehicleMake', 'any'),
                   data.get('VehicleModel', 'any'), data.get('VehicleDrivetrain', 'any'), data.get('VehicleType', 'any'),
                   data.get('VehicleInteriorColor', 'any'), data.get('VehicleColor', 'any'),
                   data.get('VehicleFeatures', 'any'), data.get('person', 'customer'),
                   data.get('email', 'NA'), data.get('phone-number', 'NA'), data.get('test_drive_time'), body)

    return body

