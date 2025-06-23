
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

class Usuario:
    def __init__(self, nombre, tono_piel, tipo_piel):
        self.nombre = nombre
        self.tono_piel = tono_piel
        self.tipo_piel = tipo_piel
    def __str__(self):
        return f"nombre:{self.nombre} - marca: {self.tono_piel} - categoria:{self.tipo_piel}"

class Review:
    def __init__(self, usuario_id, producto_id, puntuacion, comentario):
        self.usuario_id = usuario_id
        self.producto_id = producto_id
        self.puntuacion = puntuacion
        self.comentario = comentario
    def __str__(self):
        return f"Usuario {self.usuario_id} puntuó el producto {self.producto_id} con {self.puntuacion}⭐ - '{self.comentario}'"


