from manim import *

def play_parte3(scene):
    """
    Sección 3: Repulsión de Niveles
    """
    titulo = Text("3. Repulsión de Niveles", font_size=48, color=YELLOW)
    
    scene.play(DrawBorderThenFill(titulo))
    scene.next_slide()
    
    scene.play(titulo.animate.to_edge(UP))
    
    ejes = Axes(
        x_range=[0, 4, 1],
        y_range=[0, 1, 0.2],
        axis_config={"color": WHITE},
        x_length=6,
        y_length=4
    )
    labels = ejes.get_axis_labels(x_label="s", y_label="P(s)")
    
    scene.play(Create(ejes), Write(labels))
    
    scene.next_slide()
    
    scene.play(FadeOut(titulo), FadeOut(ejes), FadeOut(labels))
