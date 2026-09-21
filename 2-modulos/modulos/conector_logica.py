"""
Mapeo y cálculo de coordenadas para figuras y puertos.
"""

class PuertoModel:
    def __init__(self, nombre: str, offset_x: float, offset_y: float):
        self.nombre = nombre
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.x = 0.0
        self.y = 0.0

    def calcular_posicion(self, centro_x: float, centro_y: float):
        self.x = centro_x + self.offset_x
        self.y = centro_y + self.offset_y


class FiguraModel:
    def __init__(self, id_figura: int, tipo: str, x: float, y: float, tamano: float):
        self.id_figura = id_figura
        self.tipo = tipo
        self.x = x
        self.y = y
        self.tamano = tamano

        # Crear puertos A (izquierda) y B (derecha)
        offset = tamano * 0.7
        self.puertos = {
            "A": PuertoModel("A", offset_x=-offset, offset_y=0),
            "B": PuertoModel("B", offset_x=offset, offset_y=0)
        }
        self.actualizar_puertos()

    def actualizar_puertos(self):
        for puerto in self.puertos.values():
            puerto.calcular_posicion(self.x, self.y)

    def desplazar(self, dx: float, dy: float):
        self.x += dx
        self.y += dy
        self.actualizar_puertos()


class GestorDiagrama:
    """Clase principal de lógica que administra todas las entidades."""

    def __init__(self):
        self.figuras = {}      # {id_canvas: FiguraModel}
        self.puertos_map = {}  # {id_puerto_canvas: (FiguraModel, nombre_puerto)}
        self.conexiones = []   # Lista de tuplas: (figura_orig, p_orig, figura_dest, p_dest, id_linea)

    def registrar_figura(self, id_canvas: int, tipo: str, x: float, y: float, tamano: float) -> FiguraModel:
        figura = FiguraModel(id_canvas, tipo, x, y, tamano)
        self.figuras[id_canvas] = figura
        return figura

    def registrar_puerto(self, id_puerto_canvas: int, figura: FiguraModel, nombre_puerto: str):
        self.puertos_map[id_puerto_canvas] = (figura, nombre_puerto)

    def mover_figura(self, id_canvas: int, dx: float, dy: float):
        if id_canvas in self.figuras:
            self.figuras[id_canvas].desplazar(dx, dy)

    def agregar_conexion(self, figura_origen: FiguraModel, p_origen: str,
                         figura_destino: FiguraModel, p_destino: str, id_linea: int):
        self.conexiones.append((figura_origen, p_origen, figura_destino, p_destino, id_linea))

    def obtener_resumen_conexiones(self) -> list[str]:
        resumen = []
        for orig, p_o, dest, p_d, _ in self.conexiones:
            resumen.append(f"• {orig.tipo} (Puerto {p_o}) ───> {dest.tipo} (Puerto {p_d})")
        return resumen