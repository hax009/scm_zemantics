from flask import Flask, request, render_template
import csv
from io import TextIOWrapper
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password@localhost:3306/mydb'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

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
            new_user = User(username=row[0], email=row[1])
            db.session.add(new_user)
        db.session.commit()
    return 'CSV data inserted into database'

