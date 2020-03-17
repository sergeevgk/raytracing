# Ray tracing with refractions and shadowing in Python

Forked originally from [rossant/raytracing.py] (https://gist.github.com/rossant/6046463 "Simple ray tracing")

Simple ray tracing engine in Python. Depends on NumPy and Matplotlib.
Originally RT engine included:
+ Diffuse and specular lighting
+ Reflections
+ Sequential algorithm with slow execution

Our goal is to add **refraction** and make **smooth shadowing**.
We implemented recursive algorithm instead of sequential to add refraction.

Test script is located in 'tests' directory along with result images of ray tracing engine runs.


