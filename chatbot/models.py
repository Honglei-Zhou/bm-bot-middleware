import sqlalchemy_jsonfield
import ujson
import datetime
from database.db_instance import db


class Message(db.Model):

    __tablename__ = 'cars_dthonda_message'

    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(80), nullable=True)
    session_id = db.Column(db.String(120), nullable=False)
    direction = db.Column(db.String(20), nullable=False)
    message = db.Column(
        sqlalchemy_jsonfield.JSONField(
            # MariaDB does not support JSON for now
            enforce_string=True,
            # MariaDB connector requires additional parameters for correct UTF-8
            enforce_unicode=False,
            json=ujson
        ),
        nullable=True
    )

    dialogflow_resp = db.Column(
        sqlalchemy_jsonfield.JSONField(
            # MariaDB does not support JSON for now
            enforce_string=True,
            # MariaDB connector requires additional parameters for correct UTF-8
            enforce_unicode=False,
            json=ujson
        ),
        nullable=True
    )
    is_read = db.Column(db.Integer)
    from_bot = db.Column(db.Integer)
    message_owner = db.Column(db.String(80), nullable=True)

    created_time = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return '<Message %r>' % self.id


class Chat(db.Model):
    __tablename__ = 'cars_dthonda_chat'

    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(80), nullable=True)

    device_type = db.Column(db.String(80))
    device_detail = db.Column(db.String(80))

    session_id = db.Column(db.String(120), nullable=False)

    started = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    duration = db.Column(db.Text)

    lead = db.Column(db.Integer)

    handler = db.Column(db.String(50))

    dealer_id = db.Column(db.String(100))
    dealer_name = db.Column(db.Text)

    department = db.Column(db.String(50))

    alive = db.Column(db.Integer)

    missed = db.Column(db.String(10))

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()


class Lead(db.Model):
    __tablename__ = 'cars_dthonda_lead'

    id = db.Column(db.Integer, primary_key=True)

    dealer_id = db.Column(db.String(100))
    customer_name = db.Column(db.String(80), nullable=True)

    created = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    session_id = db.Column(db.String(120))

    email = db.Column(db.String(50))
    phone = db.Column(db.String(50))

    notes_offer = db.Column(db.Text)

    appointment = db.Column(db.DateTime)

    department = db.Column(db.String(50))

    handler = db.Column(db.String(50))

    priority = db.Column(db.Integer)

    status = db.Column(db.String(20))

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_session(cls, session_id, status):
        return cls.query.filter_by(session_id=session_id).filter_by(status=status).first()

    def __repr__(self):
        return '<Lead %r>' % self.id


class Group(db.Model):
    __tablename__ = 'cars_dthonda_group'

    id = db.Column(db.Integer, primary_key=True)

    session_id = db.Column(db.String(120), nullable=False)

    alive = db.Column(db.Integer, default=0)

    created = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    dealer_id = db.Column(db.String(100))
    dealer_name = db.Column(db.Text)

    department = db.Column(db.String(50))

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return '<Group %r>' % self.session_id


class WebUserModel(db.Model):

    __tablename__ = 'cars_dthonda_webuser'

    id = db.Column(db.Integer, primary_key=True)

    session_id = db.Column(db.String(120), nullable=False)

    ip_addr = db.Column(db.String(100))
    city = db.Column(db.String(50))
    state = db.Column(db.String(50))

    device_type = db.Column(db.String(80))
    device_detail = db.Column(db.String(80))

    created = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    dealer_id = db.Column(db.String(100))
    dealer_name = db.Column(db.Text)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()


class Car(db.Model):
    __tablename__ = 'inventory'

    # id = db.Column(db.Integer, primary_key=True)

    dealer_id = db.Column(db.String(100))
    dealer_name = db.Column(db.Text)

    vin = db.Column(db.String(50), primary_key=True)
    stock = db.Column(db.String(50))

    new_used = db.Column(db.String(10))
    year = db.Column(db.Integer)

    make = db.Column(db.String(100))
    model = db.Column(db.String(100))
    model_number = db.Column(db.String(100))

    body = db.Column(db.Text)
    transmission = db.Column(db.Text)

    series = db.Column(db.String(50))

    body_door_ct = db.Column(db.Integer)
    odometer = db.Column(db.Integer)
    engine_cylinder_ct = db.Column(db.Integer)
    engine_displacement = db.Column(db.Float)
    drivetrain_desc = db.Column(db.String(20))
    colour = db.Column(db.Text)
    interior_color = db.Column(db.Text)
    msrp = db.Column(db.Float)
    price = db.Column(db.Float)
    inventory_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    certified = db.Column(db.String(10))
    description = db.Column(db.Text)

    features = db.Column(db.Text)

    photo_url_list = db.Column(db.Text)
    city_mpg = db.Column(db.Float)
    highway_mpg = db.Column(db.Float)

    photos_last_modified_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    series_detail = db.Column(db.Text)

    engine = db.Column(db.Text)

    fuel = db.Column(db.String(100))

    age = db.Column(db.Integer)

    def __repr__(self):
        return '<Car %r>' % self.vin
