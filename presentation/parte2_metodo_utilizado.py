from manim import *

def play_parte2(scene):
    """
    Sección 2: Método Utilizado
    """
    titulo = Text("2. Método Utilizado", font_size=48, color=GREEN)
    
    scene.play(FadeIn(titulo, shift=UP))
    scene.next_slide()
    
    scene.play(titulo.animate.to_edge(UP))
    
    formula = MathTex(r"\hat{H} \psi = E \psi", font_size=72)
    descripcion = Text("Ecuación de Schrödinger independiente del tiempo", font_size=24)
    descripcion.next_to(formula, DOWN)
    
    scene.play(Write(formula))
    scene.play(FadeIn(descripcion))
    
    scene.next_slide()
    
    scene.play(FadeOut(titulo), FadeOut(formula), FadeOut(descripcion))
