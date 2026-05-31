from manim import *
import numpy as np

def get_rectangular_path(start_pos, velocity, num_bounces, width, height):
    points = [np.array(start_pos, dtype=float)]
    curr_pos = np.array(start_pos, dtype=float)
    curr_vel = np.array(velocity, dtype=float)

    for _ in range(num_bounces):
        tx = float('inf')
        if curr_vel[0] > 0:
            tx = (width/2 - curr_pos[0]) / curr_vel[0]
        elif curr_vel[0] < 0:
            tx = (-width/2 - curr_pos[0]) / curr_vel[0]

        ty = float('inf')
        if curr_vel[1] > 0:
            ty = (height/2 - curr_pos[1]) / curr_vel[1]
        elif curr_vel[1] < 0:
            ty = (-height/2 - curr_pos[1]) / curr_vel[1]

        t = min(tx, ty)
        next_pos = curr_pos + t * curr_vel
        points.append(next_pos)

        if t == tx:
            curr_vel[0] *= -1
        if t == ty:
            curr_vel[1] *= -1

        curr_pos = next_pos

    return points

def get_stadium_path(start_pos, velocity, num_bounces, straight_width, radius):
    points = [np.array(start_pos, dtype=float)]
    curr_pos = np.array(start_pos, dtype=float)
    curr_vel = np.array(velocity, dtype=float)

    for _ in range(num_bounces):
        best_t = float('inf')
        normal = None

        if curr_vel[1] != 0:
            t_top = (radius - curr_pos[1]) / curr_vel[1]
            if t_top > 1e-5:
                x_hit = curr_pos[0] + t_top * curr_vel[0]
                if abs(x_hit) <= straight_width / 2:
                    if t_top < best_t:
                        best_t = t_top
                        normal = np.array([0, -1, 0], dtype=float)

            t_bot = (-radius - curr_pos[1]) / curr_vel[1]
            if t_bot > 1e-5:
                x_hit = curr_pos[0] + t_bot * curr_vel[0]
                if abs(x_hit) <= straight_width / 2:
                    if t_bot < best_t:
                        best_t = t_bot
                        normal = np.array([0, 1, 0], dtype=float)

        w2 = straight_width / 2
        a = curr_vel[0]**2 + curr_vel[1]**2

        b = 2 * (curr_vel[0] * (curr_pos[0] - w2) + curr_vel[1] * curr_pos[1])
        c = (curr_pos[0] - w2)**2 + curr_pos[1]**2 - radius**2
        disc = b**2 - 4*a*c
        if disc >= 0:
            if a != 0:
                t1 = (-b + np.sqrt(disc)) / (2*a)
                t2 = (-b - np.sqrt(disc)) / (2*a)
                for t in (t1, t2):
                    if t > 1e-5:
                        hit_x = curr_pos[0] + t * curr_vel[0]
                        if hit_x >= w2 - 1e-5:
                            if t < best_t:
                                best_t = t
                                hit_y = curr_pos[1] + t * curr_vel[1]
                                normal = np.array([w2 - hit_x, -hit_y, 0], dtype=float)
                                normal = normal / np.linalg.norm(normal)

        b_left = 2 * (curr_vel[0] * (curr_pos[0] + w2) + curr_vel[1] * curr_pos[1])
        c_left = (curr_pos[0] + w2)**2 + curr_pos[1]**2 - radius**2
        disc_left = b_left**2 - 4*a*c_left
        if disc_left >= 0:
            if a != 0:
                t1 = (-b_left + np.sqrt(disc_left)) / (2*a)
                t2 = (-b_left - np.sqrt(disc_left)) / (2*a)
                for t in (t1, t2):
                    if t > 1e-5:
                        hit_x = curr_pos[0] + t * curr_vel[0]
                        if hit_x <= -w2 + 1e-5: 
                            if t < best_t:
                                best_t = t
                                hit_y = curr_pos[1] + t * curr_vel[1]
                                normal = np.array([-w2 - hit_x, -hit_y, 0], dtype=float)
                                normal = normal / np.linalg.norm(normal)

        if best_t == float('inf'):
            break

        next_pos = curr_pos + best_t * curr_vel
        points.append(next_pos)

        curr_vel = curr_vel - 2 * np.dot(curr_vel, normal) * normal
        curr_pos = next_pos

    return points

def play_parte1(scene):

    titulo = Text("Chaotic vs Deterministic", font_size=48, color=BLUE)

    scene.play(Write(titulo))
    scene.next_slide()

    title_rect = Text("Rectangular", font_size=40).to_edge(UP)
    scene.play(Transform(titulo, title_rect))

    rect_billiard = Rectangle(width=6, height=3, color=WHITE)
    scene.play(Create(rect_billiard))

    colors = [RED, GREEN, BLUE]
    angles = [0.6, 0.62, 0.58]
    paths_rect = []
    dots_rect = []
    traces_rect = []

    for i, angle in enumerate(angles):
        v = [np.cos(angle)*1.5, np.sin(angle)*1.5, 0]
        pts = get_rectangular_path([0,0,0], v, 8, 6, 3)
        path = VMobject().set_points_as_corners(pts)
        paths_rect.append(path)

        dot = Dot(color=colors[i]).move_to(pts[0])
        trace = TracedPath(dot.get_center, stroke_color=colors[i], stroke_width=2)

        dots_rect.append(dot)
        traces_rect.append(trace)

    scene.add(*traces_rect)
    scene.play(*[FadeIn(dot) for dot in dots_rect])

    scene.play(
        *[MoveAlongPath(dot, path, run_time=6, rate_func=linear) for dot, path in zip(dots_rect, paths_rect)]
    )
    scene.next_slide()

    scene.play(FadeOut(rect_billiard), *[FadeOut(t) for t in traces_rect], *[FadeOut(d) for d in dots_rect])

    title_stad = Text("Stadium", font_size=40).to_edge(UP)
    scene.play(Transform(titulo, title_stad))

    stadium_billiard = VGroup(
        Line(LEFT*2 + UP*1.5, RIGHT*2 + UP*1.5),
        Line(LEFT*2 + DOWN*1.5, RIGHT*2 + DOWN*1.5),
        Arc(radius=1.5, start_angle=-PI/2, angle=PI).shift(RIGHT*2),
        Arc(radius=1.5, start_angle=PI/2, angle=PI).shift(LEFT*2)
    )
    scene.play(Create(stadium_billiard))

    paths_stad = []
    dots_stad = []
    traces_stad = []
    for i, angle in enumerate(angles):
        v = [np.cos(angle)*1.5, np.sin(angle)*1.5, 0]
        pts = get_stadium_path([0,0,0], v, 8, 4, 1.5)
        path = VMobject().set_points_as_corners(pts)
        paths_stad.append(path)

        dot = Dot(color=colors[i]).move_to(pts[0])
        trace = TracedPath(dot.get_center, stroke_color=colors[i], stroke_width=2)
        dots_stad.append(dot)
        traces_stad.append(trace)

    scene.add(*traces_stad)
    scene.play(*[FadeIn(dot) for dot in dots_stad])
    scene.play(
        *[MoveAlongPath(dot, path, run_time=6, rate_func=linear) for dot, path in zip(dots_stad, paths_stad)]
    )
    scene.next_slide()

    scene.play(FadeOut(stadium_billiard), *[FadeOut(t) for t in traces_stad], *[FadeOut(d) for d in dots_stad])

    title_coords = Text("Coordinate Dependence", font_size=40).to_edge(UP)
    scene.play(Transform(titulo, title_coords))

    rect_wall = Line(DOWN*1.5, UP*1.5, color=WHITE).shift(LEFT*4)
    stad_wall = Arc(radius=3, start_angle=PI - PI/6, angle=PI/3, color=WHITE).shift(RIGHT*5)

    text_indep = Text("Independent x, y", font_size=30).next_to(rect_wall, UP, buff=0.5)
    text_dep = Text("Dependent x, y", font_size=30).next_to(stad_wall, UP, buff=0.5)

    pt_rect = rect_wall.point_from_proportion(0.5)
    v_in_rect = Arrow(pt_rect + LEFT*2 + DOWN*1, pt_rect, buff=0, color=YELLOW)
    v_out_rect = Arrow(pt_rect, pt_rect + LEFT*2 + UP*1, buff=0, color=YELLOW)

    pt_stad = stad_wall.point_from_proportion(0.7) 
    v_in_stad = Arrow(pt_stad + LEFT*2 + DOWN*0.5, pt_stad, buff=0, color=YELLOW)
    v_out_stad = Arrow(pt_stad, pt_stad + LEFT*1.5 + UP*1.5, buff=0, color=YELLOW)

    scene.play(
        Create(rect_wall), Create(stad_wall),
        Write(text_indep), Write(text_dep)
    )
    scene.play(GrowArrow(v_in_rect), GrowArrow(v_in_stad))
    scene.play(GrowArrow(v_out_rect), GrowArrow(v_out_stad))

    scene.next_slide()

    scene.play(
        FadeOut(rect_wall), FadeOut(stad_wall),
        FadeOut(text_indep), FadeOut(text_dep),
        FadeOut(v_in_rect), FadeOut(v_out_rect),
        FadeOut(v_in_stad), FadeOut(v_out_stad)
    )

    title_class_quant = Text("Classical vs Quantum", font_size=40).to_edge(UP)
    scene.play(Transform(titulo, title_class_quant))

    t_classical = Text("Classical: Particle", font_size=36).move_to(UP*1.5 + LEFT*3)
    dot_classical = Dot(color=BLUE).move_to(UP*0.5 + LEFT*4)

    t_quantum = Text("Quantum: Wave", font_size=36).move_to(DOWN*1 + LEFT*3)

    grid_center = DOWN * 1.5 + RIGHT * 2
    dots_data = []
    for x in range(-7, 8):
        for y in range(-3, 4):
            pos = grid_center + RIGHT * (x * 0.4) + UP * (y * 0.4)
            dots_data.append(pos)

    grid = VGroup(*[Dot(radius=0.03, color=BLUE).move_to(pos) for pos in dots_data])

    wave_pos = ValueTracker(-4.0)

    def update_grid(g):
        wx = wave_pos.get_value()
        for dot, pos in zip(g, dots_data):
            dx = pos[0] - (grid_center[0] + wx)
            dy = pos[1] - grid_center[1]
            dist_sq = dx**2 + dy**2
            amplitude = 4.0
            sigma = 1.0
            factor = 1 + amplitude * np.exp(- dist_sq / (2 * sigma**2))

            new_dot = Dot(radius=0.03 * factor, color=BLUE)
            new_dot.set_opacity(min(1.0, 0.2 + 0.8 * (factor - 1) / amplitude))
            new_dot.move_to(pos)
            dot.become(new_dot)

    grid.add_updater(update_grid)

    scene.play(Write(t_classical), Write(t_quantum))
    scene.add(grid)
    scene.play(
        FadeIn(dot_classical),
        FadeIn(grid)
    )

    scene.play(
        dot_classical.animate.shift(RIGHT * 6),
        wave_pos.animate.set_value(4.0),
        run_time=4,
        rate_func=linear
    )
    grid.clear_updaters()
    scene.next_slide()

    scene.play(
        FadeOut(t_classical), FadeOut(t_quantum),
        FadeOut(dot_classical), FadeOut(grid)
    )

    title_eq = Text("Quantum Mechanics", font_size=40).to_edge(UP)
    scene.play(Transform(titulo, title_eq))

    full_eq = MathTex(r"\hat{H}\Psi = E\Psi", r"\implies \Psi = \sum_i c_i \Psi_i", font_size=60)
    full_eq.move_to(ORIGIN)

    eq_schrodinger = MathTex(r"\hat{H}\Psi = E\Psi", font_size=60).move_to(ORIGIN)

    scene.play(Write(eq_schrodinger))
    scene.next_slide()

    scene.play(
        Transform(eq_schrodinger, full_eq[0]),
        Write(full_eq[1])
    )

    text_linear = Text("Linearity of Solutions", font_size=36, color=YELLOW).next_to(full_eq, DOWN, buff=1)
    scene.play(Write(text_linear))

    scene.next_slide()

    scene.play(FadeOut(titulo), FadeOut(eq_schrodinger), FadeOut(full_eq[1]), FadeOut(text_linear))
