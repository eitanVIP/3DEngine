import math


class Rotation:
    def __init__(self, pitch: float, yaw: float, roll: float):
        self.pitch = pitch
        self.yaw = yaw
        self.roll = roll

    def __iadd__(self, other):
        return Rotation(self.pitch + other.pitch, self.yaw + other.yaw, self.roll + other.roll)


class Point:
    def __init__(self, x: float, y: float, z: float):
        self.x = x
        self.y = y
        self.z = z

    def move(self, x: float, y: float, z: float):
        return Point(self.x + x, self.y + y, self.z + z)

    def rotate(self, rotation: Rotation):
        cosa = math.cos(rotation.pitch)
        sina = math.sin(rotation.pitch)

        cosb = math.cos(rotation.yaw)
        sinb = math.sin(rotation.yaw)

        cosc = math.cos(rotation.roll)
        sinc = math.sin(rotation.roll)

        Axx = cosa * cosb
        Axy = cosa * sinb * sinc - sina * cosc
        Axz = cosa * sinb * cosc + sina * sinc

        Ayx = sina * cosb
        Ayy = sina * sinb * sinc + cosa * cosc
        Ayz = sina * sinb * cosc - cosa * sinc

        Azx = -sinb
        Azy = cosb * sinc
        Azz = cosb * cosc

        return Point(
            Axx * self.x + Axy * self.y + Axz * self.z,
            Ayx * self.x + Ayy * self.y + Ayz * self.z,
            Azx * self.x + Azy * self.y + Azz * self.z
        )

    def toScreenSpace(self, width, height):
        return width / 2 + self.x * width, height / 2 - self.y * height


class Line:
    def __init__(self, p1: Point, p2: Point):
        self.p1 = p1
        self.p2 = p2


class Triangle:
    def __init__(self, p1: Point, p2: Point, p3: Point):
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3

    def move(self, x: float, y: float, z: float):
        return Triangle(self.p1.move(x, y, z), self.p2.move(x, y, z), self.p3.move(x, y, z))

    def rotate(self, rotation: Rotation):
        return Triangle(
            self.p1.rotate(rotation),
            self.p2.rotate(rotation),
            self.p3.rotate(rotation)
        )

    def toScreenSpace(self, width, height):
        return [
            self.p1.toScreenSpace(width, height),
            self.p2.toScreenSpace(width, height),
            self.p3.toScreenSpace(width, height)
        ]


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
