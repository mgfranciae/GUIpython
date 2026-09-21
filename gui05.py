import tkinter as tk
from tkinter import messagebox

def nuevo_archivo():
    messagebox.showinfo("Menú", "Creando nuevo archivo...")

def salir():
    ventana.quit()

ventana = tk.Tk()
ventana.title("Aplicación con Menú")
ventana.geometry("400x300")

# 1. Crear la barra de menú principal
barra_menu = tk.Menu(ventana)

# 2. Crear el menú desplegable "Archivo"
menu_archivo = tk.Menu(barra_menu, tearoff=0) # tearoff=0 quita la línea punteada por defecto
menu_archivo.add_command(label="Nuevo", command=nuevo_archivo)
menu_archivo.add_separator()  # Línea divisoria
menu_archivo.add_command(label="Salir", command=salir)

# 3. Crear el menú desplegable "Ayuda"
menu_ayuda = tk.Menu(barra_menu, tearoff=0)
menu_ayuda.add_command(label="Acerca de", command=lambda: messagebox.showinfo("Acerca de", "Guía Tkinter v1.0"))

# 4. Agregar los menús a la barra principal
barra_menu.add_cascade(label="Archivo", menu=menu_archivo)
barra_menu.add_cascade(label="Ayuda", menu=menu_ayuda)

# 5. Asignar la barra de menú a la ventana
ventana.config(menu=barra_menu)

ventana.mainloop()