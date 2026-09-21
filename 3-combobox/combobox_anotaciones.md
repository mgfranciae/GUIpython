# Manual de Referencia Completo: `ttk.Combobox` en Tkinter / Python

El widget `ttk.Combobox` combina una caja de texto con un menú desplegable, permitiendo al usuario seleccionar una opción de una lista predefinida o escribir un valor personalizado. Pertenece al módulo `tkinter.ttk` (Themed Tkinter).

---

## 1. Importación e Inicialización Básico

```python
import tkinter as tk
from tkinter import ttk

root = tk.Tk()

# Declaración básica
combo = ttk.Combobox(root)
combo.pack()

root.mainloop()

```

---

## 2. Sintaxis y Parámetros del Constructor

```python
combo = ttk.Combobox(master, **opciones)

```

### Opciones Principales (`kw`)

| Opción | Tipo | Descripción |
| --- | --- | --- |
| `master` | Widget | Contenedor padre (ej. `Tk`, `Frame`, `LabelFrame`). |
| `values` | `list` / `tuple` | Lista de cadenas de texto que se mostrarán en la lista desplegable. |
| `state` | `str` | Estado del widget: `'normal'` (permite escribir o elegir), `'readonly'` (solo permite seleccionar), `'disabled'` (desactivado). |
| `textvariable` | `tk.StringVar` | Variable de control para sincronizar el texto seleccionado con una variable de Python. |
| `width` | `int` | Ancho del widget medido en número de caracteres. |
| `height` | `int` | Número máximo de filas visibles en el menú desplegable (por defecto suele ser 10). |
| `justify` | `str` | Alineación del texto en la caja: `'left'`, `'center'`, `'right'`. |
| `font` | `tuple` / `str` | Fuente del texto principal. Ejemplo: `("Arial", 10, "bold")`. |

---

## 3. Métodos Principales

| Método | Descripción | Ejemplo de Uso |
| --- | --- | --- |
| `.get()` | Devuelve el valor actual seleccionado o digitado como `str`. | `texto = combo.get()` |
| `.set(valor)` | Asigna un valor directo a la caja de texto. | `combo.set("Lunes")` |
| `.current(index)` | Selecciona la opción en la posición `index` de `values`. Si se pasa sin argumentos, devuelve el índice de la opción seleccionada (-1 si no coincide). | `combo.current(0)` |
| `['values'] = lista` | Actualiza dinámicamente la lista de opciones. | `combo['values'] = ["A", "B", "C"]` |
| `.config(**opciones)` | Permite modificar opciones después de crear el widget. | `combo.config(state="readonly")` |
| `.selection_clear()` | Limpia cualquier selección de texto dentro de la caja de texto. | `combo.selection_clear()` |

---

## 4. Eventos Virtuales

El evento más importante del `ttk.Combobox` es `<<ComboboxSelected>>`, el cual se dispara **únicamente cuando el usuario selecciona una opción de la lista desplegable** (no cuando escribe manualmente).

### Enlace de Evento (`.bind()`)

```python
def al_seleccionar(event):
    # 'event.widget' hace referencia al combobox que disparó el evento
    valor = event.widget.get()
    print(f"Opción seleccionada: {valor}")

combo.bind("<<ComboboxSelected>>", al_seleccionar)

```

---

## 5. Recetario de Casos de Uso Comunes

### Caso 1: Forzar Selección Única (`state='readonly'`)

Evita que el usuario escriba valores aleatorios en el campo de texto.

```python
combo = ttk.Combobox(root, values=["Opción 1", "Opción 2"], state="readonly")
combo.current(0)  # Establecer la primera opción por defecto

```

---

### Caso 2: Uso con `tk.StringVar`

Permite conectar el valor del widget a una variable observable.

```python
var_seleccion = tk.StringVar()

combo = ttk.Combobox(root, textvariable=var_seleccion, values=["A", "B", "C"])
combo.pack()

# Capturar el cambio a través de la variable
def responder_cambio(*args):
    print("Nuevo valor:", var_seleccion.get())

var_seleccion.trace_add("write", responder_cambio)

```

---

### Caso 3: Manejo de Claves y Valores (IDs)

Tkinter muestra cadenas de texto en los Comboboxes. Si necesitas trabajar con un ID interno (ej. `id_categoria`), se mapea mediante diccionarios o listas paralelas:

```python
# Mapeo de datos: {Nombre_Visibilidad: ID_BD}
categorias = {
    "Electrónica": 101,
    "Hogar": 102,
    "Ferretería": 103
}

combo = ttk.Combobox(root, values=list(categorias.keys()), state="readonly")
combo.pack()

def obtener_id_seleccionado(event):
    nombre = combo.get()
    id_bd = categorias.get(nombre)
    print(f"Nombre visual: {nombre} | ID BD: {id_bd}")

combo.bind("<<ComboboxSelected>>", obtener_id_seleccionado)

```

---

### Caso 4: Estilizado con `ttk.Style`

Los widgets `ttk` no aceptan argumentos tradicionales como `bg` o `fg` directamente en su constructor. Se modifican usando estilos:

```python
style = ttk.Style()

# Modificar la fuente y colores de todos los Comboboxes
style.configure("TCombobox", 
                font=("Segoe UI", 10),
                padding=5)

# Cambiar color de fondo de la lista desplegable emergente (TCombobox*Listbox)
root.option_add('*TCombobox*Listbox.font', ("Segoe UI", 10))
root.option_add('*TCombobox*Listbox.selectBackground', '#2196F3')
root.option_add('*TCombobox*Listbox.selectForeground', 'white')

```

---

## 6. Manejo de Errores Comunes

1. **`combo.get()` devuelve cadena vacía `""`:**
* Ocurre si la propiedad `values` no ha sido inicializada y no hay texto ingresado.
* **Solución:** Validar con `if not combo.get():` antes de procesar el dato.


2. **`combo.current()` lanza `tk.TclError`:**
* Ocurre cuando se pasa un índice fuera de rango o cuando la lista `values` está vacía.
* **Solución:** Verificar `if combo['values']:` antes de invocar `.current()`.


3. **El evento `<<ComboboxSelected>>` no detecta escritura manual:**
* Es el comportamiento por diseño. Para capturar la escritura manual tecla a tecla, vincula el evento `<KeyRelease>` o usa un `.trace_add()` sobre un `StringVar`.