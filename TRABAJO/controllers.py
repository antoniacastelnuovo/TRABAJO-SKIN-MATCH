
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

