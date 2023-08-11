from datetime import datetime
from flask import Flask, request, render_template
import csv
import os
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password@localhost:3306/mydb'
db = SQLAlchemy(app)
DB_last_update = datetime.now()

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
    global DB_last_update
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
        headers = next(csv_reader)
        columns = dict()
        for header, i in zip(headers, range(len(headers))):
            columns[header.lower()] = i

        for row in csv_reader:
            # skip old records
            if "timestamp" in columns and \
                datetime.strptime(row[columns["timestamp"]], '%Y-%m-%d %H:%M:%S') < DB_last_update:
                print("old record detected, skipping")
                continue
            new_record = Shipment(
                sku = row[columns["sku"]],
                quantity = row[columns["number of products sold"]],
                shippingtime = row[columns["shipping times"]],
                carrier = row[columns["shipping carriers"]],
                shippingcost = row[columns["shipping costs"]],
                location = row[columns["location"]],
                inspection = row[columns["inspection results"]],
                transportmode = row[columns["transportation modes"]],
                route = row[columns["routes"]]
            )
            db.session.add(new_record)
        db.session.commit()
        DB_last_update = datetime.now()

    os.remove("temp.csv")
    return 'CSV data inserted into database'

