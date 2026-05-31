from manim import *
from manim_slides import Slide

from parte1_juego_billar import play_parte1
from parte2_metodo_utilizado import play_parte2
from parte3_repulsion_niveles import play_parte3
from parte4_trayectorias import play_parte4
from parte5_simetrias import play_parte5

class PresentacionGeneral(Slide):

    def construct(self):

        titulo_principal = Text("Quantum Chaos and the\nStatistics of Energy Levels", font_size=48, color=TEAL)
        subtitulo = Text("Pablo Orellana and María de los Ángeles Lara", font_size=32)
        subtitulo.next_to(titulo_principal, DOWN)

        self.play(FadeIn(titulo_principal, shift=UP))
        self.play(Write(subtitulo))
        self.next_slide()

        self.play(FadeOut(titulo_principal), FadeOut(subtitulo))

        play_parte1(self)
        play_parte2(self)
        play_parte3(self)
        play_parte4(self)
        play_parte5(self)

        cierre = Text("Thanks for watching", font_size=48)
        mascota = ImageMobject("output/picho.png")
        mascota.scale(1.2)
        mascota.to_corner(DR)

        self.play(Write(cierre), FadeIn(mascota))
        self.next_slide()
        self.play(FadeOut(cierre), FadeOut(mascota))
