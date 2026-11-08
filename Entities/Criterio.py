class Criterio:
    def __init__(self, codigo, nombre, peso):
        self.__codigo = codigo
        self.nombre = nombre
        self.peso = peso

    @property
    def codigo(self):
        return self.__codigo

    @property
    def nombre(self):
        return self.__nombre
    @nombre.setter
    def nombre(self, nuevo_nombre):
        if nuevo_nombre.strip() == "":
            raise ValueError("El nombre no puede estar vacío.")
        self.__nombre = nuevo_nombre.strip() #strip elimina los espacios

    @property
    def peso(self):
        return self.__peso
    @peso.setter
    def peso(self, nuevo_peso):
        if type(nuevo_peso) != int or nuevo_peso <= 0:
            raise ValueError("El peso debe ser un número entero positivo.")
        self.__peso = nuevo_peso

