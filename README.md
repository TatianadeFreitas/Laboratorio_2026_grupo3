# Laboratorio 2026 - Programación 1

Gupo número 3

Integrantes: Valentina Alayon, Isis Capdevielle, Tatiana de Freitas

# De qué trata

Es un programa de consola en Python para comparar opciones de IA (por ejemplo Claude, OpenAI o Gemini) y ver cuál conviene para distintos casos de uso de una empresa. Se cargan criterios, opciones y casos, y el programa calcula el puntaje y el costo de cada opción, le asigna un estado y arma un ranking.
No usa servicios reales ni internet, y los datos se guardan solo mientras el programa está abierto.

## Cómo ejecutarlo

Hace falta Python 3.10 o superior. No usamos librerías externas, solo `abc`, `datetime` y `math`, que vienen con Python, así que no hay que instalar nada.

Desde una terminal, parado en la carpeta donde está `main.py`:
Hay que ejecutarlo desde ahí, si no Python no encuentra las carpetas `Entities` y `Exceptions`.

## Archivos

- `main.py`: los menús y el ingreso de datos.
- `entities/Sistema.py`: guarda las listas y tiene la lógica del programa.
- `entities/OpcionIA.py`: la clase abstracta OpcionIA y sus hijas ServicioAPI y PlanMensual.
- `entities/Criterio.py`, `entities/CasoUso.py`, `entities/Evaluacion.py`
- `exceptions/ErrorLaboratorio.py`: la excepción propia que usamos para los errores de datos.

## Cómo probarlo

Primero hay que cargar todos los criterios, porque después de registrar la primera opción ya no se pueden agregar más. Después se cargan las opciones (con un puntaje de 0 a 10 por cada criterio) y los casos de uso. Con eso ya se puede comparar las opciones para un caso o hacer evaluaciones individuales, y probar las actualizaciones y los listados.

## Cómo se calcula

- Puntaje total: suma de (puntaje × peso) dividida la suma de los pesos.
- Costo de un servicio API: (consultas estimadas / 1000) × precio cada 1000 consultas.
- Costo de un plan mensual: usuarios × costo por usuario.
- Estado: "fuera de presupuesto" si el costo supera el presupuesto del caso. Si no, "puntaje insuficiente" si el puntaje es menor al mínimo. Si no, "recomendada". Si es justo igual al presupuesto o al mínimo, se considera válido.

## Errores

Si se ingresa un dato inválido, un nombre repetido o un código que no existe, el programa muestra un mensaje y vuelve a pedir el dato.