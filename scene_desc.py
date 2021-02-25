
from vector_class import vec3


class transform:
    def __init__(self):
        self.scale = 1
        self.rotation = vec3()
        self.translation = vec3()


class scene:
    instances = []

    @classmethod
    def add_to_scene(cls, object):
        cls.instances.append(object)


class instance:
    def __init__(self, obj):
        self.model = obj
        self.transform = transform()
        scene.add_to_scene(self)


class cube:
    red = (255, 0, 0)
    green = (0, 255, 0)
    blue = (0, 0, 255)
    yellow = (255, 255, 0)
    purple = (128, 0, 128)
    cyan = (255, 0, 255)

    def __init__(self, position=vec3()):

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
        self.position = position


def RenderObject(vertices, triangles):
    projected = []
    for V in vertices:
        projected.append(ProjectVertex(V))
    for T in triangles:
        RenderTriangle(T, projected)


def RenderTriangle(triangle, projected):
    DrawWireframeTriangle(projected[triangle[0].x],
                          projected[triangle[0].y],
                          projected[triangle[0].z],
                          triangle[1])


def RenderModel(model, transform):
    projected = []
    for V in model.vertices:
        projected.append(ProjectVertex(transform * V))

    for T in model.triangles:
        RenderTriangle(T, projected)


def RenderScene():
    M_camera = MakeCameraMatrix(camera.position, camera.orientation)

    for I in scene.instances:
        M = I.transform * M_camera
        RenderModel(I.model, M)


def ApplyTransform(vertex, transform):
    scaled = Scale(vertex, transform.scale)
    rotated = Rotate(scaled, transform.rotation)
    translated = Translate(rotated, transform.translation)
    return translated


def RenderInstance(instance):
    projected = []
    model = instance.model
    for V in model.vertices:
        V_dash = ApplyTransform(V, instance.transform)
        projected.append(ProjectVertex(V_dash))
    for T in model.triangles:
        RenderTriangle(T, projected)
