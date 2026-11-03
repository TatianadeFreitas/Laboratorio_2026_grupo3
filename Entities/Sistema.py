import from Entities.CasoUso import CasoUso

class Sistema:

    def __init__(self):
        self.__criterios = []
        self.__opciones = []
        self.__casos = []
        self.__evaluaciones = []

    def listar_criterios(self):

        if len(self.__criterios) == 0:
            print("No hay criterios registrados.")

        else:
            posicion = 0

            while posicion < len(self.__criterios):
                criterio = self.__criterios[posicion]
                print(criterio)
                posicion += 1
    
    def listar_opciones(self):

        posicion = 0

        while posicion < len(self.__opciones):
            opcion = self.__opciones[posicion]

            print(f"\n{opcion.codigo} - {opcion.nombre}")
            print(f" {opcion.descripcion_costo()}")
            print(f" Costo mensual: USD {opcion.costo_estimado():.2f}")

            criterio_pos = 0

            while criterio_pos < len(self.__criterios):
                criterio = self.__criterios[criterio_pos]

                print(f" {criterio.nombre}: {opcion.puntajes[criterio.codigo]}")

                criterio_pos += 1

            posicion += 1

        if len(self.__opciones) == 0:
            print("No hay opciones de IA registradas.")

    def listar_casos(self):
        posicion = 0

        while posicion < len(self.__casos):
            caso = self.__casos[posicion]

            cantidad = self.cantidad_recomendadas(caso.codigo)

            print(f"{caso} | Recomendadas: {cantidad}")

            posicion += 1

        if len(self.__casos) == 0:
            print("No hay casos de uso registrados.")

    def cantidad_recomendadas(self, codigo_caso):

        evaluaciones = self.evaluaciones_del_caso(codigo_caso)

        cantidad = 0
        posicion = 0

        while posicion < len(evaluaciones):

            if evaluaciones[posicion].estado == Evaluacion.RECOMENDADA:
                cantidad += 1

            posicion += 1

        return cantidad
    
    