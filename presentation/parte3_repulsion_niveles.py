from manim import *
import numpy as np

def QuadraticBezier(p0, p1, p2, color=WHITE):

    return CubicBezier(p0, p0 + (2/3)*(p1 - p0), p2 + (2/3)*(p1 - p2), p2, color=color)

def play_parte3(scene):

    title = Text("3. Domains & Separability", font_size=40, color=YELLOW).to_edge(UP)
    scene.play(Write(title))

    msg_5 = Text("Coupling Between Axes", font_size=32, color=YELLOW).next_to(title, DOWN)
    scene.play(Write(msg_5))

    rect_small = Rectangle(width=3, height=2, color=BLUE).shift(LEFT*3.5 + UP*0.5)
    stad_small = VGroup(
        Line(LEFT*1 + UP*0.8, RIGHT*1 + UP*0.8, color=RED),
        Line(LEFT*1 + DOWN*0.8, RIGHT*1 + DOWN*0.8, color=RED),
        ArcBetweenPoints(RIGHT*1 + UP*0.8, RIGHT*1 + DOWN*0.8, angle=-PI, color=RED),
        ArcBetweenPoints(LEFT*1 + DOWN*0.8, LEFT*1 + UP*0.8, angle=-PI, color=RED)
    ).shift(RIGHT*3.5 + UP*0.5)

    scene.play(Create(rect_small), Create(stad_small))

    slider = NumberLine(x_range=[0, 10, 1], length=6, color=WHITE).shift(DOWN*2.5)
    slider_label = Text("Parameter A (x-mode)", font_size=24).next_to(slider, LEFT)
    pointer = Triangle(color=YELLOW, fill_opacity=1).scale(0.2).rotate(PI).next_to(slider.n2p(0), UP, buff=0.1)

    scene.play(Create(slider), Write(slider_label), DrawBorderThenFill(pointer))

    def get_rect_grid(t):
        vg = VGroup()
        center = rect_small.get_center()
        for i in range(1, 6):
            x_prop = (i/6 - 0.5)*2
            x_shift = np.sin(t + i)*0.3
            vg.add(Line(
                center + RIGHT*(x_prop*1.5 + x_shift) + DOWN*1, 
                center + RIGHT*(x_prop*1.5 + x_shift) + UP*1, 
                color=TEAL
            ))
        for i in range(1, 4):
            y_prop = (i/4 - 0.5)*2
            vg.add(Line(
                center + LEFT*1.5 + UP*(y_prop*1), 
                center + RIGHT*1.5 + UP*(y_prop*1), 
                color=PURPLE
            ))
        return vg

    def get_stad_grid(t):
        vg = VGroup()
        center = stad_small.get_center()
        for i in range(1, 6):
            x_prop = (i/6 - 0.5)*2
            vg.add(QuadraticBezier(
                center + RIGHT*(x_prop*1.8) + UP*0.8,
                center + RIGHT*(x_prop*1.8 + np.sin(t*0.5)*0.5) + UP*(0.3 * np.cos(t+i)), 
                center + RIGHT*(x_prop*1.8) + DOWN*0.8,
                color=TEAL
            ))
        for i in range(1, 4):
            y_prop = (i/4 - 0.5)*2
            vg.add(QuadraticBezier(
                center + LEFT*1.5 + UP*(y_prop*0.8),
                center + RIGHT*(0.5 * np.sin(t*0.5-i)) + UP*(y_prop*0.8 + np.cos(t*0.5)*0.2),
                center + RIGHT*1.5 + UP*(y_prop*0.8),
                color=PURPLE
            ))
        return vg

    t_tracker = ValueTracker(0)
    rect_g = always_redraw(lambda: get_rect_grid(t_tracker.get_value()))
    stad_g = always_redraw(lambda: get_stad_grid(t_tracker.get_value()))

    pointer.add_updater(lambda p: p.next_to(slider.n2p(t_tracker.get_value()), UP, buff=0.1))

    scene.play(Create(rect_g), Create(stad_g))

    scene.play(t_tracker.animate.set_value(10), run_time=6, rate_func=there_and_back)

    pointer.clear_updaters()
    scene.next_slide()

    scene.play(
        FadeOut(VGroup(msg_5, slider, slider_label, pointer, rect_g, stad_g, rect_small, stad_small, title))
    )

    title_repulsion = Text("Level Repulsion", font_size=40, color=YELLOW).to_edge(UP)
    scene.play(Write(title_repulsion))

    eq_text = Text("Nearest-Neighbor Spacing:", font_size=32).shift(UP*0.5)

    eq_formula = MathTex(r"s_i = E_i - E_{i-1}", font_size=48).next_to(eq_text, DOWN, buff=0.5)

    box = SurroundingRectangle(eq_formula, color=WHITE, buff=0.3)

    scene.play(Write(eq_text))
    scene.play(Write(eq_formula), Create(box))

    scene.next_slide()

    scene.play(FadeOut(eq_text), FadeOut(eq_formula), FadeOut(box))

    np.random.seed(42)
    poisson_data = np.random.exponential(scale=1.0, size=500)
    poisson_hist, _ = np.histogram(poisson_data, bins=15, range=(0, 4), density=True)

    def wigner_dyson(x):
        return (np.pi / 2) * x * np.exp(- (np.pi / 4) * x**2)

    x_rand = np.random.uniform(0, 4, 2000)
    y_rand = np.random.uniform(0, 1.2, 2000)
    wd_data = x_rand[y_rand < wigner_dyson(x_rand)]
    wd_data = wd_data[:500]
    wd_hist, _ = np.histogram(wd_data, bins=15, range=(0, 4), density=True)

    axes_rect = Axes(
        x_range=[0, 4, 1],
        y_range=[0, 1.2, 0.5],
        x_length=4,
        y_length=3,
        axis_config={"include_numbers": False},
        tips=False,
    ).shift(LEFT * 3.5 + DOWN * 0.5)

    axes_stad = Axes(
        x_range=[0, 4, 1],
        y_range=[0, 1.2, 0.5],
        x_length=4,
        y_length=3,
        axis_config={"include_numbers": False},
        tips=False,
    ).shift(RIGHT * 3.5 + DOWN * 0.5)

    label_rect = Text("Rectangular", font_size=28).next_to(axes_rect, UP)
    label_stad = Text("Stadium", font_size=28).next_to(axes_stad, UP)

    def get_bars(axes, hist_data, color):
        bars = VGroup()
        bar_width = axes.x_length / 15
        for i, h in enumerate(hist_data):
            x_val = (i + 0.5) * (4 / 15)
            y_val = h
            bottom = axes.c2p(x_val - (4/30), 0)
            top = axes.c2p(x_val - (4/30), y_val)
            height = np.linalg.norm(top - bottom)

            rect = Rectangle(width=bar_width*0.8, height=height, color=color, fill_opacity=0.7)
            rect.move_to(bottom + UP * height/2)
            bars.add(rect)
        return bars

    bars_rect = get_bars(axes_rect, poisson_hist, BLUE)
    bars_stad = get_bars(axes_stad, wd_hist, RED)

    scene.play(Create(axes_rect), Create(axes_stad), Write(label_rect), Write(label_stad))
    scene.play(
        AnimationGroup(*[GrowFromEdge(bar, DOWN) for bar in bars_rect], lag_ratio=0.08),
        AnimationGroup(*[GrowFromEdge(bar, DOWN) for bar in bars_stad], lag_ratio=0.08)
    )

    scene.next_slide()

    scene.play(FadeOut(axes_rect), FadeOut(axes_stad), FadeOut(label_rect), FadeOut(label_stad), FadeOut(bars_rect), FadeOut(bars_stad))

    bgs_text = Text("BGS Conjecture", font_size=42, color=TEAL).shift(UP*1)

    arrow = Arrow(UP, DOWN, color=WHITE, buff=0.5).next_to(bgs_text, DOWN)

    rmt_text = Text("Random Matrix Theory (RMT)", font_size=42, color=ORANGE).next_to(arrow, DOWN)

    scene.play(Write(bgs_text))
    scene.play(GrowArrow(arrow))
    scene.play(Write(rmt_text))

    scene.next_slide()

    scene.play(FadeOut(bgs_text), FadeOut(arrow), FadeOut(rmt_text))

    scene.play(
        FadeIn(axes_rect), FadeIn(axes_stad), FadeIn(label_rect), FadeIn(label_stad),
        AnimationGroup(*[GrowFromEdge(bar, DOWN) for bar in bars_rect], lag_ratio=0.05),
        AnimationGroup(*[GrowFromEdge(bar, DOWN) for bar in bars_stad], lag_ratio=0.05)
    )

    formula_poisson = MathTex(r"P(s) = e^{-s}", font_size=32).next_to(axes_rect, UP, buff=0.8)
    formula_wd = MathTex(r"P(s) = \frac{\pi}{2} s \exp\left(-\frac{\pi}{4} s^2\right)", font_size=32).next_to(axes_stad, UP, buff=0.8)

    scene.play(
        label_rect.animate.next_to(formula_poisson, UP, buff=0.2),
        label_stad.animate.next_to(formula_wd, UP, buff=0.2)
    )

    scene.play(Write(formula_poisson), Write(formula_wd))

    curve_poisson = axes_rect.plot(lambda x: np.exp(-x), color=YELLOW, x_range=[0, 4])
    curve_wd = axes_stad.plot(wigner_dyson, color=YELLOW, x_range=[0, 4])

    scene.play(Create(curve_poisson), Create(curve_wd))

    scene.next_slide()

    det_label = Text("Deterministic / Integrable", font_size=24, color=BLUE).next_to(axes_rect, DOWN, buff=0.5)
    chaotic_label = Text("Chaotic", font_size=24, color=RED).next_to(axes_stad, DOWN, buff=0.5)

    scene.play(Write(det_label), Write(chaotic_label))

    scene.next_slide()

    scene.play(
        FadeOut(VGroup(
            axes_rect, axes_stad, label_rect, label_stad, 
            bars_rect, bars_stad, formula_poisson, formula_wd, 
            curve_poisson, curve_wd, det_label, chaotic_label
        ))
    )

    results_subtitle = Text("Our Results", font_size=32, color=WHITE).next_to(title_repulsion, DOWN)

    img_distr_r = ImageMobject("/home/pabloore/conjuntoV/universidad/Practicas/fisicaComplejos/PCS-Project-/output/170x100_distr_r_solo.png")
    img_distr_r.height = 5.5
    img_distr_r.move_to(DOWN * 0.5)

    scene.play(Write(results_subtitle))
    scene.play(
        FadeIn(img_distr_r)
    )

    scene.next_slide()

    img_distr_qc = ImageMobject("/home/pabloore/conjuntoV/universidad/Practicas/fisicaComplejos/PCS-Project-/output/170x100_solo_distr_qc.png")
    img_distr_qc.height = 5.5
    img_distr_qc.move_to(DOWN * 0.5)

    scene.play(
        FadeOut(img_distr_r)
    )
    scene.play(
        FadeIn(img_distr_qc)
    )

    scene.next_slide()

    scene.play(
        FadeOut(Group(
            title_repulsion, results_subtitle, img_distr_qc
        ))
    )
