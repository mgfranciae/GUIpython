"""
Módulo para consultar la base de datos tabla_maestra.db.
"""

import sqlite3


class RepositorioMaestro:
    """Maneja las consultas SQL hacia la tabla maestra."""

    def __init__(self, ruta_db: str = "tabla_maestra.db"):
        self.ruta_db = ruta_db

    def _obtener_conexion(self):
        return sqlite3.connect(self.ruta_db)

    def obtener_dias(self) -> list[str]:
        """Extrae los nombres de los días ordenados cronológicamente."""
        with self._obtener_conexion() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT nombre FROM tabla_maestra WHERE tipo = 'DIA' ORDER BY orden ASC"
            )
            # Extraer los elementos de las tuplas resultantes
            return [registro[0] for registro in cursor.fetchall()]

    def obtener_meses(self) -> list[str]:
        """Extrae los nombres de los meses ordenados cronológicamente."""
        with self._obtener_conexion() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT nombre FROM tabla_maestra WHERE tipo = 'MES' ORDER BY orden ASC"
            )
            return [registro[0] for registro in cursor.fetchall()]