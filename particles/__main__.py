import moderngl
import numpy as np

from particles.window import Window

PARTICLE_COUNT = 100000
ACCELERATION = (0, -0.0001)
RESITUTION_COEFFICIENT = 0.95


def particle() -> np.ndarray:
    a = np.random.uniform(0, np.pi * 2.0)
    r = np.random.uniform(0, 0.001)

    return np.array(
        [0, 0, np.cos(a) * r - 0.003, np.sin(a) * r - 0.008],
        dtype="f4",
    )

def particle_color() -> np.ndarray:
    return np.array(
        [np.random.uniform(0.5, 1) for _ in range(3)],
        dtype="f4",
    )


class ParticleSimulation(Window):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.program = self.ctx.program(
            vertex_shader=(self.resource_dir / "program_vertex_shader.glsl").read_text(),
            fragment_shader=(self.resource_dir / "program_fragment_shader.glsl").read_text(),
        )

        self.transform = self.ctx.program(
            vertex_shader=(self.resource_dir / "transform_vertex_shader.glsl").read_text(),
            varyings=["out_pos", "out_prev"],
        )

        self.transform["acceleration"].value = ACCELERATION
        self.transform["restitution_coefficient"].value = RESITUTION_COEFFICIENT

        self.vbo1 = self.ctx.buffer(b"".join(particle() for _ in range(PARTICLE_COUNT)))
        self.vbo2 = self.ctx.buffer(reserve=self.vbo1.size)

        self.cvbo = self.ctx.buffer(b"".join(particle_color() for _ in range(PARTICLE_COUNT)))

        self.vao1 = self.ctx.vertex_array(
            self.program,
            [
                (self.vbo1, "2f 2x4", "in_pos"),
                (self.cvbo, "3f", "in_color"),
            ],
        )

        self.vao2 = self.ctx.vertex_array(
            self.transform,
            [(self.vbo1, "2f 2f", "in_pos", "in_prev")],
        )

    def render(self, time: float, dt: float):
        self.ctx.clear(0, 0, 0)
        self.ctx.point_size = 3

        self.vao1.render(moderngl.POINTS, PARTICLE_COUNT)
        self.vao2.transform(self.vbo2, moderngl.POINTS, PARTICLE_COUNT)
        self.ctx.copy_buffer(self.vbo1, self.vbo2)


if __name__ == "__main__":
    ParticleSimulation.run()
