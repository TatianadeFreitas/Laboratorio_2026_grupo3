from abc import ABC, abstractmethod

class OpcionIA(ABC):
    def __init__(self, codigo, nombre, puntajes):
        self._codigo = codigo
        self.nombre = nombre
        self.puntajes = puntajes  # es un diccionario 

    @property
    def codigo(self):
        return self._codigo

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        if type(valor) != str:  # Comprobamos que el valor sea una cadena de texto
            raise ValueError("El nombre debe ser un texto.")  # Si no es un texto, lanzamos un error con un mensaje 

        if valor.strip() == "":  # Comprueba que el valor no esté vacío después de eliminar los espacios en blanco al inicio y al final
            raise ValueError("El nombre no puede estar vacío.")

        self._nombre = valor.strip()

    @property
    def puntajes(self):
        return self.__puntajes

    @puntajes.setter
    def puntajes(self, nuevos_puntajes):
        if type(nuevos_puntajes) != dict:
            raise ValueError("Los puntajes deben ser un diccionario.")
        
        for codigo_criterio, puntaje in nuevos_puntajes.items(): #codigo_criterio = clave, puntaje = valor
            if type(puntaje) != int or not (0 <= puntaje <= 10):
                raise ValueError(f"El puntaje para el criterio {codigo_criterio} debe ser un número entero entre 0 y 10.")
        
        self.__puntajes = nuevos_puntajes

    @abstractmethod
    def costo_estimado(self):
        pass # se usa ya que el metodo no tiene cuerpo asi no da error
        #tipo de dato float     

class ServicioAPI(OpcionIA):
    def __init__(self, codigo, nombre, puntajes, costo_por_1000, consultas_estimadas):
        super().__init__(codigo, nombre, puntajes)
        self.costo_por_1000 = costo_por_1000
        self.consultas_estimadas = consultas_estimadas

    @property
    def costo_por_1000(self):
        return self.__costo_por_1000

    @costo_por_1000.setter
    def costo_por_1000(self, valor):
        if type(valor) not in (int, float):
            raise ValueError("El costo por 1000 consultas debe ser un número.")
        if valor < 0:
            raise ValueError("El costo por 1000 consultas no puede ser negativo.")
        self.__costo_por_1000 = float(valor)

    @property
    def consultas_estimadas(self):
        return self.__consultas_estimadas

    @consultas_estimadas.setter
    def consultas_estimadas(self, valor):
        if type(valor) != int:
            raise ValueError("Las consultas estimadas deben ser un número entero.")
        if valor <= 0:
            raise ValueError("Las consultas estimadas deben ser un número entero positivo.")
        self.__consultas_estimadas = valor

    def costo_estimado(self):
        #se le define el cuerpo al metodo heredado
        return (self.consultas_estimadas / 1000) * self.costo_por_1000


class PlanMensual(OpcionIA):
    def __init__(self, codigo, nombre, puntajes, cantidad_usuarios, costo_por_usuario):
        super().__init__(codigo, nombre, puntajes) #se usa super para acceder a los métodos de la clase padre: OpcionIA
        self.cantidad_usuarios = cantidad_usuarios
        self.costo_por_usuario = costo_por_usuario

    @property
    def cantidad_usuarios(self):
        return self.__cantidad_usuarios

    @cantidad_usuarios.setter
    def cantidad_usuarios(self, valor):
        if type(valor) != int:
            raise ValueError("La cantidad de usuarios debe ser un número entero.")
        if valor <= 0:
            raise ValueError("La cantidad de usuarios debe ser un número entero positivo.")
        self.__cantidad_usuarios = valor

    @property
    def costo_por_usuario(self):
        return self.__costo_por_usuario

    @costo_por_usuario.setter
    def costo_por_usuario(self, valor):
        if type(valor) not in (int, float):
            raise ValueError("El costo por usuario debe ser un número.")
        if valor < 0:
            raise ValueError("El costo por usuario no puede ser negativo.")
        self.__costo_por_usuario = float(valor)

    def costo_estimado(self):
        #se le define el cuerpo al metodo heredado
        return self.cantidad_usuarios * self.costo_por_usuario

