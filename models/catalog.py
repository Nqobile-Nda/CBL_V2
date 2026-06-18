import sqlite3

def database_connection():
    conn = sqlite3.connect("CBL.db")
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    return conn, cur


def create_catalog_table():
    conn, cur = database_connection()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS catalog (
    item_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    image TEXT NOT NULL,
    price TEXT NOT NULL,
    description TEXT NOT NULL,
    created_at TEXT NOT NULL,
    last_edited_at TEXT NOT NULL
    );
    """)

    conn.close()

    return print("Catalog table has been created")


def add_catalog_item(name, image, category, price, description, time_created, time_edited):
    conn, cur = database_connection()
    cur.execute("""
    INSERT INTO catalog (name, image, category, price, description, created_at, last_edited_at)
    VALUES (?,?,?,?,?,?,?)
    """, (name, image, category, price, description, time_created, time_edited))
    conn.commit()
    conn.close()

    return


def load_catalog():
    conn, cur = database_connection()
    cur.execute("SELECT * FROM catalog")
    catalog = [dict(row) for row in cur.fetchall()]

    conn.close()
    return catalog