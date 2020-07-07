import datetime
from sqlalchemy import Table, Column, ForeignKey, Integer, String, DateTime, PrimaryKeyConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

Data_Base = declarative_base()
class Signature(Data_Base):
    __tablename__ = 'signatures'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    signature = Column(String(64))

class Mistake(Data_Base):
    __tablename__ = 'mistakes'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    contents = Column(String(1024))
    discord_guild_id = Column(Integer)
    discord_channel_id = Column(Integer)
    discord_message_id = Column(Integer)


class User(Data_Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    discord_user_id = Column(Integer)
    signatures = relationship(Signature)
    mistakes = relationship(Mistake)

