from math import sqrt


class vec2:
    def __init__(self, x=0, y=0):
        self.x, self.y = (x, y)

    def __add__(self, other):
        return vec2(self.x+other.x, self.y+other.y)

    def __sub__(self, other):
        return vec2(self.x-other.x, self.y-other.y)

    def __mul__(self, scalar):
        return vec2(self.x*scalar, self.y*scalar)

    def __truediv__(self, scalar):
        return vec2(round(self.x/scalar, 2), round(self.y/scalar, 2))

    def __add__(self, other):
        return vec2(self.x+other.x, self.y+other.y)

    def len(self):
        return round(sqrt(self.x**2 + self.y**2), 2)

    def normalize(self):
        l = self.len()
        return vec2(round(self.x/(l), 2), round(self.y/(l), 2))

    def __repr__(self):
        return "vec2 ({},{}){\n}".format(self.x, self.y)


class vec3:
    def __init__(self, x=0, y=0, z=0):
        self.x, self.y, self.z = (x, y, z)

    def __add__(self, other):
        return vec3(self.x+other.x, self.y+other.y, self.z+other.z)

    def __sub__(self, other):
        return vec3(self.x-other.x, self.y-other.y, self.z-other.z)

    def __mul__(self, scalar):
        return vec3(self.x*scalar, self.y*scalar, self.z*scalar)

    def __truediv__(self, scalar):
        return vec3(round(self.x/scalar, 2), round(self.y/scalar, 2), round(self.z/scalar, 2))

    def __add__(self, other):
        return vec3(self.x+other.x, self.y+other.y, self.z+other.z)

    def len(self):
        return round(sqrt(self.x**2 + self.y**2 + self.z**2), 2)

    def __repr__(self):
        return "vec3 object({},{},{})".format(self.x, self.y, self.z)

    def normalize(self):
        l = self.len()
        return vec3(round(self.x/(l), 2), round(self.y/(l), 2), round(self.z/(l), 2))

    def dot(self, other):
        return self.x*other.x + self.y*other.y + self.z*other.z

    @classmethod
    def from_tuple(cls, t1):
        return cls(t1[0], t1[1], t1[2])


class vec4():
    def __init__(self, x=0, y=0, z=0, w=1):
        self.x = x
        self.y = y
        self.z = z
        self.w = w

    def __repr__(self):
        return "vec4 object({},{},{},{})".format(self.x, self.y, self.z, self.w)
