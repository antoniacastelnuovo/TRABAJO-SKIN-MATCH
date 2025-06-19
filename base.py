class Producto:
    def __init__(self,id,nombre,marca,categoria,tono, precio,vencimiento,tipo_piel):
        self.id=id
        self.nombre=nombre
        self.marca=marca
        self.categoria=categoria
        self.tono=tono
        self.precio = precio
        self.vencimiento=vencimiento
        self.tipo_piel=tipo_piel
    def __str__(self):
        return f"nombre:{self.nombre} - marca: {self.marca} - categoria:{self.categoria} - tono: {self.tono} - precio: ${self.precio} - vencimiento: {self.vencimiento}"

import pandas as pd
import random

def detectar_piel(imagen):
    tipos = ["seca", "grasa", "mixta", "normal"]
    return random.choice(tipos)

def recomendar_productos(tipo_piel):
    df = pd.read_csv("productos.csv")
    recomendados = df[df["tipo_piel"] == tipo_piel]
    return recomendados.to_dict(orient="records")

def buscar_producto_online(nombre): #simulacion de una api de terceros (devuelve un link del local donde encontrar el producto)
    return {"tienda": "MakeUp Store", "link": f"https://tienda.com/{nombre.replace(' ', '_')}"}

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


from flask import Flask, request, jsonify
from controllers import detectar_piel, recomendar_productos, buscar_producto_online
from database import crear_tabla
import pandas as pd
import sqlite3

app = Flask(__name__)
crear_tabla()

@app.route("/api/detectar_piel", methods=["POST"])
def api_detectar_piel():
    imagen = request.files.get("imagen")
    tipo = detectar_piel(imagen)
    return jsonify({"tipo_piel": tipo})

@app.route("/api/recomendaciones", methods=["GET"])
def api_recomendar():
    tipo_piel = request.args.get("tipo_piel")
    productos = recomendar_productos(tipo_piel)
    return jsonify(productos)

@app.route("/api/productos", methods=["GET"])
def api_productos():
    df = pd.read_csv("productos.csv")
    return jsonify(df.to_dict(orient="records"))

@app.route("/api/productos", methods=["POST"])
def agregar_producto():
    data = request.json
    conn = sqlite3.connect("productos.db")
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO productos VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                   (data["id"], data["nombre"], data["marca"], data["categoria"],
                    data["tono"], data["precio"], data["stock"], data["vencimiento"],
                    data["tipo_piel"]))
    conn.commit()
    conn.close()
    return jsonify({"msg": "Producto agregado"}), 201

@app.route("/api/productos/<int:id>", methods=["DELETE"])
def eliminar_producto(id):
    conn = sqlite3.connect("productos.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM productos WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return jsonify({"msg": f"Producto {id} eliminado"})

@app.route("/api/buscar_online", methods=["GET"])
def buscar_online():
    nombre = request.args.get("nombre")
    resultado = buscar_producto_online(nombre)
    return jsonify(resultado)

if __name__ == "__main__":
    app.run(debug=True)


#csv


import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("productos.csv")
df["tipo_piel"].value_counts().plot(kind="bar", title="Productos por tipo de piel")
plt.xlabel("Tipo de piel")
plt.ylabel("Cantidad de productos")
plt.show()

