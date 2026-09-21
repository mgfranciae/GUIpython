import tkinter as tk

def procesar_entrada():
    texto = entry_datos.get()
    lbl_resultado.config(text=f"Ingresaste: {texto}")

ventana = tk.Tk()
ventana.title("Campos de Entrada")
ventana.geometry("300x180")

tk.Label(ventana, text="Escribe algo:").pack(pady=(10, 2))

entry_datos = tk.Entry(ventana, width=30)
entry_datos.pack(pady=5)

btn_guardar = tk.Button(ventana, text="Procesar", command=procesar_entrada)
btn_guardar.pack(pady=5)

lbl_resultado = tk.Label(ventana, text="", font=("Arial", 10, "bold"))
lbl_resultado.pack(pady=10)

ventana.mainloop()