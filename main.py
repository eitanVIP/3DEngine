import math
import time

import pygame

import Utils
from Engine import Engine
from Utils import Model, Triangle, Point, Rotation, Vector
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

    engine = Engine(1080, 1080, 90, 144, "My 3D Engine")

    # loadedModel = Utils.createModelFromFile(filedialog.askopenfilename(), Point(0, 0, 6), Rotation(0, math.pi, 0))
    # engine.addModel(loadedModel)
    engine.addModel(cube)
    speed = 0.1
    sensitivity = 1 / 800

    while True:
        keys, mouse = engine.update()

        cube.rotate(Rotation(0, 0.02, 0))

        if keys[pygame.K_w]:
            engine.camera.move(Vector(0, 0, speed))
        if keys[pygame.K_s]:
            engine.camera.move(Vector(0, 0, -speed))
        if keys[pygame.K_d]:
            engine.camera.move(Vector(speed, 0, 0))
        if keys[pygame.K_a]:
            engine.camera.move(Vector(-speed, 0, 0))
        if keys[pygame.K_e] or keys[pygame.K_SPACE]:
            engine.camera.move(Vector(0, speed, 0))
        if keys[pygame.K_q] or keys[pygame.K_LCTRL]:
            engine.camera.move(Vector(0, -speed, 0))

        engine.camera.rotate(Rotation(mouse[1] * -sensitivity, mouse[0] * sensitivity, 0))


if __name__ == "__main__":
    main()
