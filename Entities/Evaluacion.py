from datetime import datetime

class Evaluacion:
    # Definimos constantes de clase para los estados posibles exigidos en el obligatorio.
    # Esto evita usar "strings magicos" sueltos por el codigo y previene errores de tipeo.

    RECOMENDADA = "recomendada"  # Estado asignado cuando la opción cumple tanto con el presupuesto como con el puntaje mínimo requerido.
    FUERA_PRESUPUESTO = "fuera de presupuesto"    # Estado asignado cuando el costo mensual de la opción supera el presupuesto disponible del caso.
    PUNTAJE_INSUFICIENTE = "puntaje insuficiente"  # Estado asignado cuando cumple con el presupuesto, pero su puntaje total es menor al mínimo aceptable.

    def __init__(self, codigo, fecha, opcion, caso, puntaje_total, costo_mensual, estado):
        # Asignamos los atributos privados que almacenan el estado de la evaluación
        self.__codigo = codigo             # Identificador único de la evaluación
        self.__fecha = fecha               # Objeto datetime con la fecha y hora de creación
        self.__opcion = opcion             # Referencia al objeto OpcionIA evaluado
        self.__caso = caso                 # Referencia al objeto CasoUso evaluado
        self.__puntaje_total = puntaje_total     # Puntaje ponderado calculado (0 a 10)
        self.__costo_mensual = costo_mensual     # Costo estimado en USD calculado
        self.__estado = estado             # Estado resultante según presupuesto y puntaje

    # --- Propiedades (Getters) para acceder de forma segura a los atributos privados ---
    @property
    def codigo(self):
        return self.__codigo

    @property
    def fecha(self):
        return self.__fecha

    @property
    def opcion(self):
        return self.__opcion

    @property
    def caso(self):
        return self.__caso

    @property
    def puntaje_total(self):
        return self.__puntaje_total

    @property
    def costo_mensual(self):
        return self.__costo_mensual

    @property
    def estado(self):
        return self.__estado

    # Setter para el estado, útil por ejemplo al actualizar presupuestos o precios
    @estado.setter
    def estado(self, nuevo_estado):
        self.__estado = nuevo_estado

    def __str__(self):
        # Formateamos la fecha a un formato legible de texto (Día/Mes/Año Hora:Minuto:Segundo)
        fecha_str = self.__fecha.strftime("%d/%m/%Y %H:%M:%S")
        
        # Retornamos una cadena limpia con toda la información clave de la evaluación
        return (f"Código: {self.__codigo} | Fecha: {fecha_str} | "
                f"Opción: {self.__opcion.nombre} | Caso: {self.__caso.nombre} | "
                f"Presupuesto del caso: USD {self.__caso.presupuesto:.2f} | "
                f"Puntaje: {self.__puntaje_total:.2f} | Costo: USD {self.__costo_mensual:.2f} | "
                f"Estado: {self.__estado}")
                #:.2f sirve para mostrar el puntaje y costo con 2 decimales
                
    def actualizar_resultados(self, puntaje, costo, estado):
        self.__puntaje_total = puntaje
        self.__costo_mensual = costo
        self.__estado = estado