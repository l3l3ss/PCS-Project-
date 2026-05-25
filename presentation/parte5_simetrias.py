from manim import *

def play_parte5(scene):
    """
    Sección 5: Simetrías
    """
    titulo = Text("5. Simetrías", font_size=48, color=PURPLE)
    
    scene.play(Write(titulo))
    scene.next_slide()
    
    scene.play(titulo.animate.to_edge(UP))
    
    cuarto = Sector(radius=2, angle=PI/2, color=PURPLE, fill_opacity=0.5)
    cuarto.move_to(ORIGIN)
    
    scene.play(FadeIn(cuarto, shift=DOWN))
    
    texto_simetria = Text("Descomposición por paridad", font_size=24)
    texto_simetria.next_to(cuarto, DOWN)
    
    scene.play(Write(texto_simetria))
    
    scene.next_slide()
    
    scene.play(FadeOut(titulo), FadeOut(cuarto), FadeOut(texto_simetria))
