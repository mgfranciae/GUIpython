import tkinter as tk

ventana = tk.Tk()
ventana.title("Formulario con Grid")
ventana.geometry("280x120")

# Fila 0: Usuario
tk.Label(ventana, text="Usuario:").grid(row=0, column=0, padx=10, pady=10, sticky="e")
entry_user = tk.Entry(ventana)
entry_user.grid(row=0, column=1, padx=10, pady=10)

# Fila 1: Clave
tk.Label(ventana, text="Contraseña:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
entry_pass = tk.Entry(ventana, show="*")
entry_pass.grid(row=1, column=1, padx=10, pady=5)

# Fila 2: Botón que abarca 2 columnas
btn_login = tk.Button(ventana, text="Iniciar Sesión")
btn_login.grid(row=2, column=0, columnspan=2, pady=10)

ventana.mainloop()