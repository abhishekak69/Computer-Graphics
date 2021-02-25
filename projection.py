import pygame
import time
from vector_class import vec3, vec2

O = vec3()
Cw = 800
Ch = 800
size = [Cw, Ch]
screen = pygame.display.set_mode(size)
d = 1
Vw = 1
Vh = 1
inf = 999
projection_plane_d = 1
# BACKGROUND_COLOR = (255, 255, 255)
BACKGROUND_COLOR = vec3()
BLUE = vec3(0, 0, 255)
GREEN = vec3(0, 255, 0)
RED = vec3(255, 0, 0)


def putpixel(Cx, Cy, color):
    Sx = (Cw/2)+Cx
    Sy = (Ch/2)-Cy
    pygame.draw.circle(screen, (color.x, color.y, color.z), (Sx, Sy), 1)


def interpolate(i0, d0, i1, d1):
    if i0 == i1:
        return [d0]
    values = []
    a = (d1 - d0) / (i1 - i0)
    d = d0
    for i in range(int(i0), int(i1)+1):
        values.append(d)
        d = d + a
    return values


# print(interpolate(0, 0, 0, -150))


def drawLine(p0, p1, color):
    x0, y0, x1, y1 = p0.x, p0.y, p1.x, p1.y
    # print(x0, y0, x1, y1)
    if abs(x1 - x0) > abs(y1 - y0):
        if x0 > x1:
            p0, p1 = p1, p0

        ys = interpolate(p0.x, p0.y, p1.x, p1.y)
        for x in range(int(p0.x), int(p1.x)+1):
            putpixel(x, ys[int(x - p0.x)], color)

    else:
        if y0 > y1:
            p0, p1 = p1, p0
        xs = interpolate(p0.y, p0.x, p1.y, p1.x)
        for y in range(int(p0.y), int(p1.y)+1):
            putpixel(xs[int(y - p0.y)], y, color)


def ViewportToCanvas(x, y):
    return vec2(int(x * Cw/Vw), int(y * Ch/Vh))


def ProjectVertex(v):
    return ViewportToCanvas(v.x * d / v.z, v.y * d / v.z)


# def drawTriangle(p0, p1, p2, color):
#     drawLine(p0, p1, color)
#     drawLine(p1, p2, color)
#     drawLine(p2, p0, color)


# The four "front" vertices
vAf = vec3(-1,  1, 5)
vBf = vec3(1,  1, 5)
vCf = vec3(1, -1, 5)
vDf = vec3(-1, -1, 5)

# The four "back" vertices
vAb = vec3(-1,  1, 6)
vBb = vec3(1,  1, 6)
vCb = vec3(1, -1, 6)
vDb = vec3(-1, -1, 6)

# print(ProjectVertex(vAf), ProjectVertex(vBf), ProjectVertex(
#     vCf), ProjectVertex(vDf), ProjectVertex(vAb))
# print(ProjectVertex(vBb), ProjectVertex(vCb), ProjectVertex(vDb))


pygame.init()
pygame.display.set_caption("rasterisation Projection")
done = False
flag = False

while not done:
    screen.fill((255, 255, 255))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    if not flag:

        drawLine(ProjectVertex(vAf), ProjectVertex(vBf), BLUE)
        drawLine(ProjectVertex(vBf), ProjectVertex(vCf), BLUE)
        drawLine(ProjectVertex(vCf), ProjectVertex(vDf), BLUE)
        drawLine(ProjectVertex(vDf), ProjectVertex(vAf), BLUE)

        # The back face
        drawLine(ProjectVertex(vAb), ProjectVertex(vBb), RED)
        drawLine(ProjectVertex(vBb), ProjectVertex(vCb), RED)
        drawLine(ProjectVertex(vCb), ProjectVertex(vDb), RED)
        drawLine(ProjectVertex(vDb), ProjectVertex(vAb), RED)

        # The front-to-back edges
        drawLine(ProjectVertex(vAf), ProjectVertex(vAb), GREEN)
        drawLine(ProjectVertex(vBf), ProjectVertex(vBb), GREEN)
        drawLine(ProjectVertex(vCf), ProjectVertex(vCb), GREEN)
        drawLine(ProjectVertex(vDf), ProjectVertex(vDb), GREEN)

        pygame.display.update()
    flag = True
