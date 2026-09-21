import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk


def cargar_imagen():
    # 1. Seleccionar la ruta del archivo de imagen
    ruta_imagen = filedialog.askopenfilename(
        title="Seleccionar una imagen",
        filetypes=[
            ("Imágenes", "*.png *.jpg *.jpeg *.bmp *.gif *.webp"),
            ("Todos los archivos", "*.*")
        ]
    )

    # 2. Si el usuario seleccionó una imagen (no canceló)
    if ruta_imagen:
        try:
            # Abrir la imagen con Pillow
            imagen_original = Image.open(ruta_imagen)

            # Redimensionar la imagen manteniendo la proporción (Ancho x Alto máximo)
            imagen_original.thumbnail((350, 300))

            # Convertir la imagen de Pillow a un objeto compatible con Tkinter
            imagen_tk = ImageTk.PhotoImage(imagen_original)

            # Actualizar el Label con la nueva imagen
            lbl_imagen.config(image=imagen_tk, text="")
            
            # ¡CRUCIAL! Guardar una referencia de la imagen para evitar que 
            # el recolector de basura de Python la elimine de la memoria
            lbl_imagen.image = imagen_tk

            lbl_estado.config(text=f"Cargado: {ruta_imagen}", fg="green")

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar la imagen:\n{e}")


# --- Ventana Principal ---
root = tk.Tk()
root.title("Visor de Imágenes con filedialog")
root.geometry("400x420")

# Botón para activar el filedialog
btn_cargar = tk.Button(
    root,
    text="Cargar Imagen",
    command=cargar_imagen,
    bg="#4CAF50",
    fg="white",
    font=("Arial", 10, "bold")
)
btn_cargar.pack(pady=10)

# Label para mostrar información del archivo
lbl_estado = tk.Label(root, text="Ninguna imagen cargada", font=("Arial", 9, "italic"))
lbl_estado.pack(pady=2)

# Label que servirá de contenedor para mostrar la imagen
lbl_imagen = tk.Label(
    root, 
    text="[ Aquí se mostrará la imagen ]", 
    bg="#E0E0E0", 
    width=40, 
    height=15
)
lbl_imagen.pack(fill="both", expand=True, padx=20, pady=10)

root.mainloop()