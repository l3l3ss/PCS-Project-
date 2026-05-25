# Presentación del Proyecto: Caos Cuántico en Billares

Este directorio contiene los archivos para crear y visualizar una presentación global en **Manim Slides**. Para que puedan colaborar en ramas separadas, la presentación ha sido dividida en diferentes módulos que son importados desde un único archivo principal.

## Estructura de archivos

* `main_presentation.py`: Es el archivo principal que compila toda la presentación. Contiene la clase principal `PresentacionGeneral`.
* `parte1_juego_billar.py`: Lógica y animaciones del juego de billar.
* `parte2_metodo_utilizado.py`: Detalles sobre el método utilizado.
* `parte3_repulsion_niveles.py`: Explicación de la repulsión de niveles.
* `parte4_trayectorias.py`: Visualización de las trayectorias.
* `parte5_simetrias.py`: Desglose de las simetrías.

Cada parte define una función (ej: `play_parte1(scene)`) a la que se le pasa la escena principal para añadir las animaciones.

## ¿Qué necesitan instalar?

Si aún no lo tienen, instalen Manim y Manim Slides en su entorno:

```bash
pip install manim manim-slides
```

## ¿Cómo trabajar y probar las diapositivas conjuntas?

Para **generar/renderizar toda la presentación**, ejecuten desde la raíz del proyecto:

```bash
manim presentation/main_presentation.py PresentacionGeneral -p -ql
```

Para **presentar** las diapositivas de forma interactiva (con pausas):

```bash
python3 -m manim_slides PresentacionGeneral
```

*(Si el comando `manim-slides` no es reconocido por tu terminal, ejecuta `python3 -m manim_slides`)*
*(Si te aparece un error del tipo `AttributeError: 'QVideoWidget' object has no attribute 'videoSink'`, es porque tienes instalado PyQt5 y está causando conflicto. Ejecuta entonces: `QT_API=pyside6 python3 -m manim_slides PresentacionGeneral`)*

Usa las flechas `Izquierda`/`Derecha` para navegar por las diapositivas a través de las diferentes secciones.

---
**Trabajo en equipo:** Puedes crear tu rama (e.g. `feature/trayectorias`) y trabajar únicamente en el archivo `parte4_trayectorias.py`. Como `main_presentation.py` simplemente llama a esas funciones, no tendréis conflictos al juntarlo todo en la rama `main`.
