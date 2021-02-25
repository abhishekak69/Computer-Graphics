import pygame
import numpy as np
import math

O = (0, 0, 0)
Cw = 600
Ch = 600
size = [Cw, Ch]
screen = pygame.display.set_mode(size)
d = 1
Vw = 1
Vh = 1
inf = 999
projection_plane_d = 1
BACKGROUND_COLOR = (0, 0, 0)


class light():
    def __init__(self, type, intensity, position=None, direction=None):
        self.type, self.intensity, self.position, self.direction = (
            type, intensity, position, direction)


l1 = light("ambient", 0.2)
l2 = light("point", 0.6, position=(2, 1, 0))
l3 = light("directional", 0.2, direction=(1, 4, 4))
Lights = [l1, l2, l3]


def length(A):
    return math.sqrt(A[0]**2+A[1]**2+A[2]**2)


def ComputeLighting(P, N):
    i = 0.0
    for light in Lights:
        if light.type == "ambient":
            i += light.intensity
        else:
            if light.type == "point":
                L = (light.position[0] - P[0], light.position[1] -
                     P[1], light.position[2] - P[2])
            else:
                L = light.direction

            n_dot_l = dot(N, L)
            if n_dot_l > 0:
                i += light.intensity * n_dot_l/(length(N) * length(L))
    return i


class sphere():
    def __init__(self, center, radius, color):
        self.center, self.radius, self.color = (center, radius, color)

    def display(self):
        print(self.center, self.radius, self.color)


s1 = sphere((0, 0, 3), 0.5, (255, 0, 0))
s2 = sphere((2, 0, 4), 1, (0, 0, 255))
s3 = sphere((-2, 0, 4), 1, (0, 255, 0))
s4 = sphere((0, -5001, 0), 5000, (255, 255, 0))
scene = [s1, s2, s3, s4]


def dot(a, b):
    return (a[0]*b[0]+a[1]*b[1]+a[2]*b[2])


def putpixel(Cx, Cy, color, screen):
    Sx = (Cw/2)+Cx
    Sy = (Ch/2)-Cy
    pygame.draw.circle(screen, color, (Sx, Sy), 1)


def CanvasToViewport(x, y):
    return (x*(Vw/Cw), y*(Vh/Ch), d)


def TraceRay(O, D, t_min, t_max):
    closest_t = inf
    closest_sphere = None
    for sphere in scene:
        t1, t2 = IntersectRaySphere(O, D, sphere)
        if t_min < t1 < t_max and t1 < closest_t:
            closest_t = t1
            closest_sphere = sphere

        if t_min < t2 < t_max and t2 < closest_t:
            closest_t = t2
            closest_sphere = sphere

    if closest_sphere == None:
        return BACKGROUND_COLOR

    # return closest_sphere.color
    P = ((O[0] + closest_t * D[0]),
         (O[1] + closest_t * D[1]), (O[2] + closest_t * D[2]))
    N = (P[0] - closest_sphere.center[0], P[1] -
         closest_sphere.center[1], P[2] - closest_sphere.center[2])
    len_N = length(N)
    N = (N[0]/len_N, N[1]/len_N, N[2]/len_N)
    return (closest_sphere.color[0] * ComputeLighting(P, N), closest_sphere.color[1] * ComputeLighting(P, N), closest_sphere.color[2] * ComputeLighting(P, N))


def IntersectRaySphere(O, D, sphere):
    r = sphere.radius
    CO = (O[0]-sphere.center[0], O[1]-sphere.center[1], O[2]-sphere.center[2])

    a = dot(D, D)
    b = 2*dot(CO, D)
    c = dot(CO, CO) - r*r

    discriminant = b*b - 4*a*c
    if discriminant < 0:
        return (inf, inf)

    t1 = (-b + math.sqrt(discriminant)) / (2*a)
    t2 = (-b - math.sqrt(discriminant)) / (2*a)
    return (t1, t2)


pygame.init()
pygame.display.set_caption("Yeahhh Babyyy")
done = False
flag = False
# clock = pygame.time.Clock()
while not done:
    # clock.tick(120)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    screen.fill((0, 0, 0))
    if not flag:
        for y in range(Ch//2, (-(Ch//2))-1, -1):
            for x in range(-Cw//2, (Cw//2)+1):
                D = CanvasToViewport(x, y)
                color = TraceRay(O, D, 1, inf)
                putpixel(x, y, color, screen)
                pygame.display.update()
        flag = True
    # done = True

    # This function must write after all the other drawing commands.
    # pygame.display.update()

pygame.quit()
