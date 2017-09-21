# -*- coding: utf-8 -*-
import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine


Base = declarative_base()
secret_key = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in xrange(32))

# the necessary user class
class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(32), index=True)
    picture = Column(String)
    email = Column(String)
    password_hash = Column(String(64))

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def generate_auth_token(self, expiration=600):
        s = Serializer(secret_key, expires_in = expiration)
        return s.dumps({'id': self.id })

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(secret_key)
        try:
            data = s.loads(token)
        except SignatureExpired:
            #Valid Token, but expired
            return None
        except BadSignature:
            #Invalid Token
            return None
        user_id = data['id']
        return user_id


# the food classes
class FoodClass(Base):
    __tablename__ = 'foodclass'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    creator_id = Column(Integer, ForeignKey('user.id'))
    creator = relationship(User)



class FoodItem(Base):
    __tablename__ = 'fooditem'

    name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    description = Column(String(250))
    price = Column(String(8))
    typical_size = Column(String(20))
    need_to_shop = Column(Integer)
    foodclass_id = Column(Integer, ForeignKey('foodclass.id'))
    foodclass = relationship(FoodClass)
    creator_id = Column(Integer, ForeignKey('user.id'))
    creator = relationship(User)

    @property
    def serialize(self):
        #Returns object Data in easily serializable format
        return {
            'name': self.name,
            'description': self.description,
            'id': self.id,
            'price': self.price,
            'typical_size': self.typical_size,
            'need_to_shop': self.need_to_shop,
        }


### create the db ###
engine = create_engine('sqlite:///foodlist.db')

Base.metadata.create_all(engine)
