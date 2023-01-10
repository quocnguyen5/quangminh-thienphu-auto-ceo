from playhouse.sqlite_ext import *
import datetime


db = SqliteDatabase("my_database.db")


class BaseModel(Model):
    class Meta:
        database = db


class LinkLead(BaseModel):
    offer_id = CharField(unique=True)
    network = CharField()
    url = CharField()
    is_lead = BooleanField(default=False)
    package = CharField()
    device = CharField()
    country = CharField()
    _delete = CharField(default=False)


class LinkLeadData(BaseModel):
    link = ForeignKeyField(LinkLead, backref="link")
    data = JSONField()
    is_lead = BooleanField(default=False)
    created_date = DateTimeField(default=datetime.datetime.now)


class Account(BaseModel):
    email = CharField(unique=True)
    date_full = DateField(default=lambda: (datetime.date.today() - datetime.timedelta(1)))
