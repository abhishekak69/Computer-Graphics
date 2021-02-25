import pygame
import numpy as np
import math
import threading
import time

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
# BACKGROUND_COLOR = (255, 255, 255)
BACKGROUND_COLOR = (0, 0, 0)
recursion_depth = 3


class light():
    def __init__(self, type, intensity, position=None, direction=None):
        self.type, self.intensity, self.position, self.direction = (
            type, intensity, position, direction)


l1 = light("ambient", 0.2)
l2 = light("point", 0.6, position=(2, 1, 0))
l3 = light("directional", 0.2, direction=(1, 4, 4))
Lights = [l1, l2, l3]


def ReflectRay(R, N):
    n_dot_r = dot(N, R)*2
    return (n_dot_r*N[0]-R[0], n_dot_r*N[1]-R[1], n_dot_r*N[2]-R[2])


def length(A):
    return math.sqrt(A[0]**2+A[1]**2+A[2]**2)


def ComputeLighting(P, N, V, s):
    i = 0.0
    for light in Lights:
        if light.type == "ambient":
            i += light.intensity
        else:
            if light.type == "point":
                L = (light.position[0] - P[0], light.position[1] -
                     P[1], light.position[2] - P[2])
                t_max = 1
            else:
                L = light.direction
                t_max = inf
            shadow_sphere, shadow_t = ClosestIntersection(P, L, 0.001, t_max)
            if shadow_sphere != None:
                continue
            n_dot_l = dot(N, L)
            if n_dot_l > 0:
                i += light.intensity * n_dot_l/(length(N) * length(L))

            if s != -1:
                n_dot_l = 2*dot(N, L)
                R = (N[0]*n_dot_l-L[0], N[1]*n_dot_l-L[1], N[2]*n_dot_l-L[2])
                r_dot_v = dot(R, V)
                if r_dot_v > 0:
                    i += light.intensity*pow(r_dot_v/(length(R)*length(V)), s)
    return i


class sphere():
    def __init__(self, center, radius, color, specular, reflective):
        self.center, self.radius, self.color, self.specular, self.reflective = (
            center, radius, color, specular, reflective)

    def display(self):
        print(self.center, self.radius, self.color)


# s1 = sphere((0, -1, 3), 1, (255, 0, 0), 500, 0.2)
s1 = sphere((0, 0, 3), 0.5, (255, 0, 0), 500, 0.2)

s2 = sphere((2, 0, 4), 1, (0, 0, 255), 500, 0.3)
s3 = sphere((-2, 0, 4), 1, (0, 255, 0), 10, 0.4)
s4 = sphere((0, -5001, 0), 5000, (255, 255, 0), 1000, 0.5)
scene = [s1, s2, s3, s4]


def dot(a, b):
    return (a[0]*b[0]+a[1]*b[1]+a[2]*b[2])


def clamp(color):
    color = list(color)
    for i in range(3):
        if color[i] > 255:
            color[i] = 255
    return color


def putpixel(Cx, Cy, color, screen):
    Sx = (Cw/2)+Cx
    Sy = (Ch/2)-Cy
    pygame.draw.circle(screen, clamp(color), (Sx, Sy), 1)


def CanvasToViewport(x, y):
    return (x*(Vw/Cw), y*(Vh/Ch), d)


def ClosestIntersection(O, D, t_min, t_max):
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

    return (closest_sphere, closest_t)


def TraceRay(O, D, t_min, t_max, depth):
    closest_sphere, closest_t = ClosestIntersection(O, D, t_min, t_max)

    if closest_sphere == None:
        return BACKGROUND_COLOR

    # return closest_sphere.color
    P = ((O[0] + closest_t * D[0]),
         (O[1] + closest_t * D[1]), (O[2] + closest_t * D[2]))
    N = (P[0] - closest_sphere.center[0], P[1] -
         closest_sphere.center[1], P[2] - closest_sphere.center[2])
    len_N = length(N)
    N = (N[0]/len_N, N[1]/len_N, N[2]/len_N)
    i = ComputeLighting(P, N, (-D[0], -D[1], -D[2]), closest_sphere.specular)
    local_color = (
        closest_sphere.color[0] * i, closest_sphere.color[1] * i, closest_sphere.color[2] * i)
    r = closest_sphere.reflective

    if r <= 0 or depth <= 0:
        return local_color
    R = ReflectRay((-D[0], -D[1], -D[2]), N)
    reflected_color = TraceRay(P, R, 0.001, inf, depth - 1)
    return (local_color[0]*(1-r)+reflected_color[0]*r, local_color[1]*(1-r)+reflected_color[1]*r, local_color[2]*(1-r)+reflected_color[2]*r)


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


def threadpix(xstart, xend, ystart, yend, step):
    # print("new Thread")
    for y in range(ystart, yend, -step):
        for x in range(xstart, xend):
            # print(y, x)
            D = CanvasToViewport(x, y)
            color = TraceRay(O, D, 1, inf, recursion_depth)
            putpixel(x, y, color, screen)
            pygame.display.update()
    return


step = 4
t_1 = threading.Thread(
    target=threadpix, args=(-(Cw//2), (Cw//2), (Ch//2)-1, -(Ch//2)-1, step))
t_2 = threading.Thread(
    target=threadpix, args=((-Cw//2), (Cw//2),  (Ch//2)-2, -(Ch//2)-1, step))
t_3 = threading.Thread(
    target=threadpix, args=(-(Cw//2), (Cw//2),  (Ch//2)-3, -(Ch//2)-1, step))
t_4 = threading.Thread(
    target=threadpix, args=(-(Cw//2), (Cw//2),  (Ch//2)-4, -(Ch//2)-1, step))
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
        time1 = time.perf_counter()
        t_1.start()
        t_2.start()
        t_3.start()
        t_4.start()

        t_1.join()
        t_2.join()
        t_3.join()
        t_4.join()

        time2 = time.perf_counter()
        if not flag:
            print(time2-time1)
        # threadpix(-Cw//2, (Cw//2)+1, Ch//2, -1)
        # threadpix(-Cw//2, (Cw//2)+1, 0, (-Ch//2)+1)
        # for y in range(Ch//2, (-(Ch//2))-1, -1):
        #     for x in range(-Cw//2, (Cw//2)+1):
        #         D = CanvasToViewport(x, y)
        #         color = TraceRay(O, D, 1, inf)
        #         putpixel(x, y, color, screen)
        #         pygame.display.update()
        flag = True
    # done = True

    # This function must write after all the other drawing commands.
    # pygame.display.update()

pygame.quit()
