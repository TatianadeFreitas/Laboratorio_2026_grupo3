import math  # math lo usamos solo para detectar valores raros como "inf" o "nan"

# Importamos las clases que necesitamos desde sus carpetas.
# "entities.Sistema" significa: carpeta entities, archivo Sistema.py.
from Entities.Sistema import Sistema
from Entities.OpcionIA import ServicioAPI, PlanMensual
from Exceptions.ErrorLaboratorio import ErrorLaboratorio


# Función que valida que la opción que ingresa el usuario sea válida
# (se usa para elegir dentro de los menús: de 1 a N).
def leer_opcion(minimo, maximo):
    opcion =  0  # arrancamos en 0 para que entre al while la primera vez
    while opcion < minimo or opcion > maximo:
        try:
             # int() convierte el texto a número; si no se puede, lanza ValueError
            opcion = int(input("Ingrese una de las opciones del menú: "))


            # Si es un número pero está fuera del rango, avisamos
            if opcion < minimo or opcion > maximo:
                print("Error: Ingrese una opción válida.")

        except ValueError:
             # El usuario escribió letras, símbolos o nada: no es un entero
            print("Error: Debe ingresar un número entero.")
            opcion = 0 # lo dejamos fuera de rango para que el while repita
    return opcion

def leer_texto(mensaje):                                                             #leer_texto se usa para pedir nombres: el del criterio, el
                                                                                     #seguiría con un nombre vacío. Con ella, el programa repite 
                                                                                     #la pregunta hasta que haya algo escrito:
    # Pide un texto hasta que no esté vacío                                          # de la opción de IA y el del caso de uso. Esos tres datos 
    texto = ""                                                                       #son texto libre, y la letra pide validar campos vacíos.
                                                                                     #Sin esa función, el usuario podría apretar Enter sin
    while texto.strip() == "":  # strip() saca espacios; "   " cuenta como vacío     #escribir nada, o escribir solo espacios, y el programa 
        texto = input(mensaje)                                                       #seguiría con un nombre vacío. Con ella, el programa repite 
        if texto.strip() == "":                                                      #la pregunta hasta que haya algo escrito:
            print("Error: El campo no puede estar vacío.")
    return texto.strip()  # devolvemos el texto sin espacios sobrantes

def leer_entero(mensaje, minimo=None, maximo=None):
    # Pide un entero y verifica el rango si se indica 
    # controla el rango. Con None significa "sin límite".

    while True:  # bucle infinito: solo se sale con return cuando el dato es válido
        try:
            valor = int(input(mensaje))
        except ValueError:
            print("Error: Debe ingresar un número entero.")
            continue   # vuelve al principio del while y pregunta de nuevo

        if minimo is not None and valor < minimo:
            print(f"Error: El valor debe ser mayor o igual a {minimo}.")
        elif maximo is not None and valor > maximo:
            print(f"Error: El valor debe ser menor o igual a {maximo}.")
        else:
            return valor  # válido: salimos de la función devolviendo el valor

def leer_decimal(mensaje, minimo=None, maximo=None):
    # Pide un número (acepta coma o punto decimal) y verifica el rango
    while True:
        try:
             # replace cambia la coma por punto: "12,5" -> "12.5"
            valor = float(input(mensaje).replace(",", "."))
        except ValueError:
            print("Error: Debe ingresar un número.")
            continue

        
        # float("inf") y float("nan") son válidos para Python pero no tienen
        # sentido como precio o puntaje; isfinite los detecta.
        if not math.isfinite(valor):
            print("Error: Debe ingresar un número válido.")
        elif minimo is not None and valor < minimo:
            print(f"Error: El valor debe ser mayor o igual a {minimo}.")
        elif maximo is not None and valor > maximo:
            print(f"Error: El valor debe ser menor o igual a {maximo}.")
        else:
            return valor

def elegir_caso(sistema):

 # Muestra los casos registrados y pide un código que exista.
    # Devuelve el código elegido, o None si no hay casos (así quien la
    # llama sabe que debe cancelar la operación).
   
    if len(sistema.casos) == 0:
        print("No hay casos de uso registrados.")
        return None

    sistema.listar_casos() # mostramos los casos para que el usuario vea los códigos
    while True:
        codigo = leer_entero("Ingrese el código del caso: ")
        try:
              # buscar_caso lanza ErrorLaboratorio si el código no existe
            sistema.buscar_caso(codigo)
            return codigo
        except ErrorLaboratorio as error:
            print(f"Error: {error}")  # mostramos el mensaje y volvemos a pedir

def elegir_opcion_ia(sistema):
    # Muestra las opciones y pide un código existente. Devuelve None si no hay opciones.
    if len(sistema.opciones) == 0:
        print("No hay opciones de IA registradas.")
        return None

    for opcion in sistema.opciones:
        print(f"{opcion.codigo} - {opcion.nombre}")

    while True:
        codigo = leer_entero("Ingrese el código de la opción: ")
        try:
            sistema.buscar_opcion(codigo)
            return codigo
        except ErrorLaboratorio as error:
            print(f"Error: {error}")

# ---------------------------------------------------------------
# REGISTRAR
# ---------------------------------------------------------------

def registrar_criterio(sistema):
    # No se permiten criterios nuevos una vez registrada la primera opción
        # la primera opción. Lo controlamos acá para no pedir datos en vano.
    if len(sistema.opciones) > 0:
        print("Error: No se pueden registrar criterios después de registrar opciones.")
        return

    registrado = False
    while not registrado:  # repetimos hasta que se registre sin errores
        nombre = leer_texto("Nombre del criterio: ")
        peso = leer_entero("Peso (entero positivo): ", 1) #mínimo 1 = positivo
        try:
            criterio = sistema.registrar_criterio(nombre, peso)
            print(f"Criterio registrado con código {criterio.codigo}.")
            registrado = True  # esto corta el while
        except (ErrorLaboratorio, ValueError) as error:
             # Por ejemplo: nombre duplicado. Mostramos el error y se vuelve a pedir
            print(f"Error: {error}")

def registrar_opcion(sistema):
    # Debe existir al menos un criterio para poder registrar opciones.
    if len(sistema.criterios) == 0:
        print("Error: Primero debe registrar al menos un criterio.")
        return
 
    # Armamos una lista con los nombres ya usados (en minúscula) para
    # controlar duplicados sin distinguir mayúsculas.
    nombres = []
    for opcion in sistema.opciones:
        nombres.append(opcion.nombre.lower())
 
    nombre = leer_texto("Nombre de la opción: ")
    while nombre.lower() in nombres:
        print("Error: Ya existe una opción con ese nombre.")
        nombre = leer_texto("Nombre de la opción: ")
 
    print("Tipo de opción:")
    print("1: Servicio API")
    print("2: Plan mensual")
    tipo = leer_entero("Ingrese el tipo: ", 1, 2)
 
    # Estas variables empiezan en None; solo se completan las que
    # corresponden al tipo elegido.
    costo_por_1000 = None
    consultas_estimadas = None
    cantidad_usuarios = None
    costo_por_usuario = None
 
    if tipo == 1:
        # Servicio API: costo = (consultas / 1000) x precio por 1000
        costo_por_1000 = leer_decimal("Precio por cada 1000 consultas (USD): ", 0)
        consultas_estimadas = leer_entero("Cantidad estimada de consultas al mes: ", 1)
    else:
        # Plan mensual: costo = usuarios x costo por usuario
        cantidad_usuarios = leer_entero("Cantidad de usuarios: ", 1)
        costo_por_usuario = leer_decimal("Costo mensual por usuario (USD): ", 0)
 
    # Pedimos un puntaje entero de 0 a 10 por cada criterio y los guardamos
    # en un diccionario con formato {codigo_criterio: puntaje}.
    # Al ser un diccionario no puede haber criterios duplicados, y al
    # recorrer todos los criterios no se omite ninguno.
    puntajes = {}
    for criterio in sistema.criterios:
        puntajes[criterio.codigo] = leer_entero(
            f"Puntaje (0 a 10) para '{criterio.nombre}': ", 0, 10
        )
 
    try:
        # Sistema crea el objeto correcto (ServicioAPI o PlanMensual) según el tipo
        opcion = sistema.registrar_opcion(
            nombre, tipo, puntajes,
            costo_por_1000, consultas_estimadas,
            cantidad_usuarios, costo_por_usuario
        )
        print(f"Opción registrada con código {opcion.codigo}.")
    except (ErrorLaboratorio, ValueError) as error:
        print(f"Error: {error}")
 
 
def registrar_caso(sistema):
    # Igual que con las opciones: controlamos nombre único sin distinguir mayúsculas.
    nombres = []
    for caso in sistema.casos:
        nombres.append(caso.nombre.lower())
 
    nombre = leer_texto("Nombre del caso de uso: ")
    while nombre.lower() in nombres:
        print("Error: Ya existe un caso con ese nombre.")
        nombre = leer_texto("Nombre del caso de uso: ")
 
    presupuesto = leer_decimal("Presupuesto mensual (USD): ", 0)             # >= 0
    puntaje_minimo = leer_decimal("Puntaje mínimo aceptable (0 a 10): ", 0, 10)
 
    try:
        caso = sistema.registrar_caso(nombre, presupuesto, puntaje_minimo)
        print(f"Caso registrado con código {caso.codigo}.")
    except (ErrorLaboratorio, ValueError) as error:
        print(f"Error: {error}")
 
 
def registrar_evaluacion(sistema):
    # Evaluación individual: una opción para un caso.
    codigo_opcion = elegir_opcion_ia(sistema)
    if codigo_opcion is None:  # no hay opciones: cancelamos
        return
 
    codigo_caso = elegir_caso(sistema)
    if codigo_caso is None:  # no hay casos: cancelamos
        return
 
    try:
        # Si ya existía una evaluación para esa combinación, Sistema lanza
        # ErrorLaboratorio y no crea otra (se informa el duplicado).
        evaluacion = sistema.evaluar_individual(codigo_opcion, codigo_caso)
        print(evaluacion)  # usa el __str__ de Evaluacion
    except (ErrorLaboratorio, ValueError) as error:
        print(f"Error: {error}")
 
 
# ---------------------------------------------------------------
# COMPARAR
# ---------------------------------------------------------------
 
def comparar_opciones(sistema):
    codigo_caso = elegir_caso(sistema)
    if codigo_caso is None:
        return
 
    try:
        # Esto borra las evaluaciones anteriores del caso y crea una nueva
        # por cada opción. Si no hay opciones, Sistema muestra un mensaje.
        sistema.comparar_caso(codigo_caso)
 
        # Solo mostramos el resultado si realmente se comparó algo
        if len(sistema.opciones) > 0:
            print("Comparación realizada:")
            sistema.listar_evaluaciones(codigo_caso)
    except (ErrorLaboratorio, ValueError) as error:
        print(f"Error: {error}")
 
 
# ---------------------------------------------------------------
# ACTUALIZAR
# ---------------------------------------------------------------
 
def actualizar_presupuesto(sistema):
    codigo_caso = elegir_caso(sistema)
    if codigo_caso is None:
        return
 
    nuevo_presupuesto = leer_decimal("Nuevo presupuesto mensual (USD): ", 0)
 
    try:
        # Sistema cambia el presupuesto y recalcula el estado de las
        # evaluaciones de ese caso (sin cambiar códigos ni fechas).
        sistema.actualizar_presupuesto(codigo_caso, nuevo_presupuesto)
        print("Presupuesto actualizado y evaluaciones recalculadas.")
    except (ErrorLaboratorio, ValueError) as error:
        print(f"Error: {error}")
 
 
def actualizar_opcion(sistema):
    codigo_opcion = elegir_opcion_ia(sistema)
    if codigo_opcion is None:
        return
 
    # Buscamos la opción para saber de qué tipo es, ya que cada tipo
    # tiene datos distintos para modificar.
    opcion = sistema.buscar_opcion(codigo_opcion)
 
    try:
        # isinstance pregunta si el objeto es de esa clase
        if isinstance(opcion, ServicioAPI):
            costo_por_1000 = leer_decimal("Nuevo precio por cada 1000 consultas (USD): ", 0)
            consultas = leer_entero("Nueva cantidad estimada de consultas: ", 1)
            sistema.actualizar_opcion(
                codigo_opcion,
                costo_por_1000=costo_por_1000,
                consultas_estimadas=consultas
            )
        elif isinstance(opcion, PlanMensual):
            usuarios = leer_entero("Nueva cantidad de usuarios: ", 1)
            costo_usuario = leer_decimal("Nuevo costo mensual por usuario (USD): ", 0)
            sistema.actualizar_opcion(
                codigo_opcion,
                cantidad_usuarios=usuarios,
                costo_por_usuario=costo_usuario
            )
        # Sistema recalcula el costo y el estado de todas las evaluaciones
        # de esta opción (en todos los casos). Los puntajes no cambian.
        print("Opción actualizada y evaluaciones recalculadas.")
    except (ErrorLaboratorio, ValueError) as error:
        print(f"Error: {error}")
 
 
# ---------------------------------------------------------------
# LISTAR
# ---------------------------------------------------------------
 
def listar_evaluaciones_caso(sistema):
    # Primero se elige el caso y después se listan sus evaluaciones.
    codigo_caso = elegir_caso(sistema)
    if codigo_caso is not None:
        sistema.listar_evaluaciones(codigo_caso)
 
 
def listar_ranking_caso(sistema):
    codigo_caso = elegir_caso(sistema)
    if codigo_caso is not None:
        sistema.listar_ranking(codigo_caso)
 
 
# ---------------------------------------------------------------
# MENÚS
# ---------------------------------------------------------------
 
def mostrar_menu():
    # Muestra el menú principal y devuelve la opción elegida (1 a 5).
    print("\n--- MENÚ PRINCIPAL ---")  # \n deja una línea en blanco antes
    print("1: Registrar")
    print("2: Comparar opciones para un caso")
    print("3: Actualizar")
    print("4: Listar")
    print("5: Salir del sistema")
 
    opcion = leer_opcion(1, 5)
 
    return opcion
 
 
def menu_registrar(sistema):
    # Submenú: se queda repitiendo hasta que el usuario elige 5 (Salir).
    # Después de cada acción vuelve a mostrarse el submenú, como pide la letra.
    opcion = 0
    while opcion != 5:
        print("\n--- MENÚ REGISTRAR ---")
        print("1: Criterio")
        print("2: Opción de IA")
        print("3: Caso de uso")
        print("4: Evaluación individual")
        print("5: Salir")
 
        opcion = leer_opcion(1, 5)
 
        # Cada número llama a su función. Con 5 no se hace nada y el
        # while termina, volviendo al menú principal.
        if opcion == 1:
            registrar_criterio(sistema)
        elif opcion == 2:
            registrar_opcion(sistema)
        elif opcion == 3:
            registrar_caso(sistema)
        elif opcion == 4:
            registrar_evaluacion(sistema)
 
 
def menu_actualizar(sistema):
    # Submenú de actualizar: sale con 3.
    opcion = 0
    while opcion != 3:
        print("\n--- MENÚ ACTUALIZAR ---")
        print("1: Presupuesto de un caso")
        print("2: Precio o consumo de una opción")
        print("3: Salir")
 
        opcion = leer_opcion(1, 3)
 
        if opcion == 1:
            actualizar_presupuesto(sistema)
        elif opcion == 2:
            actualizar_opcion(sistema)
 
 
def menu_listar(sistema):
    # Submenú de listar: sale con 6.
    opcion = 0
    while opcion != 6:
        print("\n--- MENÚ LISTAR ---")
        print("1: Criterios")
        print("2: Opciones")
        print("3: Casos de uso")
        print("4: Evaluaciones de un caso")
        print("5: Ranking de un caso")
        print("6: Salir")
 
        opcion = leer_opcion(1, 6)
 
        if opcion == 1:
            sistema.listar_criterios()
        elif opcion == 2:
            sistema.listar_opciones()
        elif opcion == 3:
            sistema.listar_casos()
        elif opcion == 4:
            listar_evaluaciones_caso(sistema)
        elif opcion == 5:
            listar_ranking_caso(sistema)
 
 
if __name__ == "__main__":
    # Creamos UN solo Sistema, que guarda todos los datos mientras el
    # programa está abierto (no hay archivos ni base de datos).
    sistema = Sistema()

    opcion = 0
    while opcion != 5:  # el programa termina al elegir 5 en el menú principal
        opcion = mostrar_menu()

        if opcion == 1:
            menu_registrar(sistema)
        elif opcion == 2:
            comparar_opciones(sistema)
        elif opcion == 3:
            menu_actualizar(sistema)
        elif opcion == 4:
            menu_listar(sistema)

    print("Gracias por usar el sistema. ¡Hasta luego!")