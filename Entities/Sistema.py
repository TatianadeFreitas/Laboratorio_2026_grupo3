from datetime import datetime

# Importamos las clases que vamos a utilizar.
# Primero intentamos importar los módulos desde el mismo paquete (Entities),
# utilizando el punto (.) para indicar que pertenecen a la misma carpeta
try:
    from .Criterio import Criterio
    from .CasoUso import CasoUso
    from .OpcionIA import OpcionIA, ServicioAPI, PlanMensual
    from .Evaluacion import Evaluacion
# Si ocurre un error en esos imports, intentamos importarlos sin el punto (busca el módulo sin especificar el paquete)
except ImportError:
    from Criterio import Criterio
    from CasoUso import CasoUso
    from OpcionIA import OpcionIA, ServicioAPI, PlanMensual
    from Evaluacion import Evaluacion
from Exceptions.ErrorLaboratorio import ErrorLaboratorio


class Sistema:

    def __init__(self):
        # Listas que almacenan los objetos registrados
        self.__criterios = []
        self.__opciones = []
        self.__casos = []
        self.__evaluaciones = []

        # Contadores para asignar códigos consecutivos
        self.__proximo_codigo_criterio = 1
        self.__proximo_codigo_opcion = 1
        self.__proximo_codigo_caso = 1
        self.__proximo_codigo_evaluacion = 1

    @property
    def criterios(self):
        return self.__criterios

    @property
    def opciones(self):
        return self.__opciones

    @property
    def casos(self):
        return self.__casos

    # Método para buscar un criterio
    def buscar_criterio(self, codigo):
        # Recorremos la lista de criterios.
        posicion = 0
        while posicion < len(self.__criterios):
            criterio = self.__criterios[posicion]

            # Si encontramos el código, devolvemos el criterio.
            if criterio.codigo == codigo:
                return criterio
            posicion += 1

         # Si terminamos el recorrido, el código no existe, por lo que lanzamos un error con un mensaje.
        raise ErrorLaboratorio("No existe un criterio con ese código.")

    # Método para buscar una opción
    def buscar_opcion(self, codigo):
        # Recorremos la lista de opciones.
        posicion = 0
        while posicion < len(self.__opciones):
            opcion = self.__opciones[posicion]
            if opcion.codigo == codigo:
                return opcion
            posicion += 1
        raise ErrorLaboratorio("No existe una opción con ese código.")

    # Método para buscar un caso
    def buscar_caso(self, codigo):
        # Recorremos la lista de casos.
        posicion = 0
        while posicion < len(self.__casos):
            caso = self.__casos[posicion]
            if caso.codigo == codigo:
                return caso
            posicion += 1
        raise ErrorLaboratorio("No existe un caso con ese código.")

   
    # REGISTRAR CRITERIO
    def registrar_criterio(self, nombre, peso):
        # Los criterios deben registrarse antes que las opciones
        if len(self.__opciones) > 0:
            raise ErrorLaboratorio("No se pueden registrar criterios después de registrar opciones.")
        # Controlamos que el nombre no esté repetido
        posicion = 0
        while posicion < len(self.__criterios):
            criterio = self.__criterios[posicion]
            if criterio.nombre.lower() == nombre.strip().lower(): #Verificamos que el nombre del criterio no este repetido pasando a minúsculas y quitando espacios, si lo esta lanzamos un error con un mensaje
                raise ErrorLaboratorio("Ya existe un criterio con ese nombre.")
            posicion += 1

        # Creamos el criterio con el próximo código disponible
        criterio = Criterio(self.__proximo_codigo_criterio, nombre, peso)
        # Guardamos el criterio en la lista.
        self.__criterios.append(criterio)
        # Aumentamos el contador para el próximo registro.
        self.__proximo_codigo_criterio += 1
        return criterio


    # REGISTRAR OPCIÓN DE IA
    def registrar_opcion( self, nombre, tipo, puntajes, costo_por_1000=None, consultas_estimadas=None, cantidad_usuarios=None, costo_por_usuario=None):

        # Para registrar opciones debe existir al menos un criterio.
        if len(self.__criterios) == 0:
            raise ErrorLaboratorio("Primero debe registrar al menos un criterio.")

        # Verificamos que no exista otra opción con el mismo nombre.
        posicion = 0
        while posicion < len(self.__opciones):
            opcion_existente = self.__opciones[posicion]
            if opcion_existente.nombre.lower() == nombre.strip().lower():
                raise ErrorLaboratorio("Esa opción ya está registrada.")
            posicion += 1

        # Comprobamos que los puntajes sean un diccionario con el isinstance que pregunta si un objeto es de cierta clase y devuelve True o False
        if not isinstance(puntajes, dict): # (objeto, Clase) 
            raise ErrorLaboratorio("Los puntajes deben ser un diccionario.")

        # Comprobamos que haya exactamente un puntaje por criterio.
        if len(puntajes) != len(self.__criterios):
            raise ErrorLaboratorio("Debe ingresar un puntaje por cada criterio.")

        # Verificamos que las claves sean los códigos de los criterios.
        for criterio in self.__criterios:
            if criterio.codigo not in puntajes:
                raise ErrorLaboratorio("Falta ingresar el puntaje de un criterio.")

        # Según el tipo, creamos una clase u otra.
        if tipo == 1:
            # Creamos una opción de tipo ServicioAPI.
            opcion = ServicioAPI(
                self.__proximo_codigo_opcion,
                nombre,
                puntajes,
                costo_por_1000,
                consultas_estimadas
            )

        elif tipo == 2:
            # Creamos una opción de tipo PlanMensual.
            opcion = PlanMensual(
                self.__proximo_codigo_opcion,
                nombre,
                puntajes,
                cantidad_usuarios,
                costo_por_usuario
            )
        else:
            raise ErrorLaboratorio("El tipo de opción no es válido.")

        # Guardamos la opción creada.
        self.__opciones.append(opcion)
        # Aumentamos el contador.
        self.__proximo_codigo_opcion += 1
        return opcion


    # REGISTRAR CASO DE USO
    def registrar_caso(self, nombre, presupuesto, puntaje_minimo):

        # Controlamos que no haya otro caso con el mismo nombre
        posicion = 0
        while posicion < len(self.__casos):
            caso_existente = self.__casos[posicion]
            if caso_existente.nombre.lower() == nombre.strip().lower():
                raise ErrorLaboratorio("Ya existe un caso con ese nombre.")
            posicion += 1

        # Creamos el caso con el próximo código
        caso = CasoUso(self.__proximo_codigo_caso, nombre, presupuesto, puntaje_minimo)
        self.__casos.append(caso)
        self.__proximo_codigo_caso += 1
        return caso


    # LISTAR CRITERIOS
    def listar_criterios(self):
        # Si la lista está vacía, informamos que no hay criterios.
        if len(self.__criterios) == 0:
            print("No hay criterios registrados.")
        
        # Recorremos la lista y mostramos cada criterio.
        else:
            posicion = 0
            while posicion < len(self.__criterios):
                criterio = self.__criterios[posicion]
                print(f"Código: {criterio.codigo} - " f"Nombre: {criterio.nombre} - " f"Peso: {criterio.peso}")
                posicion += 1


    # LISTAR OPCIONES
    def listar_opciones(self):
        if len(self.__opciones) == 0:
            print("No hay opciones registradas.")
        else:
            posicion = 0
            while posicion < len(self.__opciones):
                opcion = self.__opciones[posicion]

                print(f"\n{opcion.codigo} - {opcion.nombre}")

                # Mostramos los datos según el tipo de opción
                if isinstance(opcion, ServicioAPI): #Verificamos si la opcion es una instancia de ServicioAPI, si lo es mostramos el costo por 1000 consultas y las consultas estimadas
                    print("Tipo: Servicio API")
                    print(f"Precio por 1000 consultas: " f"USD {opcion.costo_por_1000:.2f}")
                    print(f"Consultas mensuales estimadas: " f"{opcion.consultas_estimadas}")

                elif isinstance(opcion, PlanMensual): #Verificamos si la opcion es una instancia de PlanMensual, si lo es mostramos la cantidad de usuarios y el costo por usuario
                    print("Tipo: Plan mensual")
                    print(f"Cantidad de usuarios: " f"{opcion.cantidad_usuarios}")
                    print(f"Costo por usuario: " f"USD {opcion.costo_por_usuario:.2f}")

                print(f"Costo mensual: USD {opcion.costo_estimado():.2f}")

                # Mostramos el puntaje de la opción para cada criterio
                criterio_pos = 0
                while criterio_pos < len(self.__criterios):
                    criterio = self.__criterios[criterio_pos]

                    print(f"{criterio.nombre}: " f"{opcion.puntajes[criterio.codigo]}")
                    criterio_pos += 1
                posicion += 1


    # LISTAR CASOS
    def listar_casos(self):

        if len(self.__casos) == 0:
            print("No hay casos registrados.")
        else:
            posicion = 0
            while posicion < len(self.__casos):
                caso = self.__casos[posicion]
                # Calculamos cuántas evaluaciones recomendadas tiene.
                cantidad = self.cantidad_recomendadas(caso.codigo)
                print(f"{caso} | Recomendadas: {cantidad}")
                posicion += 1


    # OBTENER EVALUACIONES DE UN CASO
    def evaluaciones_del_caso(self, codigo_caso):
        # Primero comprobamos que el caso exista.
        self.buscar_caso(codigo_caso)
        # Creamos una lista vacía para guardar sus evaluaciones.
        evaluaciones = []
        posicion = 0

        while posicion < len(self.__evaluaciones):
            evaluacion = self.__evaluaciones[posicion]

            # Comprobamos si la evaluación pertenece al caso.
            if evaluacion.caso.codigo == codigo_caso:
                evaluaciones.append(evaluacion)
            posicion += 1
        return evaluaciones

   
    # CONTAR EVALUACIONES RECOMENDADAS
    def cantidad_recomendadas(self, codigo_caso):
        evaluaciones = self.evaluaciones_del_caso(codigo_caso)
        cantidad = 0
        posicion = 0

        while posicion < len(evaluaciones):

            # Contamos solamente las recomendadas.
            if evaluaciones[posicion].estado == Evaluacion.RECOMENDADA:
                cantidad += 1
            posicion += 1
        return cantidad
    

    # LISTAR EVALUACIONES DE UN CASO
    def listar_evaluaciones(self, codigo_caso):

        # Comprobamos que el caso exista
        self.buscar_caso(codigo_caso)
        evaluaciones = self.evaluaciones_del_caso(codigo_caso)

        if len(evaluaciones) == 0:
            print("No hay evaluaciones para este caso.")
        else:
            posicion = 0
            while posicion < len(evaluaciones):
                print(evaluaciones[posicion])
                posicion += 1


    # LISTAR RANKING
    def listar_ranking(self, codigo_caso):

        # Comprobamos que el caso exista
        self.buscar_caso(codigo_caso)
        evaluaciones = self.evaluaciones_del_caso(codigo_caso)
        # Nos quedamos únicamente con las recomendadas
        recomendadas = []
        posicion = 0
        while posicion < len(evaluaciones):
            evaluacion = evaluaciones[posicion]
            if evaluacion.estado == Evaluacion.RECOMENDADA:
                recomendadas.append(evaluacion)
            posicion += 1

        # Ordenamos por puntaje descendente, costo ascendente y código ascendente
        # sorted() ordena una lista, y con "key" le decimos POR QUÉ DATOS ordenar. sorted() ordena de menor a mayor, pero queremos el puntaje de mayor a menor (con el signo menos se invierte)
        # lambda e: es una función chiquita. Recibe cada evaluación (e)
        ranking = sorted(
            recomendadas,
            key=lambda e: (-e.puntaje_total, e.costo_mensual, e.opcion.codigo)
        )

        if len(ranking) == 0:
            print("No hay opciones recomendadas para este caso.")
        else:
            posicion = 0
            while posicion < len(ranking):
                evaluacion = ranking[posicion]
                print(f"{posicion + 1}. {evaluacion.opcion.nombre} | "f"Puntaje: {evaluacion.puntaje_total:.2f} | "f"Costo: USD {evaluacion.costo_mensual:.2f}")
                posicion += 1

  
    # EVALUACIÓN INDIVIDUAL
    def evaluar_individual(self, codigo_opcion, codigo_caso):
        # Buscamos la opción y el caso seleccionados.
        opcion = self.buscar_opcion(codigo_opcion)
        caso = self.buscar_caso(codigo_caso)

        # Comprobamos si ya existe una evaluación para esa combinación.
        duplicada = False
        posicion = 0

        while posicion < len(self.__evaluaciones) and not duplicada:
            evaluacion = self.__evaluaciones[posicion]
            duplicada = (evaluacion.opcion.codigo == codigo_opcion and evaluacion.caso.codigo == codigo_caso)
            posicion += 1

        if duplicada:
            raise ErrorLaboratorio("Ya existe una evaluación para esa opción y ese caso.")

        # Si no está duplicada, creamos la evaluación.
        return self.__crear_evaluacion(opcion, caso)

  
    # CREAR EVALUACIÓN
    def __crear_evaluacion(self, opcion, caso):
        suma_ponderada = 0
        suma_pesos = 0
        posicion = 0

        # Calculamos el puntaje ponderado / evaluado
        while posicion < len(self.__criterios):
            criterio = self.__criterios[posicion]

            # Multiplicamos el puntaje por el peso del criterio.
            suma_ponderada += (opcion.puntajes[criterio.codigo] * criterio.peso)

            # Acumulamos los pesos.
            suma_pesos += criterio.peso
            posicion += 1

        # Calculamos el puntaje total ponderado.
        puntaje = suma_ponderada / suma_pesos

        # Calculamos el costo mensual de la opción
        costo = opcion.costo_estimado()

        # Determinamos el estado de la evaluación
        if costo > caso.presupuesto:
            estado = Evaluacion.FUERA_PRESUPUESTO

        elif puntaje < caso.puntaje_minimo:
            estado = Evaluacion.PUNTAJE_INSUFICIENTE

        else:
            estado = Evaluacion.RECOMENDADA

        # Creamos la evaluación con el próximo código disponible y la fecha actual
        evaluacion = Evaluacion(self.__proximo_codigo_evaluacion, datetime.now(), opcion, caso, puntaje, costo, estado)

        self.__evaluaciones.append(evaluacion)
        self.__proximo_codigo_evaluacion += 1

        return evaluacion


    # COMPARAR TODAS LAS OPCIONES PARA UN CASO
    def comparar_caso(self, codigo_caso):
         # Buscamos el caso seleccionado.
        caso = self.buscar_caso(codigo_caso)

        if len(self.__opciones) == 0:
            print("No hay opciones registradas para comparar.")
            return

        # Creamos una lista nueva sin las evaluaciones anteriores del caso seleccionado. Las de otros casos se conservan.
        evaluaciones_restantes = []

        posicion = 0
        while posicion < len(self.__evaluaciones):
            evaluacion = self.__evaluaciones[posicion]

            if evaluacion.caso.codigo != codigo_caso:
                evaluaciones_restantes.append(evaluacion)
            posicion += 1

        # Reemplazamos la lista anterior por la lista filtrada.
        self.__evaluaciones = evaluaciones_restantes

        # Creamos una evaluación nueva para cada opción.
        posicion = 0
        while posicion < len(self.__opciones):
            opcion = self.__opciones[posicion]
            self.__crear_evaluacion(opcion, caso)
            posicion += 1

   
    # ACTUALIZAR PRESUPUESTO DE UN CASO
    def actualizar_presupuesto(self, codigo_caso, nuevo_presupuesto):
        # Buscamos el caso que queremos actualizar
        caso = self.buscar_caso(codigo_caso)

        # El setter de CasoUso valida el nuevo presupuesto
        caso.presupuesto = nuevo_presupuesto

        # Recalculamos las evaluaciones para actualizar sus estados
        self.recalcular(codigo_caso=codigo_caso)

    
    # ACTUALIZAR DATOS DE UNA OPCIÓN
    def actualizar_opcion(self, codigo_opcion, costo_por_1000=None, consultas_estimadas=None, cantidad_usuarios=None, costo_por_usuario=None):
        # Buscamos la opción que queremos actualizar.
        opcion = self.buscar_opcion(codigo_opcion)

        # Actualizamos los datos según el tipo de opción
        if isinstance(opcion, ServicioAPI):

            if costo_por_1000 is not None:
                opcion.costo_por_1000 = costo_por_1000

            if consultas_estimadas is not None:
                opcion.consultas_estimadas = consultas_estimadas

        elif isinstance(opcion, PlanMensual):

            if cantidad_usuarios is not None:
                opcion.cantidad_usuarios = cantidad_usuarios

            if costo_por_usuario is not None:
                opcion.costo_por_usuario = costo_por_usuario

        # Recalculamos las evaluaciones de esta opción en todos los casos de uso donde fue evaluada
        self.recalcular(codigo_opcion = codigo_opcion)

    
    # RECALCULAR EVALUACIONES
    def recalcular(self, codigo_caso=None, codigo_opcion=None):

        posicion = 0
        # Recorremos todas las evaluaciones existentes.
        while posicion < len(self.__evaluaciones):
            evaluacion = self.__evaluaciones[posicion]

            # Si se indicó un caso, ignoramos las evaluaciones que pertenecen a otros casos.
            if codigo_caso is not None:
                if evaluacion.caso.codigo != codigo_caso:
                    posicion += 1
                    continue

            # Si se indicó una opción, ignoramos las evaluaciones que pertenecen a otras opciones.
            if codigo_opcion is not None:
                if evaluacion.opcion.codigo != codigo_opcion:
                    posicion += 1
                    continue

            # Obtenemos la opción y el caso de la evaluación.
            opcion = evaluacion.opcion
            caso = evaluacion.caso

            # Calculamos el costo actualizado.
            costo = opcion.costo_estimado()

            # El puntaje no cambia al modificar presupuesto o precio.
            puntaje = evaluacion.puntaje_total

            # Volvemos a determinar el estado.
            if costo > caso.presupuesto:
                estado = Evaluacion.FUERA_PRESUPUESTO

            elif puntaje < caso.puntaje_minimo:
                estado = Evaluacion.PUNTAJE_INSUFICIENTE

            else:
                estado = Evaluacion.RECOMENDADA

            # Actualizamos los resultados sin modificar el código ni la fecha de la evaluación.
            evaluacion.actualizar_resultados(puntaje, costo, estado)
            posicion += 1