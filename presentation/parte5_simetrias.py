from manim import *
import numpy as np

def get_wave_image(a, r, quad_x, quad_y, parity_x=1, parity_y=1, res=150):
    width = a + r
    height = r

    nx = int(res * width / r)
    ny = res

    x = np.linspace(0, width, nx)
    y = np.linspace(0, height, ny)
    X, Y = np.meshgrid(x, y)

    Z_base = np.sin(2 * np.pi * X / width) * np.sin(2 * np.pi * Y / height)
    Z_base += 0.7 * np.sin(3 * np.pi * X / width) * np.sin(3 * np.pi * Y / height)

    mask = (X <= a) | ((X - a)**2 + Y**2 <= r**2)
    Z_base[~mask] = 0

    sign = 1
    if quad_x == -1: sign *= parity_x
    if quad_y == -1: sign *= parity_y

    Z = Z_base * sign

    img = np.zeros((ny, nx, 4), dtype=np.uint8)

    pos = Z > 0
    neg = Z < 0

    mag = np.abs(Z)
    mag_max = np.max(mag)
    if mag_max > 0:
        mag = mag / mag_max

    img[pos, 0] = 220
    img[pos, 1] = 50
    img[pos, 2] = 50
    img[pos, 3] = (mag[pos] * 220).astype(np.uint8)

    img[neg, 0] = 50
    img[neg, 1] = 100
    img[neg, 2] = 220
    img[neg, 3] = (mag[neg] * 220).astype(np.uint8)

    img = img[::-1, :, :]

    if quad_x == -1:
        img = img[:, ::-1, :]
    if quad_y == -1:
        img = img[::-1, :, :]

    image_mobj = ImageMobject(img)
    image_mobj.set_width(width)
    image_mobj.set_height(height)

    image_mobj.move_to(ORIGIN)
    image_mobj.shift(RIGHT * (width/2 * quad_x) + UP * (height/2 * quad_y))

    return image_mobj

def get_quarter_outline(a, r, quad_x=1, quad_y=1):
    base_outline = VGroup(
        Line(ORIGIN, [a, 0, 0]),
        Arc(radius=r, arc_center=[a, 0, 0], start_angle=0, angle=PI/2),
        Line([a, r, 0], [0, r, 0]),
        Line([0, r, 0], ORIGIN)
    )
    if quad_x == -1:
        base_outline.stretch(-1, dim=0, about_point=ORIGIN)
    if quad_y == -1:
        base_outline.stretch(-1, dim=1, about_point=ORIGIN)
    return base_outline

def play_parte5(scene):

    titulo = Text("5. Symmetries and Parity", font_size=48, color=PURPLE)

    scene.play(Write(titulo))
    scene.next_slide()

    scene.play(titulo.animate.to_edge(UP).scale(0.8))

    a = 1.4
    r = 2.0

    ejes = Axes(
        x_range=[-4.5, 4.5, 1],
        y_range=[-3, 3, 1],
        x_length=9,
        y_length=6,
        axis_config={"color": GREY, "stroke_width": 2}
    )
    scene.play(Create(ejes), run_time=1.5)

    outline1 = get_quarter_outline(a, r, 1, 1).set_color(WHITE).set_stroke(width=3)
    wave1 = get_wave_image(a, r, 1, 1, parity_x=-1, parity_y=-1)

    texto_q1 = Text("State in the 1st Quadrant", font_size=24).next_to(ejes, DOWN)

    scene.play(Create(outline1), Write(texto_q1))
    scene.play(FadeIn(wave1))
    scene.next_slide()

    outline2 = get_quarter_outline(a, r, -1, 1).set_color(WHITE).set_stroke(width=3)
    wave2_geom = get_wave_image(a, r, -1, 1, parity_x=1, parity_y=-1)

    texto_ref_x = Text("Reflection across the Y-axis", font_size=24).next_to(ejes, DOWN)

    scene.play(
        Transform(texto_q1, texto_ref_x),
        TransformFromCopy(outline1, outline2),
        TransformFromCopy(wave1, wave2_geom),
        run_time=1.5
    )
    scene.next_slide()

    texto_impar_x = Text("Odd Parity in X: Sign Change", font_size=24, color=YELLOW).next_to(ejes, DOWN)
    wave2_true = get_wave_image(a, r, -1, 1, parity_x=-1, parity_y=-1)

    scene.play(
        Transform(texto_q1, texto_impar_x),
        Transform(wave2_geom, wave2_true),
        run_time=1.5
    )
    scene.next_slide()

    outline3 = get_quarter_outline(a, r, -1, -1).set_color(WHITE).set_stroke(width=3)
    outline4 = get_quarter_outline(a, r, 1, -1).set_color(WHITE).set_stroke(width=3)

    wave3_geom = get_wave_image(a, r, -1, -1, parity_x=-1, parity_y=1)
    wave4_geom = get_wave_image(a, r, 1, -1, parity_x=-1, parity_y=1)

    texto_ref_y = Text("Reflection across the X-axis", font_size=24).next_to(ejes, DOWN)

    scene.play(
        Transform(texto_q1, texto_ref_y),
        TransformFromCopy(outline2, outline3),
        TransformFromCopy(outline1, outline4),
        TransformFromCopy(wave2_geom, wave3_geom),
        TransformFromCopy(wave1, wave4_geom),
        run_time=1.5
    )
    scene.next_slide()

    texto_impar_y = Text("Odd Parity in Y: Sign Change Again", font_size=24, color=YELLOW).next_to(ejes, DOWN)
    wave3_true = get_wave_image(a, r, -1, -1, parity_x=-1, parity_y=-1)
    wave4_true = get_wave_image(a, r, 1, -1, parity_x=-1, parity_y=-1)

    scene.play(
        Transform(texto_q1, texto_impar_y),
        Transform(wave3_geom, wave3_true),
        Transform(wave4_geom, wave4_true),
        run_time=1.5
    )
    scene.next_slide()

    texto_final = Text("Complete Stadium: Sum of Independent Patterns", font_size=28, color=GREEN).next_to(ejes, DOWN)

    stadium_border = VGroup(
        Line([-a, r, 0], [a, r, 0]),
        Arc(radius=r, arc_center=[a, 0, 0], start_angle=PI/2, angle=-PI),
        Line([a, -r, 0], [-a, -r, 0]),
        Arc(radius=r, arc_center=[-a, 0, 0], start_angle=-PI/2, angle=-PI)
    ).set_color(GREEN).set_stroke(width=5)

    scene.play(
        Transform(texto_q1, texto_final),
        Create(stadium_border),
        run_time=2.0
    )
    scene.next_slide()

    texto_cuarto = Text("Quarter Stadium Grid (Exploiting Symmetry)", font_size=28, color=BLUE).next_to(titulo, DOWN, buff=0.3)

    scene.play(
        FadeOut(texto_q1),
        FadeOut(ejes),
        FadeOut(outline2), FadeOut(outline3), FadeOut(outline4),
        FadeOut(wave2_geom), FadeOut(wave3_geom), FadeOut(wave4_geom),
        FadeOut(stadium_border),
        FadeIn(texto_cuarto)
    )

    group_q1 = Group(outline1, wave1)

    scene.play(
        group_q1.animate.move_to(ORIGIN).scale(1.5),
        run_time=1.5
    )

    rect_w = (a + r) * 1.5
    rect_h = r * 1.5
    rect_q1 = Rectangle(width=rect_w, height=rect_h, color=WHITE).move_to(group_q1.get_center())

    scene.play(Create(rect_q1))

    grid = VGroup()
    cols, rows = 85, 50
    cell_w, cell_h = rect_w / cols, rect_h / rows

    for i in range(1, cols):
        line = Line(rect_q1.get_corner(UL) + RIGHT * i * cell_w, rect_q1.get_corner(DL) + RIGHT * i * cell_w, color=GRAY, stroke_width=0.5)
        grid.add(line)
    for i in range(1, rows):
        line = Line(rect_q1.get_corner(UL) + DOWN * i * cell_h, rect_q1.get_corner(UR) + DOWN * i * cell_h, color=GRAY, stroke_width=0.5)
        grid.add(line)

    scene.play(Create(grid), run_time=1.5)

    nx_ny = MathTex(r"n_x = 170 \quad \quad n_y = 100", font_size=40).next_to(rect_q1, DOWN)
    scene.play(Write(nx_ny))

    scene.next_slide()

    scene.play(
        FadeOut(titulo),
        FadeOut(texto_cuarto),
        FadeOut(group_q1),
        FadeOut(rect_q1),
        FadeOut(grid),
        FadeOut(nx_ny)
    )

