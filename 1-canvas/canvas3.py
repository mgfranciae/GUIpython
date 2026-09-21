import math
import tkinter as tk
from tkinter import messagebox


class Puerto:
    """Representa un punto de conexión en una figura (Puerto A o Puerto B)."""
    
    def __init__(self, nombre: str, offset_x: float, offset_y: float):
        self.nombre = nombre        # "A" o "B"
        self.offset_x = offset_x    # Desplazamiento X respecto al centro de la figura
        self.offset_y = offset_y    # Desplazamiento Y respecto al centro de la figura
        self.x = 0.0                # Coordenada X absoluta en el Canvas
        self.y = 0.0                # Coordenada Y absoluta en el Canvas
        self.id_canvas = None       # ID del círculo visual del puerto en Tkinter

    def actualizar_posicion(self, centro_x: float, centro_y: float):
        """Recalcula la posición absoluta del puerto basada en el centro de la figura."""
        self.x = centro_x + self.offset_x
        self.y = centro_y + self.offset_y


class FiguraConectabla:
    """Clase base que representa una figura geométrica con puertos de conexión."""
    
    def __init__(self, id_figura: int, tipo: str, x: float, y: float, tamano: float):
        self.id_figura = id_figura  # ID del objeto principal en el Canvas
        self.tipo = tipo            # "Círculo", "Rectángulo" o "Triángulo"
        self.x = x                  # Coordenada X del centro
        self.y = y                  # Coordenada Y del centro
        self.tamano = tamano        # Dimensión (radio o lado)
        self.id_texto = None        # ID del texto con la etiqueta de la figura

        # Crear los dos puertos con desplazamientos respecto al centro
        radio_offset = tamano * 0.7
        self.puertos = {
            "A": Puerto("A", offset_x=-radio_offset, offset_y=0), # Izquierda
            "B": Puerto("B", offset_x=radio_offset, offset_y=0)   # Derecha
        }
        self.actualizar_puertos()

    def actualizar_puertos(self):
        """Actualiza las coordenadas absolutas de los puertos A y B."""
        for puerto in self.puertos.values():
            puerto.actualizar_posicion(self.x, self.y)

    def mover(self, dx: float, dy: float):
        """Desplaza el centro de la figura y recalcula las posiciones de sus puertos."""
        self.x += dx
        self.y += dy
        self.actualizar_puertos()


class Conexion:
    """Representa un cable o línea entre el puerto de una figura origen y el puerto de otra destino."""
    
    def __init__(self, figura_origen: FiguraConectabla, puerto_origen_nombre: str,
                 figura_destino: FiguraConectabla, puerto_destino_nombre: str, id_linea: int):
        self.figura_origen = figura_origen
        self.puerto_origen_nombre = puerto_origen_nombre
        self.figura_destino = figura_destino
        self.puerto_destino_nombre = puerto_destino_nombre
        self.id_linea = id_linea  # ID de la línea dibujada en el Canvas

    def obtener_par_conectado(self) -> str:
        """Devuelve una cadena legible con la descripción del par conectado."""
        return (f"{self.figura_origen.tipo} (Puerto {self.puerto_origen_nombre}) ───> "
                f"{self.figura_destino.tipo} (Puerto {self.puerto_destino_nombre})")


class DiagramaConexionesApp:
    """Controlador principal de la aplicación con Tkinter."""

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Diagrama Interactivo con Puertos de Conexión")
        self.root.geometry("850x550")

        # Diccionarios para rastrear los objetos activos por su ID de Canvas
        self.figuras = {}      # {id_canvas: objeto FiguraConectabla}
        self.puertos_map = {}  # {id_canvas_puerto: (objeto Figura, "A"|"B")}
        self.conexiones = []   # Lista de objetos Conexion

        # Variables de estado para interacciones del ratón
        self.figura_seleccionada = None
        self.x_previo = 0
        self.y_previo = 0

        # Estado para la creación de conexiones
        self.puerto_origen_temp = None  # Tuple: (Figura, NombrePuerto)

        self._crear_interfaz()
        self._vincular_eventos()
        self._crear_figuras_iniciales()

    def _crear_interfaz(self):
        """Construye los widgets del formulario y del panel del Canvas."""
        # Panel superior de instrucciones
        lbl_instrucciones = tk.Label(
            self.root,
            text="• Arrastra las figuras con Clic Izquierdo.\n"
                 "• Haz Clic sobre un Puerto (rojo/azul) para iniciar/cerrar una línea de conexión.",
            bg="#ECEFF1", font=("Arial", 9), pady=6, justify="left"
        )
        lbl_instrucciones.pack(fill="x")

        # Panel inferior para mostrar el estado de las conexiones activas
        frame_estado = tk.Frame(self.root, bg="#263238", pady=6, padx=10)
        frame_estado.pack(side="bottom", fill="x")

        tk.Label(frame_estado, text="Conexiones Activas:", fg="#80CBC4", bg="#263238",
                 font=("Arial", 9, "bold")).pack(anchor="w")
        
        self.lbl_lista_conexiones = tk.Label(
            frame_estado, text="Sin conexiones.", fg="white", bg="#263238",
            font=("Consolas", 9), justify="left"
        )
        self.lbl_lista_conexiones.pack(anchor="w")

        # Lienzo principal (Canvas)
        self.canvas = tk.Canvas(self.root, bg="#FFFFFF", highlightthickness=1, highlightbackground="#CFD8DC")
        self.canvas.pack(fill="both", expand=True, padx=10, pady=10)

    def _crear_figuras_iniciales(self):
        """Genera un Círculo, un Rectángulo y un Triángulo con sus respectivos puertos."""
        self._crear_figura("Rectángulo", 150, 200, 50, "#2196F3")
        self._crear_figura("Círculo", 400, 200, 45, "#F44336")
        self._crear_figura("Triángulo", 650, 200, 50, "#4CAF50")

    def _crear_figura(self, tipo: str, x: float, y: float, tamano: float, color: str):
        """Dibuja una figura, genera sus conectores A/B e instala las etiquetas del puerto."""
        radio = tamano

        # 1. Dibujar el cuerpo principal en el Canvas
        if tipo == "Rectángulo":
            id_canvas = self.canvas.create_rectangle(x - radio, y - radio, x + radio, y + radio,
                                                     fill=color, outline="black", width=2, tags="figura")
        elif tipo == "Círculo":
            id_canvas = self.canvas.create_oval(x - radio, y - radio, x + radio, y + radio,
                                                fill=color, outline="black", width=2, tags="figura")
        elif tipo == "Triángulo":
            puntos = [x, y - radio, x - radio, y + radio, x + radio, y + radio]
            id_canvas = self.canvas.create_polygon(puntos, fill=color, outline="black", width=2, tags="figura")

        # 2. Crear instancia del Modelo de datos
        figura = FiguraConectabla(id_canvas, tipo, x, y, tamano)
        self.figuras[id_canvas] = figura

        # 3. Dibujar la etiqueta con el nombre del tipo de figura
        figura.id_texto = self.canvas.create_text(x, y, text=tipo, fill="white",
                                                  font=("Arial", 9, "bold"), tags="texto")

        # 4. Dibujar visualmente los puertos A y B en el Canvas
        colores_puertos = {"A": "#E91E63", "B": "#00BCD4"}  # Rosa para A, Creado/Cian para B
        r_puerto = 6  # Radio visual del círculo del conector

        for nombre_p, puerto in figura.puertos.items():
            id_p = self.canvas.create_oval(
                puerto.x - r_puerto, puerto.y - r_puerto,
                puerto.x + r_puerto, puerto.y + r_puerto,
                fill=colores_puertos[nombre_p], outline="black", width=1, tags="puerto"
            )
            puerto.id_canvas = id_p
            # Asociar el ID visual del puerto con su figura y nombre de puerto
            self.puertos_map[id_p] = (figura, nombre_p)

            # Etiqueta estática "A" o "B" junto al conector
            self.canvas.create_text(puerto.x, puerto.y - 12, text=nombre_p,
                                    font=("Arial", 8, "bold"), fill="#37474F", tags=f"p_label_{id_canvas}")

    def _vincular_eventos(self):
        """Asigna los eventos del ratón a las figuras y puertos."""
        # Eventos para arrastrar las figuras
        self.canvas.tag_bind("figura", "<ButtonPress-1>", self._al_presionar_figura)
        self.canvas.tag_bind("figura", "<B1-Motion>", self._al_arrastrar_figura)
        self.canvas.tag_bind("figura", "<ButtonRelease-1>", self._al_soltar_figura)

        # Evento para hacer clic en los puertos y trazar líneas de conexión
        self.canvas.tag_bind("puerto", "<Button-1>", self._al_hacer_clic_puerto)

    # --- Lógica de Arrastre ---

    def _al_presionar_figura(self, event):
        """Guarda la referencia de la figura bajo el puntero y su coordenada inicial."""
        elementos = self.canvas.find_withtag("current")
        if elementos:
            id_canvas = elementos[0]
            if id_canvas in self.figuras:
                self.figura_seleccionada = self.figuras[id_canvas]
                self.x_previo = event.x
                self.y_previo = event.y

    def _al_arrastrar_figura(self, event):
        """Desplaza la figura, sus etiquetas, sus puertos y redibuja las líneas vinculadas."""
        if self.figura_seleccionada:
            dx = event.x - self.x_previo
            dy = event.y - self.y_previo

            fig = self.figura_seleccionada

            # 1. Mover la figura principal y su texto
            self.canvas.move(fig.id_figura, dx, dy)
            self.canvas.move(fig.id_texto, dx, dy)

            # 2. Actualizar las coordenadas de los modelos de datos
            fig.mover(dx, dy)

            # 3. Mover los elementos gráficos de los puertos
            for nombre_p, puerto in fig.puertos.items():
                self.canvas.move(puerto.id_canvas, dx, dy)

            # Mover las etiquetas textuales "A" y "B"
            self.canvas.move(f"p_label_{fig.id_figura}", dx, dy)

            # 4. Redibujar las líneas de conexión asociadas a esta figura
            self._actualizar_lineas_conexion()

            self.x_previo = event.x
            self.y_previo = event.y

    def _al_soltar_figura(self, event):
        """Libera la figura seleccionada."""
        self.figura_seleccionada = None

    # --- Lógica de Conexión entre Puertos ---

    def _al_hacer_clic_puerto(self, event):
        """Gestor de estados para conectar dos puertos secuencialmente."""
        elementos = self.canvas.find_withtag("current")
        if not elementos:
            return

        id_puerto_clicado = elementos[0]
        figura, nombre_puerto = self.puertos_map[id_puerto_clicado]

        # Estado 1: Primer Clic (Seleccionar Puerto de Origen)
        if self.puerto_origen_temp is None:
            self.puerto_origen_temp = (figura, nombre_puerto)
            # Resaltar el puerto seleccionado aumentando el grosor de su borde
            self.canvas.itemconfig(id_puerto_clicado, width=3)

        # Estado 2: Segundo Clic (Seleccionar Puerto de Destino)
        else:
            figura_origen, p_origen_nombre = self.puerto_origen_temp

            # Restaurar el grosor del borde del conector de origen
            puerto_origen_obj = figura_origen.puertos[p_origen_nombre]
            self.canvas.itemconfig(puerto_origen_obj.id_canvas, width=1)

            # Validar que no se conecte la figura a sí misma
            if figura_origen.id_figura == figura.id_figura:
                messagebox.showwarning("Conexión Inválida", "No puedes conectar dos puertos de la misma figura.")
                self.puerto_origen_temp = None
                return

            # Crear la línea visual en el Canvas
            p_orig = figura_origen.puertos[p_origen_nombre]
            p_dest = figura.puertos[nombre_puerto]

            id_linea = self.canvas.create_line(
                p_orig.x, p_orig.y, p_dest.x, p_dest.y,
                fill="#37474F", width=2, dash=(4, 2), tags="linea_conexion"
            )

            # Enviar la línea al fondo para que no tape a las figuras ni a los puertos
            self.canvas.tag_lower(id_linea)

            # Guardar el registro de la nueva conexión
            nueva_conexion = Conexion(figura_origen, p_origen_nombre, figura, nombre_puerto, id_linea)
            self.conexiones.append(nueva_conexion)

            # Reiniciar la variable de estado temporal
            self.puerto_origen_temp = None

            # Actualizar el texto del panel inferior con los pares conectados
            self._actualizar_panel_estado()

    def _actualizar_lineas_conexion(self):
        """Recalcula las coordenadas de todas las líneas dibujadas según la posición actual de los puertos."""
        for c in self.conexiones:
            p_orig = c.figura_origen.puertos[c.puerto_origen_nombre]
            p_dest = c.figura_destino.puertos[c.puerto_destino_nombre]

            # Actualizar los puntos de origen (x1, y1) y destino (x2, y2) de la línea en el Canvas
            self.canvas.coords(c.id_linea, p_orig.x, p_orig.y, p_dest.x, p_dest.y)

    def _actualizar_panel_estado(self):
        """Genera y muestra la lista legible de pares conectados en la interfaz."""
        if not self.conexiones:
            self.lbl_lista_conexiones.config(text="Sin conexiones.")
            return

        lineas_texto = [f"• {conexion.obtener_par_conectado()}" for conexion in self.conexiones]
        self.lbl_lista_conexiones.config(text="\n".join(lineas_texto))


if __name__ == "__main__":
    ventana_principal = tk.Tk()
    app = DiagramaConexionesApp(ventana_principal)
    ventana_principal.mainloop()