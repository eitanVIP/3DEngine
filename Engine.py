import math

import pygame

from Utils import Triangle, Model, Line, Point


class Engine:
    def __init__(self, width: int, height: int, fov: float, fps: int):
        pygame.init()
        self.width = width
        self.height = height
        self.fps = fps
        self.screen = pygame.display.set_mode([width, height])
        self.clock = pygame.time.Clock()

        self.models = []
        self.fov = fov
        self.F = 1 / math.tan(fov / 2)

    def update(self):
        self.clock.tick(self.fps)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.finish()

        triangles2D = []

        for model in self.models:
            for triangle in model.getTransformedTriangles():
                triangles2D.append(Triangle(
                    Point(triangle.p1.x * self.F / triangle.p1.z, triangle.p1.y * self.F / triangle.p1.z, 0),
                    Point(triangle.p2.x * self.F / triangle.p2.z, triangle.p2.y * self.F / triangle.p2.z, 0),
                    Point(triangle.p3.x * self.F / triangle.p3.z, triangle.p3.y * self.F / triangle.p3.z, 0)
                ))

        self.draw(triangles2D)

    def draw(self, triangles2D: list[Triangle]):
        self.screen.fill((32, 28, 36))

        for triangle in triangles2D:
            pygame.draw.polygon(self.screen, "darkgreen", triangle.toScreenSpace(self.width, self.height))

        for triangle in triangles2D:
            pygame.draw.line(self.screen, "green", triangle.p1.toScreenSpace(self.width, self.height), triangle.p2.toScreenSpace(self.width, self.height))
            pygame.draw.line(self.screen, "green", triangle.p2.toScreenSpace(self.width, self.height), triangle.p3.toScreenSpace(self.width, self.height))
            pygame.draw.line(self.screen, "green", triangle.p1.toScreenSpace(self.width, self.height), triangle.p3.toScreenSpace(self.width, self.height))

        pygame.display.flip()

    def finish(self):
        pygame.quit()

    def addModel(self, model: Model):
        self.models.append(model)
