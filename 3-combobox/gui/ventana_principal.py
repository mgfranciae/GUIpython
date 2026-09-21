"""
Interfaz gráfica con dos desplegables (Dropdown / Combobox).
"""

import tkinter as tk
from tkinter import ttk
from modulos.base_datos import RepositorioMaestro


class VentanaPrincipalGUI:
    """Representa la vista de la aplicación."""

    def __init__(self, root: tk.Tk, repo_datos: RepositorioMaestro):
        self.root = root
        self.repo = repo_datos

        self.root.title("Carga de Selects desde SQLite")
        self.root.geometry("400x250")
        self.root.resizable(False, False)

        self._construir_widgets()
        self.cargar_datos_selects()

    def _construir_widgets(self):
        frame = ttk.LabelFrame(self.root, text=" Selección de Parámetros ", padding=15)
        frame.pack(fill="both", expand=True, padx=15, pady=15)

        # --- Dropdown 1: Días ---
        ttk.Label(frame, text="Día de la semana:").grid(row=0, column=0, sticky="w", pady=5)
        self.combo_dias = ttk.Combobox(frame, state="readonly", width=25)
        self.combo_dias.grid(row=0, column=1, pady=5, padx=5)

        # --- Dropdown 2: Meses ---
        ttk.Label(frame, text="Mes del año:").grid(row=1, column=0, sticky="w", pady=5)
        self.combo_meses = ttk.Combobox(frame, state="readonly", width=25)
        self.combo_meses.grid(row=1, column=1, pady=5, padx=5)

        # Botón para confirmar la selección
        btn_confirmar = ttk.Button(frame, text="Mostrar Selección", command=self._mostrar_seleccion)
        btn_confirmar.grid(row=2, column=0, columnspan=2, pady=15)

        # Etiqueta de resultado
        self.lbl_resultado = ttk.Label(frame, text="Selección: N/A", font=("Arial", 9, "bold"))
        self.lbl_resultado.grid(row=3, column=0, columnspan=2, pady=5)

    def cargar_datos_selects(self):
        """Pide los datos al módulo y los asigna a las listas desplegables."""
        dias = self.repo.obtener_dias()
        meses = self.repo.obtener_meses()

        # Asignar valores a los Combobox
        self.combo_dias['values'] = dias
        self.combo_meses['values'] = meses

        # Seleccionar el primer valor por defecto si existen datos
        if dias:
            self.combo_dias.current(0)
        if meses:
            self.combo_meses.current(0)

    def _mostrar_seleccion(self):
        dia = self.combo_dias.get()
        mes = self.combo_meses.get()
        self.lbl_resultado.config(text=f"Selección: {dia} de {mes}")