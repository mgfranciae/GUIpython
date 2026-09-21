
---

# Referencia Rápida de Tkinter

## 1. Estructura Mínima

```python
import tkinter as tk

root = tk.Tk()
root.title("Mi Aplicación")
root.geometry("400x300")  # Ancho x Alto

# --- Widgets y Lógica aquí ---

root.mainloop()

```

---

## 2. Widgets Principales

| Widget | Descripción | Ejemplo de Sintaxis |
| --- | --- | --- |
| **`Label`** | Muestra texto o imagen | `lbl = tk.Label(root, text="Hola", font=("Arial", 12))` |
| **`Button`** | Botón con acción | `btn = tk.Button(root, text="Clic", command=mi_funcion)` |
| **`Entry`** | Campo de texto de una línea | `txt = tk.Entry(root, width=20, show="*")` |
| **`Text`** | Caja de texto multilínea | `area = tk.Text(root, height=5, width=30)` |
| **`Frame`** | Contenedor de agrupación | `frame = tk.Frame(root, bg="lightgray", padding=10)` |
| **`Checkbutton`** | Casilla de verificación | `chk = tk.Checkbutton(root, text="Acepto", variable=var_bool)` |
| **`Radiobutton`** | Botón de opción única | `rb = tk.Radiobutton(root, text="Opción 1", value=1, variable=var_int)` |
| **`OptionMenu`** | Menú desplegable simple | `opt = tk.OptionMenu(root, var_str, "Opción 1", "Opción 2")` |

---

## 3. Gestores de Geometría (Posicionamiento)

### `.pack()` — Alineación Secuencial

* `side`: `"top"`, `"bottom"`, `"left"`, `"right"`
* `fill`: `"x"`, `"y"`, `"both"`, `"none"`
* `expand`: `True` / `False`
* `padx` / `pady`: Margen externo horizontal y vertical (píxeles)

```python
widget.pack(side="top", fill="x", padx=10, pady=5)

```

### `.grid()` — Filas y Columnas

* `row` / `column`: Índices numéricos (inician en `0`)
* `columnspan` / `rowspan`: Celdas que abarca el widget
* `sticky`: Alineación dentro de la celda (`"n"`, `"s"`, `"e"`, `"w"`, `"nsew"`)

```python
widget.grid(row=0, column=1, columnspan=2, sticky="ew", padx=5)

```

---

## 4. Métodos Indispensables de los Widgets

* **Leer valor:** `texto = entry.get()`
* **Insertar texto:** `entry.insert(0, "Texto inicial")`
* **Limpiar campo:** `entry.delete(0, tk.END)`
* **Modificar propiedad:** `widget.config(text="Nuevo Texto", state="disabled")`
* **Vincular evento:** `widget.bind("<Return>", funcion_handler)`

---

## 5. Variables de Control de Tkinter

Conectan automáticamente el estado de un widget con una variable en Python:

```python
var_str = tk.StringVar(value="Predeterminado")
var_int = tk.IntVar(value=0)
var_bool = tk.BooleanVar(value=True)

# Asignación en un widget:
entry = tk.Entry(root, textvariable=var_str)

# Métodos:
valor = var_str.get()  # Leer
var_str.set("Nuevo")   # Modificar

```

---

## 6. Cuadros de Diálogo (`messagebox` y `filedialog`)

```python
from tkinter import filedialog, messagebox

# Mensajes de alerta
messagebox.showinfo("Título", "Mensaje informativo")
messagebox.showwarning("Advertencia", "Cuidado con este dato")
messagebox.showerror("Error", "Ocurrió un fallo")
respuesta = messagebox.askyesno("Confirmar", "¿Deseas continuar?")  # Retorna True/False

# Diálogos de archivo
ruta_abrir = filedialog.askopenfilename(filetypes=[("Archivos Python", "*.py")])
ruta_guardar = filedialog.asksaveasfilename(defaultextension=".txt")

```

---

## 7. Menú Superior (Barra de Menús)

```python
barra_menu = tk.Menu(root)

# Submenú Archivo
menu_archivo = tk.Menu(barra_menu, tearoff=0)
menu_archivo.add_command(label="Nuevo", command=funcion_nuevo)
menu_archivo.add_separator()
menu_archivo.add_command(label="Salir", command=root.quit)

# Agregar submenú a la barra
barra_menu.add_cascade(label="Archivo", menu=menu_archivo)

# Asignar a la ventana principal
root.config(menu=barra_menu)

```

---

## 8. Eventos Comunes para `.bind()`

| Secuencia | Evento desencadenante |
| --- | --- |
| `<Button-1>` | Clic con el botón izquierdo del ratón. |
| `<Button-3>` | Clic con el botón derecho del ratón. |
| `<Return>` | Presionar la tecla Enter. |
| `<Key>` | Presionar cualquier tecla. |
| `<Configure>` | Redimensionar o mover la ventana. |