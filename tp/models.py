from peewee import *
from playhouse.sqlite_ext import SqliteExtDatabase
import datetime

db = SqliteExtDatabase('my_database.db')

class BaseModel(Model):
    class Meta:
        database = db

class User(BaseModel):
    email    = CharField()
    password = CharField()
    mobile   = CharField()

class Code(BaseModel):
    string = CharField()
    user   = ForeignKeyField(User, related_name='codes')

class Token(BaseModel):
    string    = CharField()
    createdAt = DateTimeField(default=datetime.datetime.now)
    user      = ForeignKeyField(User, related_name='tokens')
       
class Transaction(BaseModel):
    user        = ForeignKeyField(User, related_name='transactions')   
    amount      = FloatField()
    description = TextField()

# create table
User.create_table(True)
Code.create_table(True)
Token.create_table(True)
Transaction.create_table(True)

# connect db
db.connect()