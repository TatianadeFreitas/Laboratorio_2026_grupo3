class CasoUso:
    
    def __init__(self, codigo, nombre, presupuesto, puntaje_minimo):
        self.__codigo = codigo
        self.nombre = nombre
        self.presupuesto = presupuesto
        self.puntaje_minimo = puntaje_minimo

    @property
    def codigo(self):
        return self.__codigo

    @property
    def nombre(self):
        return self.__nombre

    @nombre.setter
    def nombre(self, valor):
        if not isinstance(valor, str): #Comprobamos que el valor sea una cadena de texto
            raise ValueError("El nombre debe ser un texto.") #Si no es un texdto, lanzamos un error con un mensaje 

        if valor.strip() == "": #Comprueba que el valor no esté vacío después de eliminar los espacios en blanco al inicio y al final
            raise ValueError("El nombre no puede estar vacío.")

        self.__nombre = valor

    @property
    def presupuesto(self):
        return self.__presupuesto

    @presupuesto.setter
    def presupuesto(self, valor):
        if valor < 0:
            raise ValueError("El presupuesto debe ser mayor o igual a cero.")

        self.__presupuesto = valor

    @property
    def puntaje_minimo(self):
        return self.__puntaje_minimo

    @puntaje_minimo.setter
    def puntaje_minimo(self, valor):
        if not (valor >= 0 and valor <= 10):
            raise ValueError("El puntaje mínimo debe estar entre 0 y 10.")

        self.__puntaje_minimo = valor

    def __str__(self):
        return (f"Código: {self.__codigo} - "
                f"Nombre: {self.__nombre} - "
                f"Presupuesto: {self.__presupuesto} USD - "
                f"Puntaje mínimo: {self.__puntaje_minimo}")