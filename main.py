import math

from Engine import Engine
from Utils import Model, Triangle, Point, Rotation


def main():
    model = Model([
        # Front Face
        Triangle(Point(-0.5, 0.5, -0.5), Point(0.5, -0.5, -0.5), Point(-0.5, -0.5, -0.5)),
        Triangle(Point(-0.5, 0.5, -0.5), Point(0.5, 0.5, -0.5), Point(0.5, -0.5, -0.5)),

        # Right Face
        Triangle(Point(0.5, 0.5, -0.5), Point(0.5, -0.5, 0.5), Point(0.5, -0.5, -0.5)),
        Triangle(Point(0.5, 0.5, 0.5), Point(0.5, -0.5, 0.5), Point(0.5, 0.5, -0.5)),

        # Back Face
        Triangle(Point(-0.5, 0.5, 0.5), Point(-0.5, -0.5, 0.5), Point(-0.5, 0.5, 0.5)),
        Triangle(Point(0.5, 0.5, 0.5), Point(-0.5, -0.5, 0.5), Point(0.5, -0.5, 0.5)),

        # Left Face
        Triangle(Point(-0.5, 0.5, 0.5), Point(-0.5, 0.5, -0.5), Point(-0.5, -0.5, -0.5)),
        Triangle(Point(-0.5, 0.5, 0.5), Point(-0.5, -0.5, 0.5), Point(-0.5, -0.5, -0.5)),

        # Top Face
        Triangle(Point(-0.5, 0.5, 0.5), Point(0.5, 0.5, -0.5), Point(-0.5, 0.5, -0.5)),
        Triangle(Point(-0.5, 0.5, 0.5), Point(0.5, 0.5, 0.5), Point(0.5, 0.5, -0.5)),

        # Bottom Face
        Triangle(Point(-0.5, -0.5, 0.5), Point(-0.5, -0.5, -0.5), Point(0.5, -0.5, 0.5)),
        Triangle(Point(0.5, -0.5, 0.5), Point(-0.5, -0.5, -0.5), Point(0.5, -0.5, -0.5)),
    ], Point(0, 0, 2), Rotation(0, 0, 0))

    engine = Engine(850, 850, 90, 72)
    engine.addModel(model)

    while True:
        # model.moveTo(math.cos(x), math.sin(x), math.sin(x) + 1.5)
        model.rotate(Rotation(0.01, 0.01 * 2, 0.01 * 3))

        engine.update()


if __name__ == "__main__":
    main()
