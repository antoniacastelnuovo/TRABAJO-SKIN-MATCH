from flask import Flask, request, jsonify
from controllers import detectar_piel, recomendar_productos, obtener_clima, recomendaciones_por_clima
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

@app.route("/api/clima", methods=["GET"]) #API TERCEROS
def api_clima():
    ciudad = request.args.get("ciudad")
    if not ciudad:
        return jsonify({"error": "Falta el parámetro 'ciudad'"}), 400
    clima = obtener_clima(ciudad)
    return jsonify(clima)

@app.route("/api/recomendaciones_clima", methods=["GET"])
def api_recomendar_por_clima(): #API TERCEROS
    ciudad = request.args.get("ciudad")
    if not ciudad:
        return jsonify({"error": "Falta parámetro 'ciudad'"}), 400
    sugerencias = recomendaciones_por_clima(ciudad)
    return jsonify({"recomendaciones": sugerencias})


if __name__ == "__main__":
    app.run(debug=True)