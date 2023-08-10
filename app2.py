from datetime import datetime
from flask import Flask, request, render_template
import csv
from io import TextIOWrapper
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password@localhost:3306/mydb'
db = SQLAlchemy(app)

class Record(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    products = db.Column(db.String(255))
    quantity = db.Column(db.Integer)
    quality = db.Column(db.String(255))
    money = db.Column(db.Float)
    time = db.Column(db.DateTime)
    plan = db.Column(db.String(255))

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
        # remove header
        next(csv_reader)

        for row in csv_reader:
            new_record = Record(products = row[0],
                    quantity = int(row[1]),
                    quality = row[2],
                    money = float(row[3]),
                    time = datetime.strptime(row[4], '%Y-%m-%d %H:%M:%S'),  # Assuming the date format
                    plan = row[5])
            db.session.add(new_record)
        db.session.commit()
    return 'CSV data inserted into database'