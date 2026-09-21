import tkinter as tk

class CanvasArrastrable:
    def __init__(self, root):
        self.root = root
        self.root.title("Arrastrar Figuras en Canvas")
        self.root.geometry("650x450")

        # Variables para rastrear el elemento seleccionado y las coordenadas previas
        self.elemento_seleccionado = None
        self.x_previo = 0
        self.y_previo = 0

        self._crear_interfaz()
        self._vincular_eventos()

    def _crear_interfaz(self):
        # Panel superior de instrucciones
        lbl_info = tk.Label(
            self.root, 
            text="Haz clic sostenido sobre cualquier figura para moverla por el lienzo.",
            bg="#ECEFF1",
            font=("Arial", 10),
            pady=8
        )
        lbl_info.pack(fill="x")

        # Lienzo (Canvas)
        self.canvas = tk.Canvas(self.root, bg="#FFFFFF", highlightthickness=1, highlightbackground="#CCCCCC")
        self.canvas.pack(fill="both", expand=True, padx=10, pady=10)

        # Dibujar algunas figuras de prueba y asignarles el tag "móvil"
        # create_*(..., tags="movil") permite asociar eventos a todas las figuras
        self.canvas.create_rectangle(50, 50, 150, 150, fill="#2196F3", outline="black", tags="movil")
        self.canvas.create_oval(200, 80, 320, 200, fill="#F44336", outline="black", tags="movil")
        self.canvas.create_polygon(400, 180, 480, 60, 550, 180, fill="#4CAF50", outline="black", tags="movil")

    def _vincular_eventos(self):
        # Vincular eventos únicamente a las figuras que tengan la etiqueta "movil"
        self.canvas.tag_bind("movil", "<ButtonPress-1>", self._al_presionar)
        self.canvas.tag_bind("movil", "<B1-Motion>", self._al_arrastrar)
        self.canvas.tag_bind("movil", "<ButtonRelease-1>", self._al_soltar)

    def _al_presionar(self, event):
        """Se ejecuta al hacer clic sobre una figura con el tag 'movil'."""
        # Detectar el ID del objeto bajo el cursor de forma precisa
        elementos = self.canvas.find_withtag("current")
        if elementos:
            self.elemento_seleccionado = elementos[0]
            # Guardar la posición actual del cursor
            self.x_previo = event.x
            self.y_previo = event.y
            
            # Traer el objeto al frente en el orden visual (z-index)
            self.canvas.tag_raise(self.elemento_seleccionado)

    def _al_arrastrar(self, event):
        """Se ejecuta continuamente mientras se mueve el ratón con el clic presionado."""
        if self.elemento_seleccionado:
            # Calcular cuánto se ha movido el ratón desde el evento anterior
            dx = event.x - self.x_previo
            dy = event.y - self.y_previo

            # Mover la figura por el desplazamiento relativo (dx, dy)
            self.canvas.move(self.elemento_seleccionado, dx, dy)

            # Actualizar la posición previa para la siguiente iteración del evento
            self.x_previo = event.x
            self.y_previo = event.y

    def _al_soltar(self, event):
        """Se ejecuta al soltar el botón del ratón."""
        self.elemento_seleccionado = None


if __name__ == "__main__":
    root = tk.Tk()
    app = CanvasArrastrable(root)
    root.mainloop()