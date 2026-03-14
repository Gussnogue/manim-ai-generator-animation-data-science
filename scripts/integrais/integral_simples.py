from manim import *

class IntegralSimples(Scene):
    def construct(self):
        # Eixos cartesianos
        axes = Axes(
            x_range=[-0.5, 2.5, 0.5],
            y_range=[-0.5, 4.5, 0.5],
            x_length=8,
            y_length=5,
            axis_config={"color": BLUE},
        )
        axes.add_coordinates()
        self.add(axes)

        # Função f(x) = x²
        graph = axes.plot(lambda x: x**2, x_range=[0, 2], color=YELLOW)

        # Área sob a curva (integral)
        area = axes.get_area(graph, x_range=[0, 2], color=TEAL, opacity=0.5)

        # Rótulo da função
        func_label = MathTex("f(x) = x^2", color=YELLOW).next_to(graph, UR, buff=0.5)

        # Título
        title = Text("Integral Simples: ∫₀² x² dx", font_size=36).to_edge(UP)

        # Animação
        self.play(Write(title))
        self.wait(0.5)
        self.play(Create(axes))
        self.wait(0.5)
        self.play(Create(graph))
        self.wait(0.5)
        self.play(FadeIn(func_label))
        self.wait(0.5)
        self.play(FadeIn(area))
        self.wait(2)

        