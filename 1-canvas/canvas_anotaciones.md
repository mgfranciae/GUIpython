# Manual de Referencia Completo: `tk.Canvas` en Tkinter / Python

El widget `tk.Canvas` (Lienzo) es uno de los componentes más versátiles de Tkinter. Permite dibujar formas geométricas, renderizar imágenes, trazar líneas, mostrar texto estructurado e incluso incrustar otros widgets de Tkinter en un espacio coordenado bidimensional $(X, Y)$.

---

## 1. Importación e Inicialización Básica

El origen de coordenadas $(0, 0)$ se encuentra en la **esquina superior izquierda** del lienzo. El eje $X$ crece hacia la derecha y el eje $Y$ crece hacia abajo.

```python
import tkinter as tk

root = tk.Tk()

# Declaración básica
canvas = tk.Canvas(root, width=600, height=400, bg="white")
canvas.pack(fill="both", expand=True)

root.mainloop()

```

---

## 2. Sintaxis y Parámetros del Constructor

```python
canvas = tk.Canvas(master, **opciones)

```

### Opciones Principales (`kw`)

| Opción | Tipo | Descripción |
| --- | --- | --- |
| `master` | Widget | Contenedor padre (ej. `Tk`, `Frame`). |
| `width` / `height` | `int` | Ancho y alto iniciales del lienzo en píxeles. |
| `bg` / `background` | `str` | Color de fondo del lienzo (ej. `"white"`, `"#212121"`). |
| `highlightthickness` | `int` | Ancho del borde de enfoque visual (poner en `0` para quitar bordes). |
| `scrollregion` | `tuple` | Región desplazable expresada como `(x1, y1, x2, y2)`. Utilizado para canvas con Barras de Desplazamiento (Scrollbars). |
| `cursor` | `str` | Apariencia del puntero al pasar sobre el canvas (ej. `"cross"`, `"hand2"`). |

---

## 3. Métodos de Dibujo de Formas (Creación)

Cada método de creación devuelve un **ID entero único** (`item_id`) que identifica al elemento dentro del lienzo.

| Método | Argumentos Coordenados | Descripción |
| --- | --- | --- |
| `.create_line()` | `x1, y1, x2, y2, ..., xn, yn` | Crea líneas de 2 o más puntos (polilíneas). |
| `.create_rectangle()` | `x1, y1, x2, y2` | Dibuja un rectángulo definido por dos esquinas opuestas. |
| `.create_oval()` | `x1, y1, x2, y2` | Dibuja una elipse o círculo inscrito en la caja delimitadora. |
| `.create_polygon()` | `x1, y1, x2, y2, ..., xn, yn` | Dibuja un polígono cerrado con $N$ vértices. |
| `.create_text()` | `x, y` | Inserta una cadena de texto centrada u orientada en $(x,y)$. |
| `.create_image()` | `x, y` | Muestra una imagen (`Photoimage`) anclada en la posición $(x,y)$. |
| `.create_window()` | `x, y` | Incrusta un widget real de Tkinter (botón, entry, etc.) dentro del canvas. |

---

## 4. Opciones de Estilizado para Elementos

| Opción | Formas Compatibles | Descripción |
| --- | --- | --- |
| `fill` | Todas | Color de relleno interno (o color de texto/línea). Usar `""` para transparente. |
| `outline` | Rectángulos, Ovalos, Polígonos | Color del borde exterior. |
| `width` | Líneas, Bordes de formas | Grosor del trazo en píxeles. |
| `dash` | Líneas, Bordes | Patrón de punteo. Ejemplo: `dash=(4, 2)` (4px línea, 2px espacio). |
| `tags` | Todas | Asigna etiquetas en texto para agrupar elementos (ej. `tags="enemigos"`). |
| `anchor` | Texto, Imágenes, Windows | Punto de anclaje relativo a la coordenada. Valores: `"center"`, `"n"`, `"nw"`, `"s"`, etc. |

---

## 5. Manipulación y Gestión de Objetos Dibujados

A diferencia de otros widgets, los elementos dentro del canvas **no son widgets independientes**, son objetos dibujados administrados por ID o etiqueta (`tag`).

```python
# 1. Mover un objeto dibujado (dx, dy son desplazamientos relativos)
canvas.move(item_id_o_tag, dx, dy)

# 2. Modificar coordenadas absolutas
canvas.coords(item_id_o_tag, x1, y1, x2, y2)

# 3. Cambiar propiedades visuales
canvas.itemconfig(item_id_o_tag, fill="red", outline="yellow")

# 4. Eliminar un elemento o grupo
canvas.delete(item_id_o_tag)   # Eliminar uno
canvas.delete("all")           # Limpiar todo el lienzo

# 5. Cambiar el orden Z (Profundidad)
canvas.tag_raise(item_id_o_tag)  # Mover al frente
canvas.tag_lower(item_id_o_tag)  # Mover al fondo

```

---

## 6. Manejo de Eventos en Objetos Específicos

Es posible capturar clics o movimiento del ratón sobre elementos concretos usando `.tag_bind()`:

```python
rect_id = canvas.create_rectangle(50, 50, 150, 150, fill="blue", tags="interactivo")

def al_hacer_clic(event):
    print("Se hizo clic sobre el rectángulo")

# Vincular evento por tag o por ID
canvas.tag_bind("interactivo", "<Button-1>", al_hacer_clic)

```

---

## ¿Es posible mostrar video dentro de un Canvas?

**Sí, es totalmente posible**, pero **Tkinter no incluye un reproductor de video nativo**.

Para lograrlo se debe decodificar el video fotograma por fotograma (usando librerías como `OpenCV` o `imageio`) y actualizar continuamente una imagen dentro del `Canvas` mediante un bucle de eventos.

### Ejemplo Completo: Reproducción de Video / Cámara con OpenCV y Canvas

```bash
pip install opencv-python pillow

```

```python
"""
Ejemplo de reproducción de video / Webcam dentro de un tk.Canvas
"""

import tkinter as tk
import cv2
from PIL import Image, ImageTk


class VideoCanvasApp:
    def __init__(self, root: tk.Tk, video_source=0):
        self.root = root
        self.root.title("Video en tk.Canvas")

        # 1. Abrir captura de video (0 para Webcam, o ruta a archivo 'video.mp4')
        self.cap = cv2.VideoCapture(video_source)

        # 2. Crear Canvas
        self.width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)) or 640
        self.height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)) or 480
        
        self.canvas = tk.Canvas(root, width=self.width, height=self.height, bg="black")
        self.canvas.pack()

        # Crear un contenedor de imagen inicial en el Canvas
        self.image_container = self.canvas.create_image(0, 0, anchor="nw")

        # Mantener referencia viva de la imagen para evitar que Garbage Collector la elimine
        self.photo = None

        # 3. Iniciar el bucle de actualización
        self.actualizar_fotograma()

    def actualizar_fotograma(self):
        ret, frame = self.cap.read()

        if ret:
            # OpenCV usa BGR, se debe convertir a RGB para PIL/Tkinter
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame_rgb)
            self.photo = ImageTk.PhotoImage(image=img)

            # Actualizar la imagen dentro del canvas sin recrear el objeto
            self.canvas.itemconfig(self.image_container, image=self.photo)

        # Programar la siguiente lectura (~30 FPS -> 33 milisegundos)
        self.root.after(33, self.actualizar_fotograma)

    def __del__(self):
        if hasattr(self, 'cap') and self.cap.isOpened():
            self.cap.release()


if __name__ == "__main__":
    root = tk.Tk()
    # Pasa 0 para la cámara web o "ruta/al/video.mp4"
    app = VideoCanvasApp(root, video_source=0)
    root.mainloop()

```

---

## 7. Errores Comunes con `tk.Canvas`

1. **Las imágenes no aparecen en pantalla:**
* **Causa:** El recolector de basura de Python (*Garbage Collector*) destruye las instancias de `PhotoImage` si no se mantiene una referencia explícita a ellas.
* **Solución:** Guarda la imagen en un atributo del objeto: `self.img = ImageTk.PhotoImage(...)`.


2. **Lentitud o parpadeo al mover muchos elementos:**
* **Causa:** Volver a crear formas dinámicamente con `.create_rectangle()` dentro de un bucle en lugar de reutilizar los IDs existentes.
* **Solución:** Usa `canvas.coords(item_id, ...)` o `canvas.move(item_id, ...)` para modificar posiciones de elementos ya creados.