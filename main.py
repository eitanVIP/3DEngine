import Utils
from Engine import Engine
from Utils import Model, Triangle, Point, Rotation
from tkinter import filedialog


def main():
    cube = Model([
        # Front Face
        Triangle(Point(-0.5, 0.5, -0.5), Point(0.5, -0.5, -0.5), Point(-0.5, -0.5, -0.5)),
        Triangle(Point(-0.5, 0.5, -0.5), Point(0.5, 0.5, -0.5), Point(0.5, -0.5, -0.5)),

        # Right Face
        Triangle(Point(0.5, 0.5, -0.5), Point(0.5, -0.5, 0.5), Point(0.5, -0.5, -0.5)),
        Triangle(Point(0.5, 0.5, 0.5), Point(0.5, -0.5, 0.5), Point(0.5, 0.5, -0.5)),

        # Back Face
        Triangle(Point(0.5, 0.5, 0.5), Point(-0.5, -0.5, 0.5), Point(0.5, -0.5, 0.5)),
        Triangle(Point(0.5, 0.5, 0.5), Point(-0.5, 0.5, 0.5), Point(-0.5, -0.5, 0.5)),

        # Left Face
        Triangle(Point(-0.5, 0.5, 0.5), Point(-0.5, -0.5, -0.5), Point(-0.5, -0.5, 0.5)),
        Triangle(Point(-0.5, 0.5, 0.5), Point(-0.5, 0.5, -0.5), Point(-0.5, -0.5, -0.5)),

        # Top Face
        Triangle(Point(-0.5, 0.5, 0.5), Point(0.5, 0.5, -0.5), Point(-0.5, 0.5, -0.5)),
        Triangle(Point(-0.5, 0.5, 0.5), Point(0.5, 0.5, 0.5), Point(0.5, 0.5, -0.5)),

        # Bottom Face
        Triangle(Point(-0.5, -0.5, 0.5), Point(-0.5, -0.5, -0.5), Point(0.5, -0.5, 0.5)),
        Triangle(Point(0.5, -0.5, 0.5), Point(-0.5, -0.5, -0.5), Point(0.5, -0.5, -0.5)),
    ], Point(0, 0, 2), Rotation(0, 0, 0))

    # loadedModel = Utils.createModelFromFile(filedialog.askopenfilename(), Point(0, 0, 5), Rotation(0, 0, 0))
    loadedModel = Utils.createModelFromFile("C:\\Users\eitan\Desktop\Dragon.obj", Point(0, 0, 5), Rotation(0, 0, 0))

    engine = Engine(850, 850, 90, 72, "My 3D Engine")
    engine.addModel(loadedModel)

    while True:
        loadedModel.rotate(Rotation(0, 0.02, 0))

        engine.update()


if __name__ == "__main__":
    main()
