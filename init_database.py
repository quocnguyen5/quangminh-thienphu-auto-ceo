from model import LinkLead, LinkLeadData, Account
from peewee import SqliteDatabase
import os

if os.path.exists("my_database.db"):
    os.remove("my_database.db")

db = SqliteDatabase("my_database.db")
db.connect()
db.create_tables([LinkLead, LinkLeadData, Account])
db.close()
