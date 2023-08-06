from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)
DATABASE = "car_wash.sqlite"

def get_db_connection():
    return sqlite3.connect(DATABASE)


@app.route("/show_customers")
def index():
    try:
        with get_db_connection() as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM customers")
            customers = cur.fetchall()
        return render_template("index.html", customers=customers)
    except Exception as e:
        return f"An error occurred: {str(e)}"


@app.route("/add_customer", methods=["POST", "GET"])
def add_customer():
    if request.method == "POST":
        try:
            customer_name = request.form.get("customer_name")
            customer_id = request.form.get("customer_id")
            phone_number = request.form.get("phone_number")
            address = request.form.get("address")
            email = request.form.get("email")
            with get_db_connection() as conn:
                cur = conn.cursor()
                cur.execute("INSERT INTO customers (customer_name, customer_id, phone_number, address, email) VALUES (?, ?, ?, ?, ?)",
                            (customer_name, customer_id, phone_number, address, email))
                conn.commit()
            return render_template("add_customer.html")
        except Exception as e:
            return f"An error occurred: {str(e)}"
    else:
        return render_template("add_customer.html")
    

@app.route("/search", methods=["GET", "POST"])
def search():
    if request.method == "POST":
        try:
            customer_name = request.form.get("customer_name")
            with get_db_connection() as conn:
                cur = conn.cursor()
                cur.execute("SELECT * FROM customers WHERE customer_name = ?", (customer_name,))
                customer_data = cur.fetchone()
            if customer_data:
                customer_name, customer_id, phone_number, address, email = customer_data
                return render_template("search.html", customer_found=True, customer_data=customer_data)
            else:
                return render_template("search.html", customer_found=False)
        except Exception as e:
            return f"An error occurred: {str(e)}"
    else:
        return render_template("search.html", customer_found=None, customer_data=None)
    

@app.route("/", methods=["GET", "POST"])
def add_order():
    if request.method == "POST":
        try:
            order_id = None
            customer_name = request.form.get("customer_name")
            license_number = request.form.get("license_number")
            date = request.form.get("date")
            wash_type = request.form.get("wash_type")
            car_type = request.form.get("car_type")
            car_model = request.form.get("car_model")
            with get_db_connection() as conn:
                cur = conn.cursor()
                cur.execute('''INSERT INTO orders (order_id, customer_name, license_number, date, wash_type, car_type, car_model)
                            VALUES (?, ?, ?, ?, ?, ?, ?)''', (order_id, customer_name, license_number, date, wash_type, car_type, car_model))
                conn.commit()
            return render_template("add_order.html")
        except Exception as e:
            return f"An error occurred: {str(e)}"
    else:
        with get_db_connection() as conn:
            cur = conn.cursor()
            cur.execute("SELECT customer_name FROM customers")
            customers = cur.fetchall()
            car_types = ["פרטי", "ג'יפ", "מסחרי", "מיניבוס", "אוטובוס", "משאית"]
            wash_types = ["פנימי וחיצוני", "חיצוני", "פנימי", "מיוחדת"]  
        return render_template("add_order.html", customers=customers, car_types=car_types, wash_types=wash_types)


if __name__ == "__main__":
    app.run(debug=True)
