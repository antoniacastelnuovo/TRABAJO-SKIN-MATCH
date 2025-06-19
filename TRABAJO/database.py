import sqlite3
def conectar():
    return sqlite3.connect("productos.db")

def crear_tabla():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS productos (
        id INTEGER PRIMARY KEY,
        nombre TEXT,
        marca TEXT,
        categoria TEXT,
        tono TEXT,
        precio REAL,
        vencimiento TEXT,
        tipo_piel TEXT
    )''')
    conn.commit()
    conn.close()