import math
import random

import pywavefront


class Vector:
    def __init__(self, x: float, y: float, z: float):
        self.x = x
        self.y = y
        self.z = z

    def dot(self, other):
        return (self.x * other.x) + (self.y * other.y) + (self.z * other.z)

    def getMagnitude(self):
        return math.hypot(self.x, self.y, self.z)

    def getNormalized(self):
        return Vector(self.x / self.getMagnitude(), self.y / self.getMagnitude(), self.z / self.getMagnitude())

    def cross(self, other):
        return Vector(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x,
        )

    def reverse(self):
        return Vector(-self.x, -self.y, -self.z)

    def __mul__(self, other):
        return Vector(self.x * other, self.y * other, self.z * other)

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y, self.z + other.z)

    def __repr__(self):
        return f"Vector: x{self.x}, y{self.y}, z{self.z}"


class Rotation:
    def __init__(self, pitch: float, yaw: float, roll: float):
        self.pitch = pitch
        self.yaw = yaw
        self.roll = roll

    def __iadd__(self, other):
        return Rotation(self.pitch + other.pitch, self.yaw + other.yaw, self.roll + other.roll)

    def __repr__(self):
        return f"Rotation: pitch{self.pitch}, yaw{self.yaw}, roll{self.roll}"

    def inverse(self, pitch=True, yaw=True, roll=True):
        return Rotation(-self.pitch if pitch else self.pitch, -self.yaw if yaw else self.yaw, -self.roll if roll else self.roll)


class Point:
    def __init__(self, x: float, y: float, z: float):
        self.x = x
        self.y = y
        self.z = z

    def move(self, x: float, y: float, z: float):
        return Point(self.x + x, self.y + y, self.z + z)

    def rotate(self, rotation: Rotation):
        rotatedPoint = Point(self.x, self.y, self.z)

        # Apply yaw (rotation around Y-axis)
        x, z = rotatedPoint.x, rotatedPoint.z
        cos_yaw, sin_yaw = math.cos(rotation.yaw), math.sin(rotation.yaw)
        rotatedPoint.x = x * cos_yaw - z * sin_yaw
        rotatedPoint.z = x * sin_yaw + z * cos_yaw

        # Apply pitch (rotation around X-axis)
        y, z = rotatedPoint.y, rotatedPoint.z
        cos_pitch, sin_pitch = math.cos(rotation.pitch), math.sin(rotation.pitch)
        rotatedPoint.y = y * cos_pitch - z * sin_pitch
        rotatedPoint.z = y * sin_pitch + z * cos_pitch

        # Apply roll (rotation around Z-axis)
        x, y = rotatedPoint.x, rotatedPoint.y
        cos_roll, sin_roll = math.cos(rotation.roll), math.sin(rotation.roll)
        rotatedPoint.x = x * cos_roll - y * sin_roll
        rotatedPoint.y = x * sin_roll + y * cos_roll

        return rotatedPoint

    def toScreenSpace(self, width, height):
        return width / 2 + self.x * width, height / 2 - self.y * height

    def __sub__(self, other):
        return Vector(
            self.x - other.x,
            self.y - other.y,
            self.z - other.z
        )

    def __add__(self, other):
        return Point(
            self.x + other.x,
            self.y + other.y,
            self.z + other.z
        )

    def __repr__(self):
        return f"Point: x{self.x}, y{self.y}, z{self.z}"


class Color:
    def __init__(self, r: int, g: int, b: int):
        self.r = r
        self.g = g
        self.b = b

    def __mul__(self, other):
        return Color(self.r * other, self.g * other, self.b * other)

    def __eq__(self, other):
        return self.r == other.r and self.g == other.g and self.b == other.b

    def getAsTuple(self):
        return self.r, self.g, self.b

    @staticmethod
    def random():
        return Color(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))


class Triangle:
    def __init__(self, p1: Point, p2: Point, p3: Point, color: Color = Color(0, 255, 0)):
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        self.color = color
        if(self.color == Color(0, 255, 0)):
            self.color = Color.random()

    def getPoints(self):
        return [self.p1, self.p2, self.p3]

    def move(self, x: float, y: float, z: float):
        return Triangle(
            self.p1.move(x, y, z),
            self.p2.move(x, y, z),
            self.p3.move(x, y, z),
            self.color
        )

    def rotate(self, rotation: Rotation):
        return Triangle(
            self.p1.rotate(rotation),
            self.p2.rotate(rotation),
            self.p3.rotate(rotation),
            self.color
        )

    def toScreenSpace(self, width, height):
        return [
            self.p1.toScreenSpace(width, height),
            self.p2.toScreenSpace(width, height),
            self.p3.toScreenSpace(width, height)
        ]

    def getNormal(self):
        A = self.p2 - self.p1
        B = self.p3 - self.p1
        return A.cross(B).getNormalized()

    def __repr__(self):
        return f"Triangle: p1- {self.p1}, p2- {self.p2}, p3- {self.p3}"


class Model:
    def __init__(self, triangles: list[Triangle], position: Point, rotation: Rotation):
        self.triangles: list[Triangle] = triangles
        self.position: Point = position
        self.rotation: Rotation = rotation

    def getTransformedTriangles(self):
        return [t.rotate(self.rotation).move(self.position.x, self.position.y, self.position.z) for t in self.triangles]

    def moveTo(self, x: float, y: float, z: float):
        self.position = Point(x, y, z)

    def move(self, x: float, y: float, z: float):
        self.position = self.position.move(x, y, z)

    def rotate(self, rotation: Rotation):
        self.rotation += rotation

    def rotateTo(self, rotation: Rotation):
        self.rotation = rotation


class Camera:
    def __init__(self, position: Point, rotation: Rotation, fov: float, cullingDist: float):
        self.position = position
        self.rotation = rotation
        self.fov = fov
        self.cullingDist = cullingDist

    def move(self, translation: Vector):
        translation = (self.getRight() * translation.x +
                       self.getUp() * translation.y +
                       self.getForward() * translation.z)
        self.position += translation

    def rotate(self, rotation: Rotation):
        self.rotation += rotation.inverse(yaw=False)

    def getForward(self):
        return Vector(
            math.cos(self.rotation.pitch) * math.sin(self.rotation.yaw),
            -math.sin(self.rotation.pitch),
            math.cos(self.rotation.pitch) * math.cos(self.rotation.yaw)
        )

    def getRight(self):
        return Vector(
            math.cos(self.rotation.yaw) * math.cos(self.rotation.roll),
            math.sin(self.rotation.roll),
            -math.sin(self.rotation.yaw) * math.cos(self.rotation.roll)
        )

    def getUp(self):
        return self.getForward().cross(self.getRight())


def createModelFromFile(filePath: str, position: Point, rotation: Rotation):
    obj = pywavefront.Wavefront(filePath, collect_faces=True)

    triangles = []
    for face in obj.mesh_list[0].faces:
        triangles.append(Triangle(
            Point(obj.vertices[face[0]][0], obj.vertices[face[0]][1], obj.vertices[face[0]][2]),
            Point(obj.vertices[face[1]][0], obj.vertices[face[1]][1], obj.vertices[face[1]][2]),
            Point(obj.vertices[face[2]][0], obj.vertices[face[2]][1], obj.vertices[face[2]][2])
        ))

    return Model(triangles, position, rotation)
