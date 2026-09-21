import tkinter as tk

def cambiar_texto():
    lbl_mensaje.config(text="¡Hiciste clic en el botón!")

ventana = tk.Tk()
ventana.title("Etiquetas y Botones")
ventana.geometry("350x150")

# Label
lbl_mensaje = tk.Label(ventana, text="Estado: Esperando acción", font=("Arial", 11))
lbl_mensaje.pack(pady=15)

# Botón
btn_accion = tk.Button(ventana, text="Presióname", command=cambiar_texto, bg="#2196F3", fg="white")
btn_accion.pack(pady=5)

ventana.mainloop()