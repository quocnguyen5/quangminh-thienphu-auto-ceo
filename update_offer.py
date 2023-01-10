from model import LinkLead
from peewee import SqliteDatabase

db = SqliteDatabase("my_database.db")

url_filename = "offer.txt"
with open(url_filename) as file:
    lines = file.readlines()
    urls = [line.rstrip().split(",") for line in lines]
db.connect()
LinkLead.update(_delete=True).execute()
for data in urls:
    id, network, url, package, country, device = data
    print(id, network, url, package, country, device)
    offer_item = LinkLead.get_or_none(LinkLead.offer_id == id, LinkLead.network == network)
    if offer_item:
        LinkLead.update(url=url, network=network, package=package, country=country, device=device, _delete=False).where(
            LinkLead.id == offer_item.id).execute()
    else:
        LinkLead.create(offer_id=id, network=network, url=url, package=package,
                        country=country, device=device, _delete=False)
db.close()
