import sqlite3

def get_db_connection():
    connection = sqlite3.connect("canteen.db")
    connection.row_factory = sqlite3.Row
    return connection

def create_tables():
    connection = get_db_connection()
    cursor = connection.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            audio_path TEXT NOT NULL,
            status TEXT DEFAULT 'pending'
        )
    """)
    
    connection.commit()
    connection.close()

def add_order(audio_path):
    connection = get_db_connection()
    cursor = connection.cursor()
    
    cursor.execute(
        "INSERT INTO orders (audio_path) VALUES (?)",
        (audio_path,)
    )
    
    connection.commit()
    order_id = cursor.lastrowid
    connection.close()
    return order_id

def get_pending_orders():
    connection = get_db_connection()
    cursor = connection.cursor()
    
    cursor.execute(
        "SELECT * FROM orders WHERE status = 'pending' ORDER BY id ASC"
    )
    orders = cursor.fetchall()
    
    connection.close()
    return orders

def update_order_status(order_id, new_status):
    connection = get_db_connection()
    cursor = connection.cursor()
    
    cursor.execute(
        "UPDATE orders SET status = ? WHERE id = ?",
        (new_status, order_id)
    )
    
    connection.commit()
    connection.close()

if __name__ == "__main__":
    create_tables()
    print("Database and tables initialized successfully!")