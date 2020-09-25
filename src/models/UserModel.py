# src/models/UserModel.py
from marshmallow import fields, Schema
import datetime
from . import db
from ..app import bcrypt
from .BlogpostModel import BlogpostSchema

class UserModel(db.Model):
    """
    User Model
    """
    
    # table name
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    apaterno = db.Column(db.String(128), nullable=False)
    amaterno = db.Column(db.String(128))
    rfc = db.Column(db.String(128))
    avatar = db.Column(db.Text)
    phone = db.Column(db.Numeric(14,0))
    moral = db.Column(db.Boolean)
    admin = db.Column(db.Boolean)
    tokenfg = db.Column(db.Text)
    street = db.Column(db.String(250))
    int_no = db.Column(db.String(10))
    ext_no = db.Column(db.String(10))
    suburb = db.Column(db.String(250))
    country = db.Column(db.String(250))
    state = db.Column(db.String(250))
    city = db.Column(db.String(250))
    cp = db.Column(db.Integer)
    email = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=True)
    created_at = db.Column(db.DateTime)
    modified_at = db.Column(db.DateTime)
    blogposts = db.relationship('BlogpostModel', backref='users', lazy=True)

  # class constructor
    def __init__(self, data):
        """
        Class constructor
        """
        self.name = data.get('name')
        self.apaterno = data.get('apaterno')
        self.amaterno = data.get('amaterno')
        self.rfc = data.get('rfc')
        self.avatar = data.get('avatar')
        self.phone = data.get('phone')
        self.moral = data.get('moral')
        self.admin = data.get('admin')
        self.tokenfg = data.get('tokenfg')
        self.street = data.get('street')
        self.int_no = data.get('int_no')
        self.ext_no = data.get('ext_no')
        self.suburb = data.get('suburb')
        self.country = data.get('country')
        self.state = data.get('state')
        self.city = data.get('city')
        self.cp = data.get('cp')
        self.email = data.get('email')
        self.password = self.__generate_hash(data.get('password'))
        self.created_at = datetime.datetime.utcnow()
        self.modified_at = datetime.datetime.utcnow()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, data):
        for key, item in data.items():
            if key == 'password': 
                self.password = self.__generate_hash(data.get('password'))
            setattr(self, key, item)
        self.modified_at = datetime.datetime.utcnow()
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __generate_hash(self, password):
        return bcrypt.generate_password_hash(password, rounds=10).decode("utf-8")
    
    def check_hash(self, password):
        return bcrypt.check_password_hash(self.password, password)

    @staticmethod
    def get_all_users():
        return UserModel.query.all()

    @staticmethod
    def get_one_user(id):
        return UserModel.query.get(id)
        
    @staticmethod
    def get_user_by_email(value):
        return UserModel.query.filter_by(email=value).first()

    def __repr(self):
        return '<id {}>'.format(self.id)

class UserSchema(Schema):
    """
    User Schema
    """
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    apaterno = fields.Str(required=True)
    amaterno = fields.Str()
    rfc = fields.Str()
    avatar = fields.Str()
    phone = fields.Number()
    moral = fields.Bool()
    admin = fields.Bool()
    tokenfg = fields.Str()
    street = fields.Str()
    int_no = fields.Str()
    ext_no = fields.Str()
    suburb = fields.Str()
    country = fields.Str()
    state = fields.Str()
    city = fields.Str()
    cp = fields.Int()
    email = fields.Email(required=True)
    password = fields.Str(required=True)
    created_at = fields.DateTime(dump_only=True)
    modified_at = fields.DateTime(dump_only=True)
    blogposts = fields.Nested(BlogpostSchema, many=True)