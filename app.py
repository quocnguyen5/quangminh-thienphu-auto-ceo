from peewee import SqliteDatabase
from model import LinkLead, LinkLeadData
from flask import Flask, render_template, redirect

app = Flask(__name__)


@app.route("/")
def table():
    linklead = LinkLead.select().where(LinkLead._delete == False).dicts()
    return render_template("main_table.html", datas=linklead)


@app.route("/true")
def table():
    linklead = LinkLead.select().where(LinkLead.is_lead == True, LinkLead._delete == False).dicts()
    return render_template("main_table.html", datas=linklead)


@app.route("/false")
def table_false():
    linklead = LinkLead.select().where(LinkLead.is_lead == False, LinkLead._delete == False).dicts()
    return render_template("main_table.html", datas=linklead)


@app.route("/details/<id>")
def table_details(id):
    linklead = LinkLead.get(LinkLead.offer_id == id)
    linklead_data = LinkLeadData.select().join(LinkLead).where(
        LinkLead.offer_id == id, LinkLeadData.is_lead == True).dicts()
    return render_template("detail_table.html", linklead=linklead, linklead_data=linklead_data)


@app.route("/details/<id>/false")
def table_details_false(id):
    linklead = LinkLead.get(LinkLead.offer_id == id)
    linklead_data = LinkLeadData.select().join(LinkLead).where(
        LinkLead.offer_id == id, LinkLeadData.is_lead == False).dicts()
    return render_template("detail_table.html", linklead=linklead, linklead_data=linklead_data)


@app.route("/offer-redirect")
def table_details_false():
    linklead_data = LinkLeadData.select().join(LinkLead).where(LinkLeadData.is_lead == True).dicts()
    return redirect()


if __name__ == "__main__":
    app.run(debug=True)
