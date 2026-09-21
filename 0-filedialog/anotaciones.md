# Referencia Rápida: `filedialog` y `Pillow` en Tkinter

---

## 1. Módulo `filedialog` (Selección de Archivos)

El submódulo `tkinter.filedialog` proporciona diálogos nativos del sistema operativo para abrir y guardar archivos o directorios.

### Importación

```python
from tkinter import filedialog

```

### Funciones Principales

| Función | Descripción | Retorno |
| --- | --- | --- |
| **`askopenfilename(**opciones)`** | Abre el explorador para **seleccionar un archivo**. | `str` (Ruta absoluta) o `""` (Si cancela) |
| **`askopenfilenames(**opciones)`** | Permite seleccionar **múltiples archivos**. | `tuple` de rutas |
| **`asksaveasfilename(**opciones)`** | Muestra el diálogo para **guardar un archivo**. | `str` (Ruta destino) o `""` |
| **`askdirectory(**opciones)`** | Abre la búsqueda para **seleccionar una carpeta**. | `str` (Ruta de la carpeta) |

### Parámetros Frecuentes

* `title="Texto"`: Título de la ventana emergente.
* `filetypes=[("Etiqueta", "*.ext1 *.ext2"), ...]`: Filtro de extensiones visibles.
* `initialdir="/ruta/inicial"`: Carpeta por defecto al abrir el explorador.
* `defaultextension=".txt"`: Extensión por defecto para diálogos de guardado.

---

## 2. Librería `Pillow` (PIL)

Librería para lectura, procesamiento y conversión de formatos de imagen (`JPG`, `PNG`, `WEBP`, `BMP`, etc.).

### Instalación e Importación

```bash
pip install Pillow

```

```python
from PIL import Image, ImageTk

```

### Métodos Clave de `Image` e `ImageTk`

```python
# 1. Abrir imagen desde ruta
imagen_pil = Image.open("ruta/imagen.jpg")

# 2. Redimensionar de forma proporcional (Ancho max, Alto max)
imagen_pil.thumbnail((400, 300))

# 3. Redimensionar a tamaño exacto (fuerza dimensiones)
imagen_pil = imagen_pil.resize((200, 200))

# 4. Convertir a formato compatible con Tkinter
imagen_tk = ImageTk.PhotoImage(imagen_pil)

```

---

## 3. Uso de `Label` como "Canvas" para Imágenes

Tkinter no requiere obligatoriamente el widget `Canvas` para renderizar imágenes estáticas. Un widget **`Label`** actúa como un marco o contenedor simplificado para este fin.

### ¿Cómo funciona?

1. **Reemplazo de contenido:** Un `Label` puede contener texto (`text`), una imagen (`image`) o ambos a la vez (usando la propiedad `compound`).
2. **Carga inicial:** Se asigna el objeto `ImageTk.PhotoImage` mediante el parámetro `image`:
```python
lbl_visor.config(image=imagen_tk, text="")

```



### ⚠️ El Recolector de Basura (*Garbage Collection*)

Python elimina automáticamente de la memoria RAM cualquier variable local cuando una función termina su ejecución. Si la imagen asignada a un `Label` no tiene una referencia global o persistente, **desaparecerá de la interfaz dejando el marco en blanco**.

**Solución:** Guardar una referencia directamente dentro del objeto del widget:

```python
# Guardar la referencia en la misma propiedad del Label
lbl_visor.image = imagen_tk

```

---

## 4. Patrones de Código de Referencia

### Patrón A: Cargar Archivo de Texto en `Text`

```python
from tkinter import filedialog, END

ruta = filedialog.askopenfilename(filetypes=[("Archivos TXT", "*.txt")])

if ruta:
    with open(ruta, "r", encoding="utf-8") as f:
        contenido = f.read()
    
    widget_text.delete("1.0", END)
    widget_text.insert(END, contenido)

```

### Patrón B: Cargar e Ilustrar Imagen en `Label`

```python
from tkinter import filedialog
from PIL import Image, ImageTk

ruta = filedialog.askopenfilename(filetypes=[("Imágenes", "*.png *.jpg *.jpeg")])

if ruta:
    img = Image.open(ruta)
    img.thumbnail((300, 300))  # Ajuste proporcional
    
    img_tk = ImageTk.PhotoImage(img)
    
    lbl_imagen.config(image=img_tk, text="")
    lbl_imagen.image = img_tk   # Previene la eliminación de memoria

```