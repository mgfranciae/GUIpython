import tkinter as tk
from tkinter import messagebox


def dibujar_figura():
    # 1. Limpiar lienzo previo
    canvas.delete("all")

    # 2. Obtener dimensiones y centro del Canvas
    ancho = canvas.winfo_width()
    alto = canvas.winfo_height()

    if ancho <= 1:
        ancho, alto = 500, 400

    centro_x = ancho // 2
    centro_y = alto // 2

    # 3. Leer configuraciones de la interfaz
    figura = var_figura.get()
    color_relleno = var_color.get()
    
    try:
        tamano = int(entry_tamano.get())
    except ValueError:
        messagebox.showerror("Error de entrada", "Por favor, ingresa un tamaño numérico válido.")
        return

    radio = tamano // 2

    # 4. Trazar la figura seleccionada
    if figura == "Rectángulo":
        # create_rectangle(x1, y1, x2, y2, **opciones)
        canvas.create_rectangle(
            centro_x - radio, centro_y - radio,
            centro_x + radio, centro_y + radio,
            fill=color_relleno, outline="black", width=2
        )

    elif figura == "Círculo / Elipse":
        # create_oval(x1, y1, x2, y2, **opciones) -> Define el rectángulo delimitador
        canvas.create_oval(
            centro_x - radio, centro_y - radio,
            centro_x + radio, centro_y + radio,
            fill=color_relleno, outline="black", width=2
        )

    elif figura == "Triángulo":
        # create_polygon(x1, y1, x2, y2, x3, y3, ..., **opciones)
        p1 = (centro_x, centro_y - radio)         # Vértice superior
        p2 = (centro_x - radio, centro_y + radio) # Vértice inferior izquierdo
        p3 = (centro_x + radio, centro_y + radio) # Vértice inferior derecho
        
        canvas.create_polygon(
            p1, p2, p3,
            fill=color_relleno, outline="black", width=2
        )

    elif figura == "Estrella":
        # Polígono personalizado de 5 puntas
        puntos = [
            centro_x, centro_y - radio,
            centro_x + (radio * 0.3), centro_y - (radio * 0.3),
            centro_x + radio, centro_y - (radio * 0.3),
            centro_x + (radio * 0.4), centro_y + (radio * 0.1),
            centro_x + (radio * 0.6), centro_y + radio,
            centro_x, centro_y + (radio * 0.4),
            centro_x - (radio * 0.6), centro_y + radio,
            centro_x - (radio * 0.4), centro_y + (radio * 0.1),
            centro_x - radio, centro_y - (radio * 0.3),
            centro_x - (radio * 0.3), centro_y - (radio * 0.3)
        ]
        canvas.create_polygon(puntos, fill=color_relleno, outline="black", width=2)

    # Etiqueta de coordenadas de referencia
    canvas.create_text(
        10, 10, anchor="nw", 
        text=f"Centro: ({centro_x}, {centro_y}) | Tamaño: {tamano}px", 
        fill="#666666", font=("Arial", 9)
    )


# --- Ventana Principal ---
root = tk.Tk()
root.title("Trazado de Figuras Geométricas")
root.geometry("650x450")

# Panel lateral izquierdo (Controles)
frame_panel = tk.Frame(root, bg="#F0F0F0", width=180, pady=10) if hasattr(tk, 'Frame') else tk.Frame(root, bg="#F0F0F0", width=180)
frame_panel.pack(side="left", fill="y", padx=5, pady=5)

# Selección de Figura
tk.Label(frame_panel, text="Figura Geometrica:", bg="#F0F0F0", font=("Arial", 9, "bold")).pack(anchor="w", pady=(5, 2))
var_figura = tk.StringVar(value="Rectángulo")
opciones_figuras = ["Rectángulo", "Círculo / Elipse", "Triángulo", "Estrella"]
menu_figuras = tk.OptionMenu(frame_panel, var_figura, *opciones_figuras)
menu_figuras.pack(fill="x", pady=5)

# Selección de Color
tk.Label(frame_panel, text="Color de Relleno:", bg="#F0F0F0", font=("Arial", 9, "bold")).pack(anchor="w", pady=(10, 2))
var_color = tk.StringVar(value="#2196F3")
rb_colores = [("Azul", "#2196F3"), ("Rojo", "#F44336"), ("Verde", "#4CAF50"), ("Amarillo", "#FFEB3B")]

for texto, hex_val in rb_colores:
    tk.Radiobutton(frame_panel, text=texto, value=hex_val, variable=var_color, bg="#F0F0F0").pack(anchor="w")

# Entrada de Tamaño
tk.Label(frame_panel, text="Tamaño (píxeles):", bg="#F0F0F0", font=("Arial", 9, "bold")).pack(anchor="w", pady=(10, 2))
entry_tamano = tk.Entry(frame_panel)
entry_tamano.insert(0, "150")
entry_tamano.pack(fill="x", pady=5)

# Botón Dibujar
btn_dibujar = tk.Button(
    frame_panel, 
    text="Dibujar Figura", 
    command=dibujar_figura, 
    bg="#3F51B5", 
    fg="white", 
    font=("Arial", 10, "bold")
)
btn_dibujar.pack(fill="x", pady=20)

# Lienzo para gráficos (Canvas)
canvas = tk.Canvas(root, bg="#FFFFFF", highlightthickness=1, highlightbackground="#CCCCCC")
canvas.pack(side="right", fill="both", expand=True, padx=5, pady=5)

root.mainloop()