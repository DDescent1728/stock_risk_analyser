import mysql.connector
from mysql.connector import Error

# ===========================
# MySQL Database Configuration
# ===========================
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'YOURDBPWD', 
    'database': 'stock_db' 
}

# ===========================
# Database Connection
# ===========================
def connect_db():
    """
    Establish and return a MySQL database connection and cursor.
    """
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        if connection.is_connected():
            cursor = connection.cursor()
            return connection, cursor
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None, None

# ===========================
# CRUD Functions for Stock Prices
# ===========================
def insert_price(symbol, date, price):
    """
    Insert a new stock price into the database.
    Variables:
        symbol: Stock symbol (string)
        date: Date of closing price (YYYY-MM-DD)
        price: Closing price (float)
    """
    connection, cursor = connect_db()
    if not connection:
        return

    try:
        query = "INSERT INTO stock_prices (stock_symbol, date, close_price) VALUES (%s, %s, %s)"
        cursor.execute(query, (symbol, date, price))
        connection.commit()
    except Error as e:
        print(f"Error inserting price: {e}")
    finally:
        cursor.close()
        connection.close()

def get_price_history(symbol):
    """
    Fetch historical prices for a given stock symbol.
    Returns a list of tuples: [(date, price), ...]
    """
    connection, cursor = connect_db()
    if not connection:
        return []

    try:
        query = "SELECT date, close_price FROM stock_prices WHERE stock_symbol=%s ORDER BY date"
        cursor.execute(query, (symbol,))
        rows = cursor.fetchall()
        return rows
    except Error as e:
        print(f"Error fetching history: {e}")
        return []
    finally:
        cursor.close()
        connection.close()

def delete_stock(symbol):
    """
    Delete all records for a given stock symbol.
    """
    connection, cursor = connect_db()
    if not connection:
        return

    try:
        query = "DELETE FROM stock_prices WHERE stock_symbol=%s"
        cursor.execute(query, (symbol,))
        connection.commit()
    except Error as e:
        print(f"Error deleting stock: {e}")
    finally:
        cursor.close()
        connection.close()

# ===========================
# Simulation Results Storage
# ===========================
def insert_simulation_result(symbol, simulation_results):
    """
    Store GBM simulation results in the database.
    Variables:
        symbol: Stock symbol (string)
        simulation_results: List of lists
            Each sublist = one simulation path of prices [S1, S2, ..., SN]
    """
    connection, cursor = connect_db()
    if not connection:
        return

    try:
        # Table: simulation_results(symbol, path_number, day, price)
        for path_number, path in enumerate(simulation_results, start=1):
            for day, price in enumerate(path, start=1):
                query = "INSERT INTO simulation_results (stock_symbol, path_number, day, price) VALUES (%s, %s, %s, %s)"
                cursor.execute(query, (symbol, path_number, day, price))
        connection.commit()
    except Error as e:
        print(f"Error inserting simulation results: {e}")
    finally:
        cursor.close()
        connection.close()
