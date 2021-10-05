from pathlib import Path

import moderngl
import moderngl_window as mglw

ctx = moderngl.create_standalone_context()


class Window(mglw.WindowConfig):
    gl_version = (3, 3)
    title = "Particles"
    window_size = (1280, 720)
    aspect_ratio = 16 / 9
    resizable = True

    resource_dir = Path(__file__).parent / "resources"

    @classmethod
    def run(cls):
        mglw.run_window_config(cls)
