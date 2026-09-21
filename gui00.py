import tkinter as tk

# 1. Crear la ventana principal
ventana = tk.Tk()
ventana.title("Mi Primera Aplicación")
ventana.geometry("400x300")  # Ancho x Alto en píxeles
ventana.resizable(True, True) # Permite redimensionar (Ancho, Alto)

# 2. Iniciar el bucle de eventos (debe ir al final)
ventana.mainloop()