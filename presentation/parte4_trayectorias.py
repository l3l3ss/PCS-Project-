from manim import *

def play_parte4(scene):
    """
    Sección 4: Trayectorias
    """
    titulo = Text("4. Trayectorias Clásicas y Cicatrices", font_size=40, color=RED)
    
    scene.play(FadeIn(titulo, scale=0.5))
    scene.next_slide()
    
    scene.play(titulo.animate.to_edge(UP))
    
    punto = Dot(color=YELLOW)
    trayectoria = Line(LEFT * 2, RIGHT * 2, color=RED)
    
    scene.play(Create(trayectoria))
    scene.play(MoveAlongPath(punto, trayectoria), run_time=2)
    
    scene.next_slide()
    
    scene.play(FadeOut(titulo), FadeOut(punto), FadeOut(trayectoria))
