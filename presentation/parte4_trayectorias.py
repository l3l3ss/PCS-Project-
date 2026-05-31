from manim import *
import numpy as np

def generar_estadio(L, R, pos_ini, vel_ini, num_bounces):

    top_line = Line(start=[-L, R, 0], end=[L, R, 0], color=WHITE)
    right_arc = Arc(radius=R, start_angle=-PI/2, angle=PI, arc_center=[L, 0, 0], color=WHITE)
    bottom_line = Line(start=[L, -R, 0], end=[-L, -R, 0], color=WHITE)
    left_arc = Arc(radius=R, start_angle=PI/2, angle=PI, arc_center=[-L, 0, 0], color=WHITE)
    visual_obj = VGroup(top_line, right_arc, bottom_line, left_arc)

    points = [np.array([pos_ini[0], pos_ini[1], 0])]
    current_pos = pos_ini.copy()
    current_vel = vel_ini / np.linalg.norm(vel_ini)

    for _ in range(num_bounces):
        t_min = float('inf')
        n_min = None

        if current_vel[1] > 1e-6:
            t = (R - current_pos[1]) / current_vel[1]
            if t > 1e-6:
                x_int = current_pos[0] + t * current_vel[0]
                if -L <= x_int <= L and t < t_min:
                    t_min = t
                    n_min = np.array([0, -1])

        if current_vel[1] < -1e-6:
            t = (-R - current_pos[1]) / current_vel[1]
            if t > 1e-6:
                x_int = current_pos[0] + t * current_vel[0]
                if -L <= x_int <= L and t < t_min:
                    t_min = t
                    n_min = np.array([0, 1])

        dp_r = current_pos - np.array([L, 0])
        b_r = np.dot(current_vel, dp_r)
        c_r = np.dot(dp_r, dp_r) - R**2
        disc_r = b_r**2 - c_r
        if disc_r >= 0:
            for t in [-b_r - np.sqrt(disc_r), -b_r + np.sqrt(disc_r)]:
                if t > 1e-6:
                    x_int = current_pos[0] + t * current_vel[0]
                    if x_int >= L - 1e-5 and t < t_min:
                        t_min = t
                        p_int = current_pos + t * current_vel
                        n_min = -(p_int - np.array([L, 0])) / R

        dp_l = current_pos - np.array([-L, 0])
        b_l = np.dot(current_vel, dp_l)
        c_l = np.dot(dp_l, dp_l) - R**2
        disc_l = b_l**2 - c_l
        if disc_l >= 0:
            for t in [-b_l - np.sqrt(disc_l), -b_l + np.sqrt(disc_l)]:
                if t > 1e-6:
                    x_int = current_pos[0] + t * current_vel[0]
                    if x_int <= -L + 1e-5 and t < t_min:
                        t_min = t
                        p_int = current_pos + t * current_vel
                        n_min = -(p_int - np.array([-L, 0])) / R

        if t_min < float('inf') and n_min is not None:
            current_pos = current_pos + t_min * current_vel
            points.append(np.array([current_pos[0], current_pos[1], 0]))
            current_vel = current_vel - 2 * np.dot(current_vel, n_min) * n_min
            current_vel = current_vel / np.linalg.norm(current_vel)
        else:
            break

    return visual_obj, points

def generar_rectangulo(L, R, pos_ini, vel_ini, num_bounces):

    top_line = Line(start=[-L, R, 0], end=[L, R, 0], color=WHITE)
    bottom_line = Line(start=[L, -R, 0], end=[-L, -R, 0], color=WHITE)
    right_line = Line(start=[L, R, 0], end=[L, -R, 0], color=WHITE)
    left_line = Line(start=[-L, -R, 0], end=[-L, R, 0], color=WHITE)
    visual_obj = VGroup(top_line, right_line, bottom_line, left_line)

    points = [np.array([pos_ini[0], pos_ini[1], 0])]
    current_pos = pos_ini.copy()
    current_vel = vel_ini / np.linalg.norm(vel_ini)

    for _ in range(num_bounces):
        t_min = float('inf')
        n_min = None

        if current_vel[1] > 1e-6:
            t = (R - current_pos[1]) / current_vel[1]
            if t > 1e-6:
                x_int = current_pos[0] + t * current_vel[0]
                if -L <= x_int <= L and t < t_min:
                    t_min = t
                    n_min = np.array([0, -1])

        if current_vel[1] < -1e-6:
            t = (-R - current_pos[1]) / current_vel[1]
            if t > 1e-6:
                x_int = current_pos[0] + t * current_vel[0]
                if -L <= x_int <= L and t < t_min:
                    t_min = t
                    n_min = np.array([0, 1])

        if current_vel[0] > 1e-6:
            t = (L - current_pos[0]) / current_vel[0]
            if t > 1e-6:
                y_int = current_pos[1] + t * current_vel[1]
                if -R <= y_int <= R and t < t_min:
                    t_min = t
                    n_min = np.array([-1, 0])

        if current_vel[0] < -1e-6:
            t = (-L - current_pos[0]) / current_vel[0]
            if t > 1e-6:
                y_int = current_pos[1] + t * current_vel[1]
                if -R <= y_int <= R and t < t_min:
                    t_min = t
                    n_min = np.array([1, 0])

        if t_min < float('inf') and n_min is not None:
            current_pos = current_pos + t_min * current_vel
            points.append(np.array([current_pos[0], current_pos[1], 0]))
            current_vel = current_vel - 2 * np.dot(current_vel, n_min) * n_min
            current_vel = current_vel / np.linalg.norm(current_vel)
        else:
            break

    return visual_obj, points

def play_parte4(self):

    question = Text(
        "How does this difference\nbetween the chaotic and\nintegrable systems manifest\nin the physical structure\nof the states?",
        font_size=36
    )

    self.play(FadeIn(question))
    self.next_slide()
    self.play(FadeOut(question))

    dots = VGroup()
    center_prob = LEFT*1 + DOWN*0.5
    for x in np.linspace(-3, 3, 15):
        for y in np.linspace(-2, 2, 10):
            dist = np.sqrt((x - center_prob[0])**2 + (y - center_prob[1])**2)
            opacity = max(0.1, 1 - dist)
            dot = Dot(point=[x, y, 0], radius=0.08, color=BLUE, fill_opacity=opacity)
            dots.add(dot)

    mag_glass_circle = Circle(radius=0.8, color=WHITE, stroke_width=4).move_to(center_prob)
    mag_glass_handle = Line(mag_glass_circle.get_corner(DR), mag_glass_circle.get_corner(DR) + RIGHT*0.5 + DOWN*0.5, color=WHITE, stroke_width=6)
    mag_glass = VGroup(mag_glass_circle, mag_glass_handle)

    prob_text = MathTex(r"|\psi_{i,j}|^2", font_size=48).next_to(mag_glass_circle, UR, buff=0.5)

    self.play(FadeIn(dots))
    self.wait(0.5)
    self.play(Create(mag_glass), Write(prob_text))
    self.next_slide()

    self.play(FadeOut(dots), FadeOut(mag_glass), FadeOut(prob_text))

    title_int = Text("Integrable case", font_size=40).to_edge(UP)
    self.play(Write(title_int))

    pos_inicial = np.array([0.2, 0.1])
    angulo = np.deg2rad(41)
    vel_inicial = np.array([np.cos(angulo), np.sin(angulo)])
    rebotes = 30

    rect_int, puntos_ruta_rect = generar_rectangulo(3.0, 2.0, pos_inicial, vel_inicial, rebotes)
    self.play(Create(rect_int))

    ball = Dot(point=puntos_ruta_rect[0], color=YELLOW)

    trail = VMobject(stroke_color=YELLOW, stroke_width=2)
    trail.set_points_as_corners([puntos_ruta_rect[0], puntos_ruta_rect[0]])

    self.add(trail)
    self.play(FadeIn(ball))

    lengths = [np.linalg.norm(puntos_ruta_rect[i+1] - puntos_ruta_rect[i]) for i in range(len(puntos_ruta_rect)-1)]
    total_length = sum(lengths)

    def get_path_state_rect(alpha):
        if alpha >= 1.0:
            return puntos_ruta_rect[-1], puntos_ruta_rect
        target_dist = alpha * total_length
        current_dist = 0
        for i in range(len(puntos_ruta_rect)-1):
            if current_dist + lengths[i] >= target_dist:
                seg_length = lengths[i]
                seg_alpha = (target_dist - current_dist) / seg_length if seg_length > 0 else 0
                p_start = puntos_ruta_rect[i]
                p_end = puntos_ruta_rect[i+1]
                current_pos = p_start * (1 - seg_alpha) + p_end * seg_alpha
                return current_pos, puntos_ruta_rect[:i+1] + [current_pos]
            current_dist += lengths[i]
        return puntos_ruta_rect[-1], puntos_ruta_rect

    self.play(
        UpdateFromAlphaFunc(ball, lambda mob, alpha: mob.move_to(get_path_state_rect(alpha)[0])),
        UpdateFromAlphaFunc(trail, lambda mob, alpha: mob.set_points_as_corners(get_path_state_rect(alpha)[1])),
        run_time=10.0,
        rate_func=linear
    )

    self.next_slide()

    self.play(FadeOut(ball), FadeOut(trail), FadeOut(rect_int))

    img_int = ImageMobject("output/dens_prob_r_975.png")
    img_int.height = 4.0

    exp_text_int = Text(
        "In the previous animation, the areas of highest\nconcentration of the trajectory followed by the\nball are indicated with a colormap.",
        font_size=24
    ).next_to(img_int, DOWN, buff=0.5)

    self.play(FadeIn(img_int), Write(exp_text_int))
    self.next_slide()

    self.play(FadeOut(img_int), FadeOut(exp_text_int), FadeOut(title_int))

    title_chaotic = Text("Chaotic Billiard", font_size=40).to_edge(UP)
    self.play(Write(title_chaotic))

    stadium, puntos_ruta_estadio = generar_estadio(1.4, 2.0, pos_inicial, vel_inicial, rebotes)
    self.play(Create(stadium))

    ball2 = Dot(point=puntos_ruta_estadio[0], color=YELLOW)

    trail2 = VMobject(stroke_color=YELLOW, stroke_width=2)
    trail2.set_points_as_corners([puntos_ruta_estadio[0], puntos_ruta_estadio[0]])

    self.add(trail2)
    self.play(FadeIn(ball2))

    lengths2 = [np.linalg.norm(puntos_ruta_estadio[i+1] - puntos_ruta_estadio[i]) for i in range(len(puntos_ruta_estadio)-1)]
    total_length2 = sum(lengths2)

    def get_path_state_estadio(alpha):
        if alpha >= 1.0:
            return puntos_ruta_estadio[-1], puntos_ruta_estadio
        target_dist = alpha * total_length2
        current_dist = 0
        for i in range(len(puntos_ruta_estadio)-1):
            if current_dist + lengths2[i] >= target_dist:
                seg_length = lengths2[i]
                seg_alpha = (target_dist - current_dist) / seg_length if seg_length > 0 else 0
                p_start = puntos_ruta_estadio[i]
                p_end = puntos_ruta_estadio[i+1]
                current_pos = p_start * (1 - seg_alpha) + p_end * seg_alpha
                return current_pos, puntos_ruta_estadio[:i+1] + [current_pos]
            current_dist += lengths2[i]
        return puntos_ruta_estadio[-1], puntos_ruta_estadio

    self.play(
        UpdateFromAlphaFunc(ball2, lambda mob, alpha: mob.move_to(get_path_state_estadio(alpha)[0])),
        UpdateFromAlphaFunc(trail2, lambda mob, alpha: mob.set_points_as_corners(get_path_state_estadio(alpha)[1])),
        run_time=10.0,
        rate_func=linear
    )

    self.next_slide()

    self.play(FadeOut(ball2), FadeOut(trail2), FadeOut(stadium))

    img_chaotic = ImageMobject("output/dens_prob_c_800.png")
    img_chaotic.height = 4.5

    self.play(FadeIn(img_chaotic))
    self.next_slide()

    self.play(FadeOut(img_chaotic), FadeOut(title_chaotic))
