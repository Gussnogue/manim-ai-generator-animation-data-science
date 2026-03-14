from manim import *

class IntegralDupla(ThreeDScene):
    def construct(self):
        # Eixos 3D
        axes = ThreeDAxes(
            x_range=[-2, 2, 1],
            y_range=[-2, 2, 1],
            z_range=[0, 4, 1],
            x_length=6,
            y_length=6,
            z_length=4,
        )
        axes.add_coordinates()
        self.add(axes)

        # Superfície: f(x,y) = x^2 + y^2
        superficie = Surface(
            lambda u, v: np.array([u, v, u**2 + v**2]),
            u_range=[-1.5, 1.5],
            v_range=[-1.5, 1.5],
            resolution=(30, 30),
            fill_opacity=0.6,
            fill_color=BLUE,
            stroke_width=0.5,
            stroke_color=WHITE,
        )

        # Região de integração (retângulo no plano xy)
        regiao = Rectangle(
            width=3, height=3,
            color=YELLOW,
            fill_opacity=0.3,
            fill_color=YELLOW
        )
        regiao.move_to([0, 0, 0])  # centralizado na origem

        # Linhas verticais nas bordas para conectar a superfície (opcional)
        # Podemos fazer um grid de linhas para mostrar a projeção

        # Título
        titulo = Text("Integral Dupla: ∬_R (x² + y²) dA", font_size=36).to_edge(UP)

        self.play(Write(titulo))
        self.wait(1)

        # Mostrar eixos e região
        self.play(FadeIn(axes), FadeIn(regiao))
        self.wait(1)

        # Mostrar superfície
        self.play(
            Create(superficie),
            run_time=3,
        )
        self.wait(2)

        # Rotacionar a câmera para melhor visualização
        self.move_camera(phi=60 * DEGREES, theta=-45 * DEGREES, run_time=3)
        self.wait(2)

        # Destacar a região projetada na superfície (opcional)
        # Podemos criar uma cópia da região elevada até a superfície
        regiao_superior = regiao.copy()
        regiao_superior.apply_function(
            lambda p: np.array([p[0], p[1], p[0]**2 + p[1]**2])
        )
        regiao_superior.set_color(RED)
        regiao_superior.set_fill(opacity=0.5)

        self.play(Transform(regiao.copy(), regiao_superior), run_time=2)
        self.wait(2)

        # Fim
        self.wait(2)


