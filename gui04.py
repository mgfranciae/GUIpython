import tkinter as tk

ventana = tk.Tk()
ventana.title("Uso de Frames")
ventana.geometry("300x200")

# Panel Superior
frame_superior = tk.Frame(ventana, bg="#E0E0E0", pady=10) if hasattr(tk, 'Frame') else tk.Frame(ventana, bg="#E0E0E0")
frame_superior.pack(fill="x", padx=5, pady=5)

tk.Label(frame_superior, text="Panel de Control", bg="#E0E0E0").pack()
tk.Button(frame_superior, text="Acción 1").pack(side="left", padx=5, pady=5)
tk.Button(frame_superior, text="Acción 2").pack(side="left", padx=5, pady=5)

# Panel Inferior
frame_inferior = tk.Frame(ventana, bg="#FAFAFA")
frame_inferior.pack(fill="both", expand=True, padx=5, pady=5)

tk.Label(frame_inferior, text="Área de contenido o resultados", bg="#FAFAFA").pack(pady=20)

ventana.mainloop()