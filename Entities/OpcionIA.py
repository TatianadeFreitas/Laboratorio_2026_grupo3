#Tiene que ser abstracta
class OpcionIA:
    def __init__(self, codigo, nombre, puntaje):
        self.codigo = codigo
        self.nombre = nombre
        self.puntaje = # es un diccionario?

    #metodo
    def costo_estimado(self):



class ServicioAPI(OpcionIA):
    def __init__(self, codigo, nombre, puntajes, costo_por_1000, consultas_estimadas):
        super().__init__(codigo, nombre, puntajes)
        self.costo_por_1000 = costo_por_1000          # USD por cada 1000 consultas
        self.consultas_estimadas = consultas_estimadas