"""
Punto de Entrada Principal (Orquestador)
"""

import tkinter as tk
from modulos.conector_logica import GestorDiagrama
from gui.canvas_view import AplicacionesCanvasGUI


def main():
    # 1. Crear la ventana principal de Tkinter
    root = tk.Tk()

    # 2. Instanciar la lógica de negocio (Modulo)
    gestor_logica = GestorDiagrama()

    # 3. Instanciar la interfaz pasando la lógica por inyección de dependencias
    app_gui = AplicacionesCanvasGUI(root, gestor_logica)

    # 4. Orquestar la creación de datos iniciales a través de la GUI
    app_gui.crear_figura_grafica("Rectángulo", 150, 200, 50, "#2196F3")
    app_gui.crear_figura_grafica("Círculo", 400, 200, 45, "#F44336")
    app_gui.crear_figura_grafica("Triángulo", 650, 200, 50, "#4CAF50")

    # 5. Ejecutar el bucle de eventos
    root.mainloop()


if __name__ == "__main__":
    main()