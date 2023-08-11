from datetime import datetime
from flask import Flask, request, render_template
import csv
import os
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password@localhost:3306/mydb'
db = SQLAlchemy(app)

class Shipment(db.Model):
    sku = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer)
    shippingtime = db.Column(db.Integer)
    carrier = db.Column(db.String(45))
    shippingcost = db.Column(db.Float)
    location = db.Column(db.String(255))
    inspection = db.Column(db.String(255))
    transportmode = db.Column(db.String(255))
    route = db.Column(db.String(255))

    def __repr__(self):
        return f'<User {self.username}>'

@app.route('/upload', methods=['GET', 'POST'])
def upload_csv():
    if request.method == 'GET':
        return render_template('upload.html')  # Create an HTML form for file upload

    if 'csv_file' not in request.files:
        return 'No file part'
    file = request.files['csv_file']

    if file.filename == '':
        return 'No selected file'

    file.save("temp.csv")
    with open("temp.csv") as csvfile:
        csv_reader = csv.reader(csvfile)
        # map header to row
        sku = quantity = shipping_time = carrier = \
            shipping_cost = location = inspection = transport_mode = route = -1
        headers = next(csv_reader)
        for header, i in zip(headers, range(len(headers))):
            if header.lower() == "sku":
                sku = i
            elif header.lower() == "number of products sold":
                quantity = i
            elif header.lower() == "shipping times":
                shipping_time = i
            elif header.lower() == "shipping carriers":
                carrier = i
            elif header.lower() == "shipping costs":
                shipping_cost = i
            elif header.lower() == "location":
                location = i
            elif header.lower() == "inspection results":
                inspection = i
            elif header.lower() == "transportation modes":
                transport_mode = i
            elif header.lower() == "routes":
                route = i

        for row in csv_reader:
            new_record = Shipment(
                sku = row[sku],
                quantity = row[quantity],
                shippingtime = row[shipping_time],
                carrier = row[carrier],
                shippingcost = row[shipping_cost],
                location = row[location],
                inspection = row[inspection],
                transportmode = row[transport_mode],
                route = row[route]
            )
            db.session.add(new_record)
        db.session.commit()

    os.remove("temp.csv")
    return 'CSV data inserted into database'

