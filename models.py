import datetime
import json
from app import db
from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import JSON

class JsonEncodedDict(db.TypeDecorator):
    """Enables JSON storage by encoding and decoding on the fly."""
    impl = db.Text

    def process_bind_param(self, value, dialect):
        if value is None:
            return '{}'
        else:
            return json.dumps(value)

    def process_result_value(self, value, dialect):
        if value is None:
            return {}
        else:
            return json.loads(value)

class Result(db.Model):
    __tablename__ = 'results'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    url = db.Column(db.String())

    def __init__(self, url):
        self.url = url

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def to_json(self):
        return {
            'url': self.url,
        }

class Vendor(db.Model):
    __tablename__ = 'vendor'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String())
    image_path = db.Column(db.String())
    menu = db.Column(JsonEncodedDict)

    def __init__(self, menu, name, image_path):
        self.menu = menu
        self.name = name
        self.image_path = image_path

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def to_json(self):
        return {
            'name': self.name,
            'image_path': self.image_path,
            'menu': self.menu,
        }

class Order(db.Model):
    __tablename__ = 'order'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    vendor_id = db.Column(db.Integer, ForeignKey(Vendor.id), index=True)
    order = db.Column(JsonEncodedDict)
    created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __init__(self, vendor_id, order):
        self.vendor_id = vendor_id
        self.order = order

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def order_json(self):
        return {
            'order': self.order,
            'created_date': self.created_date,
        }

    def to_json(self):
        return {
            'id': self.id,
            'vendor_id': self.vendor_id,
            'order': self.order,
            'created_date': self.created_date,
        }
