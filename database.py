import sqlite3

def setup(filename="car_wash.sqlite"):  # create tables
    with sqlite3.connect(filename) as conn:
        cur = conn.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS customers(customer_name TEXT PRIMARY KEY, customer_id INTEGER, phone_number TEXT, address TEXT, email TEXT)")
        conn.commit()
        cur.execute("CREATE TABLE IF NOT EXISTS orders(order_id INTEGER PRIMARY KEY AUTOINCREMENT, customer_name TEXT, license_number TEXT, date TEXT, wash_type TEXT, car_type TEXT, car_model TEXT, FOREIGN KEY(customer_name) REFERENCES customers(customer_name))")
        conn.commit()


def query_db(sql, filename="car_wash.sqlite"):  # sql queries and return
    with sqlite3.connect(filename) as conn:
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit
        return cur.fetchall()

def get_dict(sql="SELECT * FROM orders"):       # הופכים את הדאטה בייס מרשימה למילון וככה ניתן למיין בקלות יתרה
    orders = query_db(sql)
    keys = ["order_id", "customer_name", "license_number", "date", "wash_type", "car_type", "car_model"]
    dicts_list = []
    for order in orders:
        values = list(order)
        dict_order = dict(zip(keys, values))
        dicts_list.append(dict_order)
    return dicts_list

    
def get_join_dict(sql="SELECT * FROM orders JOIN customers on orders.customer_name = customers.customer_name"):
    orders = list(query_db(sql))  # Convert the generator to a list
    keys = ["order_id", "customer_name", "license_number", "date", "wash_type", "car_type", "car_model", "customer_name", "customer_id", "phone_number", "address", "email"]
    dicts_list = []
    for order in orders:
        values = list(order)
        dict_order = dict(zip(keys, values))
        # dict_order["price"] = int(dict_order["price"])
        dicts_list.append(dict_order)
    return dicts_list

    
setup()
get_dict()