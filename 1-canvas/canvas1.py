import math
import tkinter as tk


def dibujar_senoidal():
    # 1. Limpiar el lienzo antes de redibujar
    canvas.delete("all")

    # 2. Obtener dimensiones del Canvas
    ancho = canvas.winfo_width()
    alto = canvas.winfo_height()

    # Si la ventana aún no se ha dibujado del todo, usar valores por defecto
    if ancho <= 1:
        ancho, alto = 600, 400

    origen_x = 50
    origen_y = alto // 2

    # 3. Dibujar ejes cartesianos (Eje X y Eje Y)
    # create_line(x1, y1, x2, y2, **opciones)
    canvas.create_line(20, origen_y, ancho - 20, origen_y, fill="#888888", width=2, arrow=tk.LAST)  # Eje X
    canvas.create_line(origen_x, alto - 20, origen_x, 20, fill="#888888", width=2, arrow=tk.LAST)   # Eje Y

    # Etiquetas de los ejes
    canvas.create_text(ancho - 30, origen_y + 15, text="t (tiempo)", fill="#555555", font=("Arial", 9))
    canvas.create_text(origen_x - 15, 25, text="V (amplitud)", fill="#555555", font=("Arial", 9))

    # 4. Parámetros de la señal senoidal
    amplitud = 100        # Altura en píxeles
    frecuencia = 0.03     # Ajuste de velocidad angular/escala en X
    fase = 0              # Desfase inicial en radianes

    puntos = []

    # 5. Generar la lista de coordenadas (x, y)
    for x_pixel in range(origen_x, ancho - 40):
        # Convertir coordenada X del pixel a ángulo t
        t = (x_pixel - origen_x) * frecuencia
        
        # Invertimos el eje Y porque en Canvas el origen (0,0) está arriba
        y_pixel = origen_y - (amplitud * math.sin(t + fase))
        
        puntos.append(x_pixel)
        puntos.append(y_pixel)

    # 6. Dibujar la línea continua que une todos los puntos
    # create_line acepta la lista de puntos extendida [x1, y1, x2, y2, ..., xN, yN]
    if len(puntos) >= 4:
        canvas.create_line(puntos, fill="#2196F3", width=2, smooth=True)


# --- Ventana Principal ---
root = tk.Tk()
root.title("Generador de Señal Senoidal en Canvas")
root.geometry("650x480")

# Panel superior de controles
frame_controles = tk.Frame(root, bg="#ECEFF1", pady=10)
frame_controles.pack(fill="x")

btn_dibujar = tk.Button(
    frame_controles,
    text="Graficar Señal Senoidal",
    command=dibujar_senoidal,
    bg="#4CAF50",
    fg="white",
    font=("Arial", 10, "bold")
)
btn_dibujar.pack()

# Widget Canvas para la gráfica
canvas = tk.Canvas(root, bg="#FFFFFF", highlightthickness=1, highlightbackground="#CCCCCC")
canvas.pack(fill="both", expand=True, padx=15, pady=15)

root.mainloop()