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

    loadedModel = Utils.createModelFromFile(filedialog.askopenfilename(), Point(0, 0, 4), Rotation(0, math.pi, 0))

    engine = Engine(1080, 1080, 90, 72, "My 3D Engine")
    engine.addModel(loadedModel)
    # engine.addModel(cube)

    while True:
        keys, mouse = engine.update()

        loadedModel.rotate(Rotation(0, 0.02, 0))

        if keys[pygame.K_w]:
            engine.camera.move(Vector(0, 0, 0.2))
        if keys[pygame.K_s]:
            engine.camera.move(Vector(0, 0, -0.2))
        if keys[pygame.K_d]:
            engine.camera.move(Vector(0.2, 0, 0))
        if keys[pygame.K_a]:
            engine.camera.move(Vector(-0.2, 0, 0))
        if keys[pygame.K_e]:
            engine.camera.move(Vector(0, 0.2, 0))
        if keys[pygame.K_q]:
            engine.camera.move(Vector(0, -0.2, 0))
        if keys[pygame.K_UP]:
            engine.camera.rotate(Rotation(0.04, 0, 0))
        if keys[pygame.K_DOWN]:
            engine.camera.rotate(Rotation(-0.04, 0, 0))
        if keys[pygame.K_RIGHT]:
            engine.camera.rotate(Rotation(0, 0.04, 0))
        if keys[pygame.K_LEFT]:
            engine.camera.rotate(Rotation(0, -0.04, 0))

        # print(mouse[1] / 50, mouse[0] / 50)
        # engine.camera.rotate(Rotation(mouse[1] / 50, mouse[0] / 50, 0))


if __name__ == "__main__":
    main()
