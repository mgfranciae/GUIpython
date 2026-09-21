"""
Script independiente para inicializar la base de datos SQLite.
"""

import sqlite3


def inicializar_bd():
    conexion = sqlite3.connect("tabla_maestra.db")
    cursor = conexion.cursor()

    # 1. Crear la tabla maestra con categorías para días y meses
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tabla_maestra (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tipo TEXT NOT NULL,       -- 'DIA' o 'MES'
            nombre TEXT NOT NULL,     -- Nombre del día o mes
            orden INTEGER NOT NULL    -- Para ordenar cronológicamente
        )
    """)

    # Limpiar tabla para evitar duplicados al reejecutar
    cursor.execute("DELETE FROM tabla_maestra")

    # 2. Insertar Días de la semana
    dias = [
        ("DIA", "Lunes", 1), ("DIA", "Martes", 2), ("DIA", "Miércoles", 3),
        ("DIA", "Jueves", 4), ("DIA", "Viernes", 5), ("DIA", "Sábado", 6),
        ("DIA", "Domingo", 7)
    ]

    # 3. Insertar Meses del año
    meses = [
        ("MES", "Enero", 1), ("MES", "Febrero", 2), ("MES", "Marzo", 3),
        ("MES", "Abril", 4), ("MES", "Mayo", 5), ("MES", "Junio", 6),
        ("MES", "Julio", 7), ("MES", "Agosto", 8), ("MES", "Septiembre", 9),
        ("MES", "Octubre", 10), ("MES", "Noviembre", 11), ("MES", "Diciembre", 12)
    ]

    cursor.executemany("INSERT INTO tabla_maestra (tipo, nombre, orden) VALUES (?, ?, ?)", dias)
    cursor.executemany("INSERT INTO tabla_maestra (tipo, nombre, orden) VALUES (?, ?, ?)", meses)

    conexion.commit()
    conexion.close()
    print("Base de datos 'tabla_maestra.db' creada e inicializada con éxito.")


if __name__ == "__main__":
    inicializar_bd()