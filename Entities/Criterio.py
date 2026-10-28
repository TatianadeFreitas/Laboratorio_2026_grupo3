class Criterio:
    # nombre único (sin distinguir mayúsculas) y peso entero positivo
    def __init__(self, codigo, nombre, peso):
        self._codigo = codigo #es una asignación directa al atributo interno. No pasar por ningún método, no hay validación
        self.nombre = nombre
        self.peso = peso

