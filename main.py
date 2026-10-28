# Función que valida que la opción que ingresa el usuario sea válida
def leer_opcion(minimo, maximo):
    opcion = 0
    while opcion < minimo or opcion > maximo:
        try:
            opcion = int(input("Ingrese una de las opciones del menú: "))

            if opcion < minimo or opcion > maximo:
                print("Error: Ingrese una opción válida.")

        except ValueError:
            print("Error: Debe ingresar un número entero.")
            opcion = 0
    return opcion


def mostrar_menu():
    print("--- MENÚ PRINCIPAL ---")
    print("1: Registrar")
    print("2: Comparar opciones para un caso")
    print("3: Actualizar")
    print("4: Listar")
    print("5: Salir del sistema")

    opcion = leer_opcion(1, 5)


    return opcion


def menu_registrar():
    print("--- MENÚ REGISTRAR ---")
    print("1: Criterio")
    print("2: Opción de IA")
    print("3: Caso de uso")
    print("4: Evaluación individual")
    print("5: Salir")

    opcion = leer_opcion(1, 5)

    '''
    if opcion == 1:
    
    elif opcion == 2:
    
    elif opcion == 3:
    
    elif opcion == 4:
    
    elif opcion == 5:
    '''


def menu_actualizar():
    print("--- MENÚ ACTUALIZAR ---")
    print("1: Presupuesto de un caso")
    print("2: Precio o consumo de una opción")
    print("3: Salir")

    opcion = leer_opcion(1, 3)
    '''
    if opcion == 1:
    
    elif opcion == 2:
    
    elif opcion == 3:
    
    elif opcion == 4:
    
    elif opcion == 5:
    '''

def menu_listar():
    print("--- MENÚ LISTAR ---")
    print("1: Criterios")
    print("2: Opciones")
    print("3: Casos de uso")
    print("4: Evaluaciones de un caso")
    print("5: Ranking de un caso")
    print("6: Salir")

    opcion = leer_opcion(1, 6)
    '''
    if opcion == 1:
    
    elif opcion == 2:
    
    elif opcion == 3:
    
    elif opcion == 4:
    
    elif opcion == 5:
    '''
