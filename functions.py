import sqlite3

def load(filename = "car_wash.sqlite"):
    with sqlite3.connect(filename) as conn:
        cur = conn.cursor()
        return cur.fetchall()

def add_customer(customer_name, customer_id, phone_number, address, email, filename ="car_wash.sqlite"):
    with sqlite3.connect(filename) as conn:
        cur = conn.cursor()
        sql_query = ("INSERT INTO customers (customer_name, customer_id, phone_number, address, email) VALUES (?, ?, ?, ?, ?)")
        contact_data = (customer_name, customer_id, phone_number, address, email)
        cur.execute(sql_query, contact_data)
        conn.commit()
        return "Customer added"

def find_customer(customer_name, filename="car_wash.sqlite"):
        with sqlite3.connect(filename) as conn:
            cur = conn.cursor()
            sql_query = ("SELECT * FROM orders WHERE customer_name = ?")
            cur.execute(sql_query, customer_name)
            customer_data = cur.fetchone()
            if customer_data:
                customer_name, customer_id, phone_number, address, email = customer_data  
                return f"Customer found:Name={customer_name}, ID={customer_id}, Phone={phone_number}, address={address}, email={email}  "
            else:
                return "Customer did not found"
 
def insert_order(order_id, customer_name, license_number, date, wash_type, car_type, car_model, filename="car_wash.sqlite"):
    with sqlite3.connect(filename) as conn:
        cur = conn.cursor()
        sql_query = '''
            INSERT INTO orders ("order_id", "customer_name", "license_number", "date", "wash_type", "car_type", "car_model")
            VALUES (?, ?, ?, ?, ?, ?, ?)
        '''
        order_data = (order_id, customer_name, license_number, date, wash_type, car_type, car_model)
        cur.execute(sql_query, order_data)
        conn.commit()
        return "Order added"
    
    
def delete_customer(customer_id, filename="car_wash.sqlite"):
    with sqlite3.connect(filename) as conn:
        cur = conn.cursor()
        sql_query = ("DELETE FROM customers WHERE customer_id = ?")
        cur.execute(sql_query, (customer_id,))
        conn.commit()
        return "Customer deleted"
    
def update_customer(customer_id, customer_name, phone_number, address, email, filename="car_wash.sqlite"):
    with sqlite3.connect(filename) as conn:
        cur = conn.cursor()
        sql_query = '''
            UPDATE customers
            SET customer_name=?, phone_number=?, address=?, email=?
            WHERE customer_id=?
        '''
        customer_data = (customer_name, phone_number, address, email, customer_id)
        cur.execute(sql_query, customer_data)
        conn.commit()
        return "Customer updated"

def find_order_by_license_number(license_number, filename="car_wash.sqlite"):
    with sqlite3.connect(filename) as conn:
        cur = conn.cursor()
        sql_query = ("SELECT * FROM orders WHERE license_number = ?")
        cur.execute(sql_query, (license_number,))
        order_data = cur.fetchall()
        if order_data:
            return order_data
        else:
            return "Order not found"
import sqlite3

def sum_orders_by_month(customer_name, year, month, filename="car_wash.sqlite"):
    with sqlite3.connect(filename) as conn:
        cur = conn.cursor()
        start_date = f"{month:02d}/{year}/{1:02d}"
        if month == 12:
            end_date = f"{1:02d}/{year+1}/{1:02d}"
        else:
            end_date = f"{month+1:02d}/{year}/{1:02d}"
        sql_query = '''
            SELECT SUM(price) AS total_amount
            FROM orders
            WHERE customer_name=? AND date >= ? AND date < ?
        '''
        cur.execute(sql_query, (customer_name, start_date, end_date))
        total_amount = cur.fetchone()[0]
        return total_amount
