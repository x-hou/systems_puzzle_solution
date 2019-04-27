import datetime
import os

from flask import Flask, render_template, redirect, url_for
from forms import ItemForm
from models import Items
from database import db_session, init_db
init_db()
app = Flask(__name__)
app.secret_key = os.environ['APP_SECRET_KEY']
# app.secret_key = 'super_duper_secret'

@app.route("/", methods=('GET', 'POST'))
def add_item():
    form = ItemForm()
    if form.validate_on_submit():
        item = Items(name=form.name.data, quantity=form.quantity.data, description=form.description.data, date_added=datetime.datetime.now())
        db_session.add(item)
        db_session.commit()
        return redirect("http://localhost:8080/success")
    return render_template('index.html', form=form)

@app.route("/success")
def success():
    results = []
    qry = db_session.query(Items)
    for item in qry.all():
        results.append([item.id, item.name, item.quantity, item.description, item.date_added])

    return str(results)

@app.teardown_request
def shutdown_session(exception=None):
    db_session.remove()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
