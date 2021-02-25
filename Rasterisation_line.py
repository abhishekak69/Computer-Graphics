import numpy as np
import pygame
import time

O = (0, 0, 0)
Cw = 800
Ch = 800
size = [Cw, Ch]
# screen = pygame.display.set_mode(size)
d = 1
Vw = 1
Vh = 1
inf = 999
projection_plane_d = 1
# BACKGROUND_COLOR = (255, 255, 255)
BACKGROUND_COLOR = (0, 0, 0)


def putpixel(Cx, Cy, color):
    Sx = (Cw/2)+Cx
    Sy = (Ch/2)-Cy
    pygame.draw.circle(screen, color, (Sx, Sy), 1)


def interpolate(i0, d0, i1, d1):
    if i0 == i1:
        # print("equal", i0, d0, i1, d1)
        return [d0]
    # print(i0, d0, i1, d1)
    values = []
    a = (d1 - d0) / (i1 - i0)
    d = d0
    for i in range(i0, i1+1):
        values.append(d)
        d = d + a
    return values


# print(interpolate(0, 0, 0, -150))


def drawLine(p0, p1, color):
    x0, y0, x1, y1 = p0[0], p0[1], p1[0], p1[1]
    # print(x0, y0, x1, y1)
    if abs(x1 - x0) > abs(y1 - y0):
        if x0 > x1:
            p0, p1 = p1, p0

        ys = interpolate(p0[0], p0[1], p1[0], p1[1])
        for x in range(p0[0], p1[0]+1):
            putpixel(x, ys[x - p0[0]], color)

    else:
        if y0 > y1:
            p0, p1 = p1, p0
        xs = interpolate(p0[1], p0[0], p1[1], p1[0])
        for y in range(p0[1], p1[1]+1):
            putpixel(xs[y - p0[1]], y, color)


def drawTriangle(p0, p1, p2, color):
    drawLine(p0, p1, color)
    drawLine(p1, p2, color)
    drawLine(p2, p0, color)


def drawFilledTriangle(p0, p1, p2, color):

    if p0[1] > p1[1]:
        p0, p1 = p1, p0
    if p0[1] > p2[1]:
        p0, p2 = p2, p0
    if p1[1] > p2[1]:
        p1, p2 = p2, p1
    print(p0, p1)
    x01 = interpolate(p0[1], p0[0], p1[1], p1[0])
    x12 = interpolate(p1[1], p1[0], p2[1], p2[0])
    x02 = interpolate(p0[1], p0[0], p2[1], p2[0])

    print(len(x01), len(x02), len(x12))
    x012 = x01[:-1]+x12

    m = len(x012)//2
    if x012[m] < x02[m]:
        x_left = x012
        x_right = x02
    else:
        x_left = x02
        x_right = x012
    print(p0[1], p2[1])
    for y in range(p0[1], p2[1]+1):
        for x in range(int(x_left[y-p0[1]]), int(x_right[y-p0[1]])):
            putpixel(x, y, color)
    drawTriangle(p0, p1, p2, BACKGROUND_COLOR)
    return


# pygame.init()
# pygame.display.set_caption("Yeahhh Babyyy")
# done = False
# flag = False

# while not done:
#     screen.fill((255, 255, 255))
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             done = True
#     if not flag:
#         drawLine((-250, -250), (250, -250), (0, 255, 255))
#         pygame.display.update()

#         drawFilledTriangle((-200, -250), (200, 50), (20, 250), (255, 255, 0))
#         pygame.display.update()

#         drawFilledTriangle((0, 150), (0, 0), (-150, 0), (255, 0, 0))
#         pygame.display.update()

#         drawFilledTriangle((0, 150), (0, 0), (150, 0), (255, 0, 0))
#         pygame.display.update()

#         drawFilledTriangle((0, -150), (0, 0), (-150, 0), (255, 0, 0))
#         pygame.display.update()

#         drawFilledTriangle((0, -150), (0, 0), (150, 0), (255, 0, 0))
#         pygame.display.update()

#     flag = True
