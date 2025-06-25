import sqlite3
import pandas as pd
import random
import requests


def detectar_piel(imagen):
    tipos = ["seca", "grasa", "mixta", "normal"]
    return random.choice(tipos)


def recomendar_productos(tipo_piel):
    conn = sqlite3.connect("productos.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM productos WHERE tipo_piel = ?", (tipo_piel,))
    columnas = [desc[0] for desc in cursor.description]
    productos = [dict(zip(columnas, fila)) for fila in cursor.fetchall()]
    conn.close()
    return productos

def buscar_producto_online(nombre):
    return {"tienda": "MakeUp Store", "link": f"https://tienda.com/{nombre.replace(' ', '_')}"}


def obtener_clima(ciudad):
    api_key = "761dd47e8f5f08f722c5b4ea7b97eb09"
    url = f"https://api.openweathermap.org/data/2.5/weather?q={ciudad}&appid={api_key}&units=metric&lang=es"
    response = requests.get(url)
    data = response.json()
    if response.status_code != 200:
        return {"error": "Ciudad no encontrada"}

    return {
        "ciudad": ciudad,
        "temperatura": data["main"]["temp"],
        "descripcion": data["weather"][0]["description"],
        "humedad": data["main"]["humidity"]
    }

def recomendaciones_por_clima(ciudad):
    clima = obtener_clima(ciudad)
    if "error" in clima:
        return [clima["error"]]
    if clima["temperatura"] > 30:
        return ["Base matte resistente al sudor", "Spray fijador"]
    elif clima["humedad"] > 70:
        return ["Polvo matificante", "Primer oil-free"]
    else:
        return ["Hidratante ligera", "Base líquida natural"]