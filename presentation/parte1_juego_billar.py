from manim import *

def play_parte1(scene):
    """
    Sección 1: Juego de Billar
    """
    titulo = Text("1. Juego de Billar", font_size=48, color=BLUE)
    
    scene.play(Write(titulo))
    scene.next_slide()
    
    scene.play(titulo.animate.to_edge(UP))
    
    rect = Rectangle(width=4, height=2, color=WHITE)
    scene.play(Create(rect))
    
    scene.next_slide()
    
    scene.play(FadeOut(titulo), FadeOut(rect))
