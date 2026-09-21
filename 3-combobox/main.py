"""
Punto de entrada u orquestador principal del proyecto.
"""

import os
import tkinter as tk
from modulos.base_datos import RepositorioMaestro
from gui.ventana_principal import VentanaPrincipalGUI


def main():
    db_filename = "tabla_maestra.db"

    # Validar que exista la base de datos antes de iniciar
    if not os.path.exists(db_filename):
        print(f"Error: No se encontró '{db_filename}'. Ejecuta 'python crear_db.py' primero.")
        return

    # 1. Instanciar la base de datos (Modelo)
    repo = RepositorioMaestro(db_filename)

    # 2. Inicializar el contenedor gráfico de Tkinter
    root = tk.Tk()

    # 3. Orquestar pasando la base de datos a la interfaz (Inyección de Dependencias)
    app = VentanaPrincipalGUI(root, repo)

    # 4. Iniciar bucle de eventos
    root.mainloop()


if __name__ == "__main__":
    main()