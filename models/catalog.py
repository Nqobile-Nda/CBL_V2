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
    category TEXT NOT NULL,
    price TEXT NOT NULL,
    description TEXT NOT NULL,
    created_at TEXT NOT NULL,
    last_edited_at TEXT NOT NULL
    );
    """)

    conn.close()

    return print("Catalog table has been created")


def load_catalog():
    conn, cur = database_connection()
    cur.execute("SELECT * FROM catalog")
    catalog = [dict(row) for row in cur.fetchall()]

    conn.close()
    return catalog


def add_catalog_item(name, image, category, price, description, time_created, time_edited):
    conn, cur = database_connection()
    cur.execute("""
    INSERT INTO catalog (name, image, category, price, description, created_at, last_edited_at)
    VALUES (?,?,?,?,?,?,?)
    """, (name, image, category, price, description, time_created, time_edited))
    conn.commit()
    conn.close()

    return


def load_catalog_item(item_id):
    conn, cur = database_connection()
    cur.execute("SELECT * FROM catalog WHERE item_id = ?", (item_id,))
    item = cur.fetchone()
    conn.close()
    return dict(item) if item else None


def update_catalog_item(item_id, name, image, category, price, description, time_edited):
    conn, cur = database_connection()
    if image:
        cur.execute("""
        UPDATE catalog SET name=?, image=?, category=?, price=?, description=?, last_edited_at=?
        WHERE item_id=?
        """, (name, image, category, price, description, time_edited, item_id))
    else:
        cur.execute("""
        UPDATE catalog SET name=?, category=?, price=?, description=?, last_edited_at=?
        WHERE item_id=?
        """, (name, category, price, description, time_edited, item_id))
    conn.commit()
    conn.close()
    return