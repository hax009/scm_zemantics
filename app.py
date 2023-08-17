from datetime import datetime
from flask import Flask, request, render_template
import csv
import os
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

# 'mysql+pymysql://root:password@localhost:3306/yourdatabasename'
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "mysql+pymysql://root:O`,+CT{>E7KqgaQ[@localhost:3306/scm_project"
db = SQLAlchemy(app)
DB_last_update = datetime.now()


class Shipment(db.Model):
    Shipment_Id = db.Column(db.Integer, primary_key=True)
    Order_Id = db.Column(db.Integer)
    Transaction_type = db.Column(db.String(255))
    Days_for_shipping_real = db.Column(db.Integer)
    Days_for_shipment_scheduled = db.Column(db.Integer)
    Benefit_per_order = db.Column(db.Float)
    Sales_per_customer = db.Column(db.Float)
    Delivery_Status = db.Column(db.String(255))
    Late_delivery_risk = db.Column(db.Integer)
    Category_Id = db.Column(db.Integer)
    Category_Name = db.Column(db.String(255))
    Customer_City = db.Column(db.String(255))
    Customer_Country = db.Column(db.String(255))
    Customer_Email = db.Column(db.String(255))
    Customer_Fname = db.Column(db.String(255))
    Customer_Id = db.Column(db.Integer)
    Customer_Lname = db.Column(db.String(255))
    Customer_Password = db.Column(db.String(255))
    Customer_Segment = db.Column(db.String(255))
    Customer_State = db.Column(db.String(255))
    Customer_Street = db.Column(db.String(255))
    Customer_Zipcode = db.Column(db.String(45))
    Department_Id = db.Column(db.Integer)
    Department_Name = db.Column(db.String(255))
    Latitude = db.Column(db.Float)
    Longitude = db.Column(db.Float)
    Market = db.Column(db.String(255))
    Order_City = db.Column(db.String(255))
    Order_Country = db.Column(db.String(255))
    Order_Customer_Id = db.Column(db.Integer)
    Order_date = db.Column(db.DateTime)
    Order_Item_Cardprod_Id = db.Column(db.Integer)
    Order_Item_Discount = db.Column(db.Float)
    Order_Item_Discount_Rate = db.Column(db.Float)
    Order_Item_Id = db.Column(db.Integer)
    Order_Item_Product_Price = db.Column(db.Float)
    Order_Item_Profit_Ratio = db.Column(db.Float)
    Order_Item_Quantity = db.Column(db.Integer)
    Sales = db.Column(db.Float)
    Order_Item_Total = db.Column(db.Float)
    Order_Profit_Per_Order = db.Column(db.Float)
    Order_Region = db.Column(db.String(255))
    Order_State = db.Column(db.String(255))
    Order_Status = db.Column(db.String(255))
    Product_Card_Id = db.Column(db.Integer)
    Product_Category_Id = db.Column(db.Integer)
    Product_Description = db.Column(db.String(255))
    Product_Image = db.Column(db.String(255))
    Product_Name = db.Column(db.String(255))
    Product_Price = db.Column(db.Float)
    Product_Status = db.Column(db.Integer)
    Shipping_date = db.Column(db.DateTime)
    Shipping_Mode = db.Column(db.String(255))

    def __repr__(self):
        return f"<User {self.username}>"


@app.route("/upload", methods=["GET", "POST"])
def upload_csv():
    global DB_last_update
    if request.method == "GET":
        return render_template("upload.html")  # Create an HTML form for file upload

    if "csv_file" not in request.files:
        return "No file part"
    file = request.files["csv_file"]

    if file.filename == "":
        return "No selected file"

    file.save("temp.csv")
    with open("temp.csv") as csvfile:
        csv_reader = csv.reader(csvfile)
        # map header to row
        headers = next(csv_reader)
        columns = dict()
        for header, i in zip(headers, range(len(headers))):
            columns[header] = i

        for row in csv_reader:
            # skip old records
            if (
                "timestamp" in columns
                and datetime.strptime(row[columns["timestamp"]], "%Y-%m-%d %H:%M:%S")
                < DB_last_update
            ):
                print("old record detected, skipping")
                continue
            new_record = Shipment(
                Transaction_type=row[columns["Type"]],
                Days_for_shipping_real=row[columns["Days for shipping (real)"]],
                Days_for_shipment_scheduled=row[
                    columns["Days for shipment (scheduled)"]
                ],
                Benefit_per_order=row[columns["Benefit per order"]],
                Sales_per_customer=row[columns["Sales per customer"]],
                Delivery_Status=row[columns["Delivery Status"]],
                Late_delivery_risk=row[columns["Late_delivery_risk"]],
                Category_Id=row[columns["Category Id"]],
                Category_Name=row[columns["Category Name"]],
                Customer_City=row[columns["Customer City"]],
                Customer_Country=row[columns["Customer Country"]],
                Customer_Email=row[columns["Customer Email"]],
                Customer_Fname=row[columns["Customer Fname"]],
                Customer_Id=row[columns["Customer Id"]],
                Customer_Lname=row[columns["Customer Lname"]],
                Customer_Password=row[columns["Customer Password"]],
                Customer_Segment=row[columns["Customer Segment"]],
                Customer_State=row[columns["Customer State"]],
                Customer_Street=row[columns["Customer Street"]],
                Customer_Zipcode=row[columns["Customer Zipcode"]],
                Department_Id=row[columns["Department Id"]],
                Department_Name=row[columns["Department Name"]],
                Latitude=row[columns["Latitude"]],
                Longitude=row[columns["Longitude"]],
                Market=row[columns["Market"]],
                Order_City=row[columns["Order City"]],
                Order_Country=row[columns["Order Country"]],
                Order_Customer_Id=row[columns["Order Customer Id"]],
                Order_date=datetime.strptime(
                    row[columns["order date (DateOrders)"]], "%m/%d/%Y %H:%M"
                ),
                Order_Id=row[columns["Order Id"]],
                Order_Item_Cardprod_Id=row[columns["Order Item Cardprod Id"]],
                Order_Item_Discount=row[columns["Order Item Discount"]],
                Order_Item_Discount_Rate=row[columns["Order Item Discount Rate"]],
                Order_Item_Id=row[columns["Order Item Id"]],
                Order_Item_Product_Price=row[columns["Order Item Product Price"]],
                Order_Item_Profit_Ratio=row[columns["Order Item Profit Ratio"]],
                Order_Item_Quantity=row[columns["Order Item Quantity"]],
                Sales=row[columns["Sales"]],
                Order_Item_Total=row[columns["Order Item Total"]],
                Order_Profit_Per_Order=row[columns["Order Profit Per Order"]],
                Order_Region=row[columns["Order Region"]],
                Order_State=row[columns["Order State"]],
                Order_Status=row[columns["Order Status"]],
                Product_Card_Id=row[columns["Product Card Id"]],
                Product_Category_Id=row[columns["Product Category Id"]],
                Product_Description=row[columns["Product Description"]],
                Product_Image=row[columns["Product Image"]],
                Product_Name=row[columns["Product Name"]],
                Product_Price=row[columns["Product Price"]],
                Product_Status=row[columns["Product Status"]],
                Shipping_date=datetime.strptime(
                    row[columns["shipping date (DateOrders)"]], "%m/%d/%Y %H:%M"
                ),
                Shipping_Mode=row[columns["Shipping Mode"]],
            )

            db.session.add(new_record)
        db.session.commit()
        DB_last_update = datetime.now()

    os.remove("temp.csv")
    return "CSV data inserted into database"
