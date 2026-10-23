from abc import ABC, abstractmethod

#FALTAN HACER LAS VALIDACIÓNES CORRESPONDIENTES

class OpcionIA(ABC):
    def __init__(self, codigo, nombre, puntajes):
        self.codigo = codigo
        self.nombre = nombre
        self.puntajes = puntajes #es un diccionario

    @abstractmethod
    def costo_estimado(self):
        pass # se usa ya que el metodo no tiene cuerpo asi no da error (preguntar si esta bien)
        #tipo de dato float     


class ServicioAPI(OpcionIA):
    def __init__(self, codigo, nombre, puntajes, costo_por_1000, consultas_estimadas):
        super().__init__(codigo, nombre, puntajes) #se usa super para acceder a los métodos de la clase padre: OpcionIA
        self.costo_por_1000 = float(costo_por_1000)
        self.consultas_estimadas = consultas_estimadas

    def costo_estimado(self):
        return (self.consultas_estimadas / 1000) * self.costo_por_1000

class PlanMensual(OpcionIA):
    def __init__(self, codigo, nombre, puntajes, cantidad_usuarios, costo_por_usuario):
        super().__init__(codigo, nombre, puntajes)
        self.cantidad_usuarios = cantidad_usuarios
        self.costo_por_usuario = float(costo_por_usuario)

    def costo_estimado(self):
        return self.cantidad_usuarios * self.costo_por_usuario