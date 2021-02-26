
from vector_class import vec2, vec3, vec4
import math
import pygame
import time

IDENTITY4 = [[1, 0, 0, 0],
             [0, 1, 0, 0],
             [0, 0, 1, 0],
             [0, 0, 0, 1]
             ]
# class transform:
#     def __init__(self):
#         self.scale = 1
#         self.rotation = vec3()
#         self.translation = vec3()


def makeOYRotationMatrix(degrees):
    cos = round(math.cos(degrees*math.pi/180.0), 2)
    sin = round(math.sin(degrees*math.pi/180.0), 2)

    return [[cos, 0, -sin, 0],
            [0, 1,    0, 0],
            [sin, 0,  cos, 0],
            [0, 0,    0, 1]]


class Camera:
    def __init__(self, position=vec3(), orientation=IDENTITY4):
        self.position = position
        self.orientation = orientation


camera = Camera()

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

# make a translation matrix


def putpixel(Cx, Cy, color):
    Sx = (Cw/2)+Cx
    Sy = (Ch/2)-Cy
    pygame.draw.circle(screen, color, (Sx, Sy), 1)


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
    if type(color) == vec3:
        color = (color.x, color.y, color.z)
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


def makeTranslationMatrix(translate):
    return [[1, 0, 0, translate.x],
            [0, 1, 0, translate.y],
            [0, 0, 1, translate.z],
            [0, 0, 0, 1]
            ]


# make a scaling matrix
def makeScalingMatrix(scaling):
    return [[scaling, 0, 0, 0],
            [0, scaling, 0, 0],
            [0, 0, scaling, 0],
            [0, 0, 0, 1]
            ]


# multiplies two 4x4 matrices
def multiplyMM4(matA, matB):
    result = [[0, 0, 0, 0],
              [0, 0, 0, 0],
              [0, 0, 0, 0],
              [0, 0, 0, 0]
              ]

    for i in range(4):
        for j in range(4):
            for k in range(4):
                result[i][j] += matA[i][k]*matB[k][j]
    return result


# multiplies a 4x4 matrix and a 4D vector
def multiplyMV(mat4x4, vector4):
    result = [0, 0, 0, 0]
    vec = [vector4.x, vector4.y, vector4.z, vector4.w]
    for i in range(4):
        for j in range(4):
            result[i] += mat4x4[i][j]*vec[j]
    return vec4(result[0], result[1], result[2], result[3])


# transpose a 4x4 matrix
def transposed(mat):
    result = [[0, 0, 0, 0],
              [0, 0, 0, 0],
              [0, 0, 0, 0],
              [0, 0, 0, 0]
              ]
    for i in range(4):
        for j in range(4):
            result[i][j] = mat[j][i]
    return result


class scene():
    instances = []

    @classmethod
    def add_to_scene(cls, object):
        cls.instances.append(object)


class instance():
    def __init__(self, obj, position=vec3(), orientation=IDENTITY4, scale=1):
        self.model = obj
        self.position = position
        self.orientation = orientation
        self.scale = scale
        self.transform = multiplyMM4(makeTranslationMatrix(self.position), multiplyMM4(
            self.orientation, makeScalingMatrix(self.scale)))
        scene.add_to_scene(self)

    def translate(self, pos):
        self.position += pos
        self.transform = multiplyMM4(makeTranslationMatrix(self.position), multiplyMM4(
            self.orientation, makeScalingMatrix(self.scale)))

    def rotate(self, rot):
        self.orientation = makeOYRotationMatrix(rot)
        self.transform = multiplyMM4(makeTranslationMatrix(self.position), multiplyMM4(
            self.orientation, makeScalingMatrix(self.scale)))


class cube():
    red = (255, 0, 0)
    green = (0, 255, 0)
    blue = (0, 0, 255)
    yellow = (255, 255, 0)
    purple = (128, 0, 128)
    cyan = (255, 0, 255)

    def __init__(self):

        self.vertices = [vec3(1,  1,  1),
                         vec3(-1,  1,  1),
                         vec3(-1, -1,  1),
                         vec3(1, -1,  1),
                         vec3(1,  1, -1),
                         vec3(-1,  1, -1),
                         vec3(-1, -1, -1),
                         vec3(1, -1, -1)
                         ]
        self.triangles = [
            [vec3(0, 1, 2), cube.red],
            [vec3(0, 2, 3), cube.red],
            [vec3(4, 0, 3), cube.green],
            [vec3(4, 3, 7), cube.green],
            [vec3(5, 4, 7), cube.blue],
            [vec3(5, 7, 6), cube.blue],
            [vec3(1, 5, 6), cube.yellow],
            [vec3(1, 6, 2), cube.yellow],
            [vec3(4, 5, 1), cube.purple],
            [vec3(4, 1, 0), cube.purple],
            [vec3(2, 6, 7), cube.cyan],
            [vec3(2, 7, 3), cube.cyan]]


def DrawWireframeTriangle(p0, p1, p2, color):
    drawLine(p0, p1, color)
    drawLine(p1, p2, color)
    drawLine(p2, p0, color)


def RenderTriangle(triangle, projected):
    DrawWireframeTriangle(projected[triangle[0].x],
                          projected[triangle[0].y],
                          projected[triangle[0].z],
                          triangle[1])


def RenderModel(model, transform):
    projected = []
    for V in model.vertices:
        vh = vec4(V.x, V.y, V.z, 1)
        projected.append(ProjectVertex(multiplyMV(transform, vh)))

    for T in model.triangles:
        RenderTriangle(T, projected)


def RenderScene():
    M_camera = multiplyMM4(transposed(
        camera.orientation), makeTranslationMatrix(camera.position*(-1)))

    for I in scene.instances:
        M = multiplyMM4(M_camera, I.transform)
        RenderModel(I.model, M)


pygame.init()
pygame.display.set_caption("rasterisation Projection")
done = False
flag = False

instance(cube(), position=vec3(1, 2, 39))
instance(cube(), position=vec3(-2, 0, 38))
i = 0
while not done:
    screen.fill((255, 255, 255))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    if i < 360:
        RenderScene()
        scene.instances[0].rotate(i)
        # scene.instances[0].translate(vec3(0.1, 0.1, 0))
        # scene.instances[1].translate(vec3(0, 0, 0.1))
        pygame.display.update()
        i += 0.5
