import tkinter as tk
from tkinter import filedialog, messagebox


def cargar_archivo():
    # Abre el cuadro de diálogo para seleccionar el archivo
    ruta_archivo = filedialog.askopenfilename(
        title="Seleccionar archivo de texto",
        filetypes=[("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")]
    )
    
    # Si el usuario seleccionó un archivo (no canceló)
    if ruta_archivo:
        try:
            with open(ruta_archivo, "r", encoding="utf-8") as archivo:
                contenido = archivo.read()
                
            # Limpiar el widget Text y colocar el nuevo contenido
            area_texto.delete("1.0", tk.END)
            area_texto.insert(tk.END, contenido)
            
            lbl_estado.config(text=f"Cargado: {ruta_archivo}", fg="green")
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo leer el archivo:\n{e}")


# 1. Ventana principal
root = tk.Tk()
root.title("Cargar datos.txt con filedialog")
root.geometry("450x350")

# 2. Botón para activar el filedialog
btn_cargar = tk.Button(
    root, 
    text="Cargar archivo (.txt)", 
    command=cargar_archivo,
    bg="#2196F3", 
    fg="white", 
    font=("Arial", 10, "bold")
)
btn_cargar.pack(pady=10)

# 3. Label de estado
lbl_estado = tk.Label(root, text="Ningún archivo cargado", font=("Arial", 9, "italic"))
lbl_estado.pack(pady=2)

# 4. Widget Text donde se mostrará el contenido
area_texto = tk.Text(root, wrap="word", font=("Consolas", 10))
area_texto.pack(fill="both", expand=True, padx=10, pady=10)

# 5. Iniciar la aplicación
root.mainloop()