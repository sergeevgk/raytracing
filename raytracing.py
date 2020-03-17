import numpy as np
import matplotlib.pyplot as plt
from test import *


def normalize(x):
    x /= np.linalg.norm(x)
    return x


def intersect_plane(O, D, P, N):
    # Return the distance from O to the intersection of the ray (O, D) with the 
    # plane (P, N), or +inf if there is no intersection.
    # O and P are 3D points, D and N (normal) are normalized vectors.
    denom = np.dot(D, N)
    if np.abs(denom) < 1e-6:
        return np.inf
    d = np.dot(P - O, N) / denom
    if d < 0:
        return np.inf
    return d


def intersect_sphere(O, D, S, R):
    # Return the distance from O to the intersection of the ray (O, D) with the 
    # sphere (S, R), or +inf if there is no intersection.
    # O and S are 3D points, D (direction) is a normalized vector, R is a scalar.
    a = np.dot(D, D)
    OS = O - S
    b = 2 * np.dot(D, OS)
    c = np.dot(OS, OS) - R * R
    disc = b * b - 4 * a * c
    if disc > 0:
        distSqrt = np.sqrt(disc)
        q = (-b - distSqrt) / 2.0 if b < 0 else (-b + distSqrt) / 2.0
        t0 = q / a
        t1 = c / q
        t0, t1 = min(t0, t1), max(t0, t1)
        if t1 >= 0:
            return t1 if t0 < 0 else t0
    return np.inf


def intersect(O, D, obj):
    if obj['type'] == 'plane':
        return intersect_plane(O, D, obj['position'], obj['normal'])
    elif obj['type'] == 'sphere':
        return intersect_sphere(O, D, obj['position'], obj['radius'])


def get_normal(obj, M):
    # Find normal.
    if obj['type'] == 'sphere':
        N = normalize(M - obj['position'])
    elif obj['type'] == 'plane':
        N = obj['normal']
    return N


def get_color(obj, M):
    color = obj['color']
    if not hasattr(color, '__len__'):
        color = color(M)
    return color


def trace_ray(rayO, rayD):
    # Find first point of intersection with the scene.
    t = np.inf
    for i, obj in enumerate(scene):
        t_obj = intersect(rayO, rayD, obj)
        if t_obj < t:
            t, obj_idx = t_obj, i
    # Return None if the ray does not intersect any object.
    if t == np.inf:
        return
    # Find the object.
    obj = scene[obj_idx]
    # Find the point of intersection on the object.
    M = rayO + rayD * t
    # Find properties of the object.
    N = get_normal(obj, M)
    color = get_color(obj, M)
    toL = normalize(L - M)
    toO = normalize(O - M)
    # Shadow: find if the point is shadowed or not.
    col_shadow_coeff = 1.
    for k, obj_sh in enumerate(scene):
        if k != obj_idx:
            if intersect(M + N * .0001, toL, obj_sh) < np.inf:
                col_shadow_coeff *= obj_sh.get('transparency', 0.)
    # Start computing the color.
    col_ray = ambient
    # Lambert shading (diffuse).
    col_ray += obj.get('diffuse_c', diffuse_c) * max(np.dot(N, toL), 0) * color
    # Blinn-Phong shading (specular).
    col_ray += obj.get('specular_c', specular_c) * max(np.dot(N, normalize(toL + toO)), 0) ** specular_k * color_light
    col_ray *= col_shadow_coeff
    return obj, M, N, col_ray


def refract(v, n, q):
    nv = np.dot(n, v)

    if nv > 0:
        return refract(v, n * (-1), 1 / q)

    a = 1 / q
    D = 1 - a * a * (1 - nv * nv)
    return None if D < 0 else (a * v) - (nv * a + np.math.sqrt(D) * n)


def rt(rayO, rayD, reflection, col, depth, normalDirection):
    if depth >= depth_max:
        return True

    traced = trace_ray(rayO, rayD)

    if not traced:
        return False

    obj, M, N, col_ray = traced
    col += reflection * col_ray * (1 - obj.get('transparency', 0.))
    # Reflection: create a new ray.
    dir = normalize(rayD - 2 * np.dot(rayD, N) * N)
    rayO1, rayD1 = M + N * normalDirection * .0001, dir
    if rt(rayO1, rayD1, reflection * obj.get('reflection', 1.), col, depth + 1, normalDirection):
        return False

    # Refraction
    dir = refract(rayD, N, obj.get('refrcoeff', 1.))
    if dir is None:
        return False
    rayO2, rayD2 = M - N * normalDirection * .0001, dir
    if rt(rayO2, rayD2, reflection * obj.get('transparency', 1.), col, depth + 1, normalDirection * (-1)):
        return False

    return False


if __name__ == '__main__':
    img = np.zeros((h, w, 3))
    for i, x in enumerate(np.linspace(S[0], S[2], w)):
        if i % 10 == 0:
            print(i / float(w) * 100, "%")
        for j, y in enumerate(np.linspace(S[1], S[3], h)):
            col[:] = 0
            Q[:2] = (x, y)
            D = normalize(Q - O)
            depth = 0
            rayO, rayD = O, D
            reflection = 1.
            normalDirection = 1
            rt(rayO, rayD, reflection, col, depth, normalDirection)

            img[h - j - 1, i, :] = np.clip(col, 0, 1)

    plt.imsave(output_filename + '.png', img)
