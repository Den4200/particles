#version 330

in vec2 in_pos;
in vec3 in_color;
out vec3 color;

void main() {
    color = in_color;
    gl_Position = vec4(in_pos, 0, 1);
}
