#version 330

uniform vec2 acceleration;
uniform float restitution_coefficient;

in vec2 in_pos;
in vec2 in_prev;

out vec2 out_pos;
out vec2 out_prev;

void main() {
    vec2 velocity = in_pos - in_prev;

    if (in_pos.x <= -1 || in_pos.x >= 1) {
        velocity.x = -velocity.x;
        velocity *= restitution_coefficient;
    }

    if (in_pos.y <= -1 || in_pos.y >= 1) {
        velocity.y = -velocity.y;
        velocity *= restitution_coefficient;
    }

    velocity += acceleration;

    out_pos = in_pos + velocity;
    out_prev = in_pos;
}
