import from  Entities.CasoUso import CasoUso

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
    
    def evaluar_individual(self, codigo_opcion, codigo_caso):
        """Ejecuta la evaluación individual de una opción para un caso."""
        # 1. Buscamos los objetos correspondientes usando sus códigos únicos

        opcion = self.buscar_opcion(codigo_opcion)
        caso = self.buscar_caso(codigo_caso)

        # 2. Verificamos que no exista previamente una evaluación para esta misma combinación
        duplicada = False
        posicion = 0
        while posicion < len(self.__evaluaciones) and not duplicada:
            evaluacion = self.__evaluaciones[posicion]
            # Comparamos si la opción y el caso de la evaluación existente coinciden
            duplicada = (evaluacion.opcion.codigo == codigo_opcion and evaluacion.caso.codigo == codigo_caso)
            posicion += 1

        # 3. Si ya existe, lanzamos el error personalizado de negocio para frenar la ejecución
        if duplicada:
            raise ErrorLaboratorio("Ya existe una evaluación para esa opción y ese caso.")
        
        # 4. Si pasa la validación, llamamos al método privado para crearla
        return self.__crear_evaluacion(opcion, caso)


    def __crear_evaluacion(self, opcion, caso):
        """Calcula puntajes, costos, determina el estado y crea la evaluación."""
        suma_ponderada = 0
        suma_pesos = 0
        posicion = 0

        # Recorremos todos los criterios registrados para calcular el puntaje ponderado
        while posicion < len(self.__criterios):
            criterio = self.__criterios[posicion]
            # Multiplicamos la nota dada por la opción en ese criterio por el peso del criterio
            
            suma_ponderada += opcion.puntajes[criterio.codigo] * criterio.peso
            suma_pesos += criterio.peso
            posicion += 1

        # Calculamos el puntaje total (evitando división por cero)  
        puntaje = suma_ponderada / suma_pesos if suma_pesos > 0 else 0
        
        # Obtenemos el costo estimado mensual utilizando el método polimórfico de la opción
        costo = opcion.costo_estimado()

        # Determinación de estado siguiendo el orden estricto de las reglas del obligatorio:
        estado = None
        if costo > caso.presupuesto:
            estado = Evaluacion.FUERA_PRESUPUESTO   # 1. Supera el presupuesto
        elif puntaje < caso.puntaje_minimo:
            estado = Evaluacion.PUNTAJE_INSUFICIENTE    # 2. No alcanza el puntaje mínimo
        else:
            estado = Evaluacion.RECOMENDADA    # 3. Cumple ambas condiciones con éxito

        # Creamos la instancia de la evaluación con la fecha y hora actual (datetime.now())  
        evaluacion = Evaluacion(
            self.__proximo_codigo_evaluacion, 
            datetime.now(), 
            opcion, 
            caso, 
            puntaje, 
            costo, 
            estado
        )

        # Guardamos la evaluación en la lista general del sistema y aumentamos el código consecutivo
        self.__evaluaciones.append(evaluacion)
        self.__proximo_codigo_evaluacion += 1
        
        return evaluacion