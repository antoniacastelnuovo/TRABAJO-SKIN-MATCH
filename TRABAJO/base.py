
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




