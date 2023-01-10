from peewee import SqliteDatabase
from model import Account

db = SqliteDatabase("my_database.db")


with open(f"account/total.txt") as f:
    accounts = f.read().splitlines()

for account in accounts:
    print(account)
    Account.get_or_create(email=account)
