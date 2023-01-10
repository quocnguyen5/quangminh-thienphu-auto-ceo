import sys
import threading
import time
import urllib.parse
from datetime import datetime, date

import requests
import schedule
from peewee import SqliteDatabase, fn

from model import Account, LinkLead, LinkLeadData

# Use a service account
db = SqliteDatabase("my_database.db")


def login(username, password=None):
    try:
        password = password or username
        headers = {
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36",
            "cookie": "_ga=GA1.2.188149608.1641196554; _gid=GA1.2.1141616972.1641196554",
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        }
        data = f"email={username}&password={password}"
        r = requests.post("https://affilitest.com/user/login", headers=headers, data=data)

        if r.status_code == 200:
            set_cookie = r.headers["Set-Cookie"].split(";")
            for cookie in set_cookie:
                if "session" in cookie:
                    return cookie
        else:
            return None
    except:
        return None


def check_link(session, email, url, device="android", country="kr"):
    headers = {
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36",
        "cookie": f"_ga=GA1.2.188149608.1641196554; _gid=GA1.2.1141616972.1641196554; {session}",
    }

    data = f"inputType=urlInput&mainInput={urllib.parse.quote(url.encode('utf8'))}&device={device}&country={country}"
    r = requests.post("https://affilitest.com/test", headers=headers, data=data)
    if r.status_code == 200:
        return r.json()["data"]
    else:
        try:
            if "upgrade your account" in r.json()["error"]:
                Account.update(date_full=date.today()).where(Account.email == email).execute()
        except:
            pass

        return None


def check_lead(url, datas, package):
    whitelist = ["adjust", "appsflyer", "adbrix", "airbridge.io", "kochava", "singular", "app.link"]
    linklead_record = LinkLead.get(LinkLead.url == url)
    linkdada = LinkLeadData.create(link=linklead_record, data=datas)
    if package in datas[-1]:
        res1 = [item for item in whitelist if item in datas[-1]]
        res2 = [item for item in whitelist if item in datas[-2]]
        if bool(res1) or bool(res2):
            LinkLead.update(is_lead=True).where(LinkLead.url == url).execute()
            LinkLeadData.update(is_lead=True).where(LinkLeadData.id == linkdada.id).execute()
            print(f"----> True:", url, package, datetime.now())
        else:
            print("----> False", url, package)
    else:
        print("----> False", url, package)


def process(offer):
    db.connect()
    result = None
    while not result:
        account = (
            Account.select()
            .where(Account.date_full.day < datetime.now().day)
            .order_by(fn.Random())
            .limit(1)
        )
        if account.count() == 0:
            print("Full account.")
            sys.exit()

        email = account[0].email
        auth = login(email, email)
        if auth is None:
            continue
        result = check_link(auth, email, offer.url, offer.device, offer.country)

    check_lead(offer.url, result, offer.package)
    db.close()


def main():
    offers = LinkLead.select().where(LinkLead._delete == False)
    for offer in offers:
        threading.Thread(
            target=process,
            args=(offer,),
        ).start()


schedule.every(5).minutes.do(main)
while True:
    schedule.run_pending()
    time.sleep(5)
