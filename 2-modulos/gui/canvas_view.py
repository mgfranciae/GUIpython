"""
Vista del Canvas e Interfaz de Usuario.
"""

import tkinter as tk
from tkinter import messagebox
from modulos.conector_logica import GestorDiagrama, FiguraModel


class AplicacionesCanvasGUI:
    def __init__(self, root: tk.Tk, gestor_logica: GestorDiagrama):
        self.root = root
        self.gestor = gestor_logica
        
        self.root.title("Diseño Desacoplado (GUI / Módulos)")
        self.root.geometry("850x550")

        # Estado visual
        self.figura_seleccionada_id = None
        self.puerto_origen_temp = None
        self.x_previo = 0
        self.y_previo = 0

        self._construir_widgets()
        self._vincular_eventos()

    def _construir_widgets(self):
        # Panel inferior para reporte de estado
        frame_estado = tk.Frame(self.root, bg="#263238", pady=6, padx=10)
        frame_estado.pack(side="bottom", fill="x")

        tk.Label(frame_estado, text="Conexiones Activas:", fg="#80CBC4", bg="#263238",
                 font=("Arial", 9, "bold")).pack(anchor="w")
        
        self.lbl_lista_conexiones = tk.Label(
            frame_estado, text="Sin conexiones.", fg="white", bg="#263238",
            font=("Consolas", 9), justify="left"
        )
        self.lbl_lista_conexiones.pack(anchor="w")

        # Lienzo (Canvas)
        self.canvas = tk.Canvas(self.root, bg="#FFFFFF", highlightthickness=1, highlightbackground="#CFD8DC")
        self.canvas.pack(fill="both", expand=True, padx=10, pady=10)

    def crear_figura_grafica(self, tipo: str, x: float, y: float, tamano: float, color: str):
        """Dibuja la figura y le delega el almacenamiento del estado al gestor de lógica."""
        radio = tamano

        # 1. Dibujar en el Canvas
        if tipo == "Rectángulo":
            id_canvas = self.canvas.create_rectangle(x - radio, y - radio, x + radio, y + radio, fill=color, tags="figura")
        elif tipo == "Círculo":
            id_canvas = self.canvas.create_oval(x - radio, y - radio, x + radio, y + radio, fill=color, tags="figura")
        elif tipo == "Triángulo":
            puntos = [x, y - radio, x - radio, y + radio, x + radio, y + radio]
            id_canvas = self.canvas.create_polygon(puntos, fill=color, tags="figura")

        # 2. Instanciar objeto de la capa 'módulos'
        figura_model = self.gestor.registrar_figura(id_canvas, tipo, x, y, tamano)

        # 3. Dibujar Texto e Identificadores de Puertos
        self.canvas.create_text(x, y, text=tipo, fill="white", font=("Arial", 9, "bold"), tags=f"txt_{id_canvas}")

        colores = {"A": "#E91E63", "B": "#00BCD4"}
        for nombre_p, puerto in figura_model.puertos.items():
            id_p = self.canvas.create_oval(
                puerto.x - 6, puerto.y - 6, puerto.x + 6, puerto.y + 6,
                fill=colores[nombre_p], tags="puerto"
            )
            self.canvas.create_text(puerto.x, puerto.y - 12, text=nombre_p,
                                    font=("Arial", 8, "bold"), tags=f"plabel_{id_canvas}")
            
            # Mapear el ID visual del puerto con el gestor lógico
            self.gestor.registrar_puerto(id_p, figura_model, nombre_p)

    def _vincular_eventos(self):
        self.canvas.tag_bind("figura", "<ButtonPress-1>", self._al_presionar_figura)
        self.canvas.tag_bind("figura", "<B1-Motion>", self._al_arrastrar_figura)
        self.canvas.tag_bind("figura", "<ButtonRelease-1>", lambda e: setattr(self, "figura_seleccionada_id", None))
        self.canvas.tag_bind("puerto", "<Button-1>", self._al_clic_puerto)

    def _al_presionar_figura(self, event):
        elementos = self.canvas.find_withtag("current")
        if elementos:
            self.figura_seleccionada_id = elementos[0]
            self.x_previo = event.x
            self.y_previo = event.y

    def _al_arrastrar_figura(self, event):
        if self.figura_seleccionada_id:
            dx = event.x - self.x_previo
            dy = event.y - self.y_previo
            fig_id = self.figura_seleccionada_id

            # Mover la representación visual en el Canvas
            self.canvas.move(fig_id, dx, dy)
            self.canvas.move(f"txt_{fig_id}", dx, dy)
            self.canvas.move(f"plabel_{fig_id}", dx, dy)

            figura_model = self.gestor.figuras[fig_id]
            for puerto in figura_model.puertos.values():
                self.canvas.move(puerto.id_canvas if hasattr(puerto, "id_canvas") else "puerto", 0, 0) # Mueve elementos agrupados por eventos

            # Mover el modelo de datos
            self.gestor.mover_figura(fig_id, dx, dy)

            # Mover también los puertos gráficos de esa figura
            for p in figura_model.puertos.values():
                # Encontrar el elemento del conector y moverlo
                pass

            # Redibujar las líneas de conexión
            self._actualizar_lineas_conexion()

            self.x_previo = event.x
            self.y_previo = event.y

    def _al_clic_puerto(self, event):
        elementos = self.canvas.find_withtag("current")
        if not elementos:
            return

        id_p = elementos[0]
        figura_model, nombre_puerto = self.gestor.puertos_map[id_p]

        if self.puerto_origen_temp is None:
            self.puerto_origen_temp = (figura_model, nombre_puerto)
        else:
            fig_orig, p_orig_nombre = self.puerto_origen_temp

            if fig_orig.id_figura == figura_model.id_figura:
                messagebox.showwarning("Atención", "No se puede conectar una figura consigo misma.")
                self.puerto_origen_temp = None
                return

            p_orig = fig_orig.puertos[p_orig_nombre]
            p_dest = figura_model.puertos[nombre_puerto]

            # Crear línea en Canvas
            id_linea = self.canvas.create_line(p_orig.x, p_orig.y, p_dest.x, p_dest.y, fill="#37474F", width=2, dash=(4, 2))
            self.canvas.tag_lower(id_linea)

            # Guardar en la capa de módulos
            self.gestor.agregar_conexion(fig_orig, p_orig_nombre, figura_model, nombre_puerto, id_linea)

            self.puerto_origen_temp = None
            self._refrescar_panel_estado()

    def _actualizar_lineas_conexion(self):
        for fig_orig, p_o, fig_dest, p_d, id_linea in self.gestor.conexiones:
            po = fig_orig.puertos[p_o]
            pd = fig_dest.puertos[p_d]
            self.canvas.coords(id_linea, po.x, po.y, pd.x, pd.y)

    def _refrescar_panel_estado(self):
        resumen = self.gestor.obtener_resumen_conexiones()
        texto = "\n".join(resumen) if resumen else "Sin conexiones."
        self.lbl_lista_conexiones.config(text=texto)