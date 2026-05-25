from manim import *
from manim_slides import Slide
from parte3_repulsion_niveles import play_parte3

class TestScene(Slide):
    def construct(self):
        play_parte3(self)
