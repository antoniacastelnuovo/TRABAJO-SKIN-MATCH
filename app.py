from flask import Flask, request, jsonify
from controllers import detectar_piel, recomendar_productos, buscar_producto_online
from database import crear_tabla
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
    conn = sqlite3.connect("productos.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM productos")
    columnas = [desc[0] for desc in cursor.description]
    datos = [dict(zip(columnas, fila)) for fila in cursor.fetchall()]
    conn.close()
    return jsonify(datos)

@app.route("/api/productos", methods=["POST"])
def agregar_producto():
    data = request.json
    campos = ["id", "nombre", "marca", "categoria", "tono", "precio", "stock", "vencimiento", "tipo_piel"]
    if not all(c in data for c in campos):
        return jsonify({"error": "Faltan campos obligatorios"}), 400

    conn = sqlite3.connect("productos.db")
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO productos (id, nombre, marca, categoria, tono, precio, stock, vencimiento, tipo_piel)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        data["id"], data["nombre"], data["marca"], data["categoria"],
        data["tono"], data["precio"], data["stock"], data["vencimiento"], data["tipo_piel"]
    ))
    conn.commit()
    conn.close()
    return jsonify({"msg": "Producto agregado correctamente"}), 201

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