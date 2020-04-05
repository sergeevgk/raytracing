import numpy as np


def add_sphere(position, radius, color, transparency=0.0, refrcoeff=0.0):
    return dict(type='sphere', position=np.array(position),
                radius=np.array(radius), color=np.array(color), reflection=.2,
                transparency=transparency, refrcoeff=refrcoeff)


def add_plane(position, normal):
    return dict(type='plane', position=np.array(position),
                normal=np.array(normal),
                color=lambda M: (color_plane0
                                 if (int(M[0] * 2) % 2) == (int(M[2] * 2) % 2) else color_plane1),
                diffuse_c=.75, specular_c=.5, reflection=.25)


# List of objects.
color_plane0 = 1. * np.ones(3)
color_plane1 = 0. * np.ones(3)

scene = [add_sphere([.4, .1, 1.], .4, [0., 0., 1.], transparency=0.7, refrcoeff=2),
         add_sphere([-.4, .1, 1.], .4, [0., 1., 0.], transparency=0.9, refrcoeff=1.5),
         add_sphere([.0, .8, 1.], .4, [1., 0., 0.], transparency=0.5, refrcoeff=1.0),
         add_plane([0., -.5, 0.], [0., 1., 0.]),
         ]

# Light position and color.
L = np.array([4., 4., -10.])
color_light = np.ones(3)

# Default light and material parameters.
ambient = .05
diffuse_c = 1.
specular_c = 1.
specular_k = 50

depth_max = 5  # Maximum number of light reflections.
col = np.zeros(3)  # Current color.
O = np.array([0., 0.35, -1.])  # Camera.
Q = np.array([0., 0., 0.])  # Camera pointing to.

# image width and height
w = 1000
h = 750

output_filename = "result" + str(w) + "x" + str(h)
r = float(w) / h
# Screen coordinates: x0, y0, x1, y1.
S = (-1., -1. / r + .25, 1., 1. / r + .25)
