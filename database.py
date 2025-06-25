import sqlite3
import pandas as pd

def conectar():
    return sqlite3.connect("productos.db")

def crear_tabla():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT,
            marca TEXT,
            categoria TEXT,
            tono TEXT,
            precio REAL,
            vencimiento TEXT,
            tipo_piel TEXT
        )
    ''')
    conn.commit()
    conn.close()

def cargar_datos_desde_excel(archivo_excel):
    df = pd.read_excel(archivo_excel)

    conn = conectar()
    cursor = conn.cursor()

    for index, row in df.iterrows():
        cursor.execute('''
            INSERT INTO productos (nombre, marca, categoria, tono, precio, vencimiento, tipo_piel)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            row['NOMBRE'],
            row['MARCA'],
            row['CATEGORIA'],
            row['TONO'],
            float(str(row['PRECIO']).replace("USD ", "").replace(",", ".")),
            row['VENCIMIENTO'],
            row.get('TIPO_PIEL', 'No definido')
        ))

    conn.commit()
    conn.close()

crear_tabla()
cargar_datos_desde_excel("base_maquillaje_completa (1).xlsx")
print("¡Base de datos creada y cargada exitosamente!")