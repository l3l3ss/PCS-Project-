from manim import *

def play_parte2(self):
    # =========================================================
    # DIAPOSITIVA 1
    # =========================================================
    
    # Expresión del Hamiltoniano en 2D
    hamiltonian = MathTex(
        r"H = -\frac{\hbar^2}{2m} \left( \frac{\partial^2}{\partial x^2} + \frac{\partial^2}{\partial y^2} \right) + V(x,y)"
    ).shift(UP * 1)
    
    self.play(Write(hamiltonian))
    self.wait(0.5)

    # Flecha hacia abajo
    arrow = Arrow(start=UP, end=DOWN, color=WHITE).next_to(hamiltonian, DOWN, buff=0.5)
    
    # Consideraciones: V=0, hbar^2/2m = 1
    considerations = MathTex(
        r"V(x,y) = 0", r"\quad \text{and} \quad", r"\frac{\hbar^2}{2m} = 1"
    ).next_to(arrow, DOWN, buff=0.5)

    self.play(GrowArrow(arrow))
    self.play(Write(considerations))
    self.next_slide()

    # Transición a la siguiente diapositiva
    self.play(FadeOut(hamiltonian), FadeOut(arrow), FadeOut(considerations))


    # =========================================================
    # DIAPOSITIVA 2
    # =========================================================
    
    # --- Animación 2.1 ---
    # Rectángulo en el centro (proporción 170x100 -> 6.8x4)
    rect = Rectangle(width=6.8, height=4, color=WHITE)
    self.play(Create(rect))
    self.wait(0.5)

    # Aplicar un grid
    grid = VGroup()
    # Usamos 85x50 visualmente para que la presentación no tarde mucho en renderizar, 
    # pero a nivel de densidad representa el 170x100 perfectamente
    cols, rows = 85, 50
    cell_w, cell_h = rect.width / cols, rect.height / rows
    
    for i in range(1, cols):
        line = Line(rect.get_corner(UL) + RIGHT * i * cell_w, rect.get_corner(DL) + RIGHT * i * cell_w, color=GRAY, stroke_width=0.5)
        grid.add(line)
    for i in range(1, rows):
        line = Line(rect.get_corner(UL) + DOWN * i * cell_h, rect.get_corner(UR) + DOWN * i * cell_h, color=GRAY, stroke_width=0.5)
        grid.add(line)
    
    self.play(Create(grid))
    self.wait(0.5)

    # Cuadraditos en azul
    blue_rects = VGroup()
    for i in range(cols):
        for j in range(rows):
            blue_rect = Rectangle(width=cell_w, height=cell_h, fill_color=BLUE, fill_opacity=0.6, stroke_width=0)
            blue_rect.move_to(rect.get_corner(UL) + RIGHT * (i + 0.5) * cell_w + DOWN * (j + 0.5) * cell_h)
            blue_rects.add(blue_rect)
    
    self.play(FadeIn(blue_rects))
    
    # Texto: Azul = True
    true_text = Text("Blue = True", color=BLUE, font_size=36).next_to(rect, DOWN)
    self.play(Write(true_text))
    self.next_slide()

    # --- Animación 2.2 ---
    # Desvanecer grid y azul
    self.play(FadeOut(grid), FadeOut(blue_rects), FadeOut(true_text))
    
    # Contorno de estadio de Bunimovich inscrito en el rectángulo
    # El rectángulo tiene ancho 6.8 y alto 4. 
    # Para que esté inscrito, el radio de los semicírculos debe ser 2 (la mitad del alto).
    # Esto deja un rectángulo central de ancho 6.8 - 2 - 2 = 2.8.
    stadium = VGroup()
    stadium_rect = Rectangle(width=2.8, height=4) 
    left_circle = Arc(radius=2, angle=PI, start_angle=PI/2, color=YELLOW, arc_center=stadium_rect.get_left())
    right_circle = Arc(radius=2, angle=PI, start_angle=-PI/2, color=YELLOW, arc_center=stadium_rect.get_right())
    
    top_line = Line(stadium_rect.get_corner(UL), stadium_rect.get_corner(UR), color=YELLOW)
    bottom_line = Line(stadium_rect.get_corner(DL), stadium_rect.get_corner(DR), color=YELLOW)
    
    stadium.add(top_line, bottom_line, left_circle, right_circle)
    
    self.play(Create(stadium))
    self.wait(0.5)

    # Nuevo grid
    self.play(Create(grid))
    self.wait(0.5)
    
    # Cuadrados dentro (azul/true) y fuera (rojo/false)
    stadium_cells = VGroup()
    
    for i in range(cols):
        for j in range(rows):
            cx = rect.get_corner(UL)[0] + (i + 0.5) * cell_w
            cy = rect.get_corner(UL)[1] - (j + 0.5) * cell_h
            
            # Comprobar si el centro de la celda está dentro del estadio
            inside = False
            if -1.4 <= cx <= 1.4 and -2 <= cy <= 2:
                inside = True # En la parte rectangular
            elif (cx - (-1.4))**2 + cy**2 <= 4:
                inside = True # En el semicírculo izquierdo
            elif (cx - 1.4)**2 + cy**2 <= 4:
                inside = True # En el semicírculo derecho
            
            color = BLUE if inside else RED
            cell_rect = Rectangle(width=cell_w, height=cell_h, fill_color=color, fill_opacity=0.6, stroke_width=0)
            cell_rect.move_to([cx, cy, 0])
            stadium_cells.add(cell_rect)
    
    self.play(FadeIn(stadium_cells))
    
    # Textos Rojo = False, Azul = True
    false_text = Text("Red = False", color=RED, font_size=36).next_to(rect, DOWN).shift(LEFT * 2)
    true_text2 = Text("Blue = True", color=BLUE, font_size=36).next_to(rect, DOWN).shift(RIGHT * 2)
    self.play(Write(false_text), Write(true_text2))
    self.next_slide()

    # --- Animación 2.3 ---
    # Transición fluida: movemos la caja y el estadio actual a la derecha,
    # y creamos una copia que se mueve a la izquierda revelando las celdas azules.
    
    bounding_box_left = rect.copy()
    dummy_blue = blue_rects.copy().set_opacity(0)
    target_blue = blue_rects.copy().scale(0.8).move_to(LEFT * 3.5 + DOWN * 0.5)
    
    self.add(bounding_box_left, dummy_blue)
    
    self.play(
        FadeOut(grid), FadeOut(stadium), FadeOut(false_text), FadeOut(true_text2),
        rect.animate.scale(0.8).move_to(RIGHT * 3.5 + DOWN * 0.5),
        stadium_cells.animate.scale(0.8).move_to(RIGHT * 3.5 + DOWN * 0.5),
        bounding_box_left.animate.scale(0.8).move_to(LEFT * 3.5 + DOWN * 0.5),
        ReplacementTransform(dummy_blue, target_blue)
    )
    
    # Mostrar nx y ny arriba
    nx_ny = MathTex(r"n_x = 170 \quad \quad n_y = 100").to_edge(UP).shift(DOWN * 0.5)
    self.play(Write(nx_ny))
    self.next_slide()
    
    # Transición
    self.play(FadeOut(bounding_box_left), FadeOut(target_blue), FadeOut(rect), FadeOut(stadium_cells), FadeOut(nx_ny))


    # =========================================================
    # DIAPOSITIVA 3
    # =========================================================
    
    # --- Animación 3.1 ---
    eq_x = MathTex(r"x_i = i \Delta x").shift(UP * 2 + LEFT * 2)
    eq_y = MathTex(r"y_j = j \Delta y").shift(UP * 2 + RIGHT * 2)
    
    eq_taylor = MathTex(
        r"\psi(x_i \pm \Delta x) = \psi(x_i) \pm \Delta x \psi'(x_i) + \frac{\Delta x^2}{2} \psi''(x_i) + \dots"
    ).shift(DOWN * 0.5)
    
    self.play(Write(eq_x), Write(eq_y))
    self.wait(0.5)
    self.play(Write(eq_taylor))
    self.next_slide()

    # --- Animación 3.2 ---
    # Hacer eq_x y eq_y más pequeñas y taylor al centro y más grande
    self.play(
        eq_x.animate.scale(0.7).to_corner(UL),
        eq_y.animate.scale(0.7).to_corner(UR),
        eq_taylor.animate.scale(1.2).move_to(ORIGIN)
    )
    self.next_slide()

    # --- Animación 3.3 ---
    # Reordenar términos para despejar segunda derivada
    eq_derivada = MathTex(
        r"\psi''(x_i) \approx \frac{\psi_{i+1} - 2\psi_i + \psi_{i-1}}{\Delta x^2}"
    ).scale(1.2).move_to(ORIGIN)
    
    self.play(ReplacementTransform(eq_taylor, eq_derivada))
    self.next_slide()

    # Transición
    self.play(FadeOut(eq_x), FadeOut(eq_y), FadeOut(eq_derivada))


    # =========================================================
    # DIAPOSITIVA 4
    # =========================================================
    
    # --- Animación 4.1 ---
    eq_deriv_x = MathTex(
        r"\psi''(x_i) \approx \frac{\psi_{i+1,j} - 2\psi_{i,j} + \psi_{i-1,j}}{\Delta x^2}"
    ).shift(UP * 1.5)
    
    eq_deriv_y = MathTex(
        r"\psi''(y_j) \approx \frac{\psi_{i,j+1} - 2\psi_{i,j} + \psi_{i,j-1}}{\Delta y^2}"
    ).shift(DOWN * 1.5)
    
    self.play(Write(eq_deriv_x))
    self.wait(0.5)
    self.play(Write(eq_deriv_y))
    self.next_slide()

    # --- Animación 4.2 ---
    # Más pequeñas, arriba, suma y línea
    group_derivs = VGroup(eq_deriv_x, eq_deriv_y)
    
    self.play(
        group_derivs.animate.scale(0.8).shift(UP * 1.5)
    )
    
    plus_sign = MathTex("+").next_to(eq_deriv_y, LEFT, buff=0.5)
    line = Line(
        group_derivs.get_corner(DL) + LEFT * 1, 
        group_derivs.get_corner(DR) + RIGHT * 1
    ).next_to(group_derivs, DOWN, buff=0.3)
    
    self.play(Write(plus_sign), Create(line))
    self.wait(0.5)
    
    # Resultado de la suma
    eq_sum_res = MathTex(
        r"\frac{\psi_{i+1,j} - 2\psi_{i,j} + \psi_{i-1,j}}{\Delta x^2} + \frac{\psi_{i,j+1} - 2\psi_{i,j} + \psi_{i,j-1}}{\Delta y^2}"
    ).next_to(line, DOWN, buff=0.5)
    
    self.play(Write(eq_sum_res))
    self.next_slide()

    # --- Animación 4.3 ---
    # Resultado al centro, y sumar E*phi = 0
    eq_helmholtz_discrete = MathTex(
        r"\frac{\psi_{i+1,j} - 2\psi_{i,j} + \psi_{i-1,j}}{\Delta x^2} + \frac{\psi_{i,j+1} - 2\psi_{i,j} + \psi_{i,j-1}}{\Delta y^2}",
        r" + E \psi_{i,j} = 0"
    ).move_to(ORIGIN)
    
    self.play(
        FadeOut(group_derivs), FadeOut(plus_sign), FadeOut(line),
        ReplacementTransform(eq_sum_res, eq_helmholtz_discrete[0])
    )
    self.play(Write(eq_helmholtz_discrete[1]))
    self.next_slide()

    # Transición
    self.play(FadeOut(eq_helmholtz_discrete))


    # =========================================================
    # DIAPOSITIVA 5
    # =========================================================
    
    # Matriz sparse en grande
    matrix_tex = r"""
    H' = 
    \begin{pmatrix}
    D      & \frac{1}{\Delta x^2} & 0      & \dots  & \frac{1}{\Delta y^2} & 0      & \dots \\
    \frac{1}{\Delta x^2} & D      & \frac{1}{\Delta x^2} & 0      & \dots  & \frac{1}{\Delta y^2} & \dots \\
    0      & \frac{1}{\Delta x^2} & D      & \frac{1}{\Delta x^2} & 0      & \dots  & \dots \\
    \vdots & 0      & \ddots & \ddots & \ddots & 0      & \vdots \\
    \frac{1}{\Delta y^2} & \vdots & 0      & \frac{1}{\Delta x^2} & D      & \frac{1}{\Delta x^2} & 0 \\
    0      & \frac{1}{\Delta y^2} & \vdots & \dots  & \frac{1}{\Delta x^2} & D      & \frac{1}{\Delta x^2} \\
    \vdots & \dots  & \dots  & \dots  & 0      & \frac{1}{\Delta x^2} & D      
    \end{pmatrix}
    """
    
    matrix_math = MathTex(matrix_tex).scale(0.8)
    
    # Añadimos el valor de D debajo de la matriz
    d_math = MathTex(r"D = k^2 - \left( \frac{2}{\Delta x^2} + \frac{2}{\Delta y^2} \right)").scale(0.8)
    
    group_matrix = VGroup(matrix_math, d_math).arrange(DOWN, buff=0.8).move_to(ORIGIN)
    
    self.play(Write(matrix_math))
    self.play(FadeIn(d_math, shift=UP))
    self.next_slide()
    
    # Final de la presentación
    self.play(FadeOut(group_matrix))