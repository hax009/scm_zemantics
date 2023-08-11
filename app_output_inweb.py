from flask import Flask, render_template, Response
import mysql.connector
import pandas as pd

app = Flask(__name__)

# MySQL database configuration, use your own db info
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "password",
    "database": "mydb"
}

@app.route('/')
def index():
    # Connect to the database and fetch data
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    query = "SELECT * FROM Shipment"
    cursor.execute(query)
    data = cursor.fetchall()
    cursor.close()
    connection.close()

    # Pass the data to the template
    return render_template('index.html', data=data)


@app.route('/download_csv')
def download_csv():
    # Connect to the database and fetch data
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    query = "SELECT * FROM Shipment"
    cursor.execute(query)
    data = cursor.fetchall()
    cursor.close()
    connection.close()

    # Create a pandas DataFrame from the data
    df = pd.DataFrame(data, columns=['sku','quantity', 'shippingtime','carrier','shippingcost','location','inspection','transportmode','route'])  
    # Convert DataFrame to CSV format
    csv_data = df.to_csv(index=False)

    # Prepare a Flask response with the CSV data
    response = Response(
        csv_data,
        content_type='text/csv',
        headers={"Content-Disposition": "attachment; filename=data.csv"}
    )

    return response

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=8000)


