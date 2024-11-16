from Utils import Triangle, Model, Point, Vector
import math
import pygame


class Engine:
    def __init__(self, width: int, height: int, fov: float, fps: int, windowName: str):
        pygame.init()
        self.width = width
        self.height = height
        self.fps = fps
        self.screen = pygame.display.set_mode([width, height])
        pygame.display.set_caption(windowName)
        self.clock = pygame.time.Clock()
        self.drawLines = False

        self.models = []
        self.fov = fov
        self.F = 1 / math.tan(fov / 2)
        self.lightDir = Vector(0, 0, 1).getNormalized()

    def update(self):
        self.clock.tick(self.fps)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.finish()

        triangles2D = []
        colors = []

        for model in self.models:
            triangles = model.getTransformedTriangles()
            triangles.sort(reverse=True, key=lambda t: (t.p1.z + t.p2.z + t.p3.z) / 3)

            for triangle in triangles:
                if not self.isTriangleVisible(triangle):
                    continue

                triangles2D.append(self.projectTriangle(triangle))
                colors.append((0, self.calculateBrightness(triangle), 0))

        self.draw(triangles2D, colors, self.drawLines)

    def isTriangleVisible(self, triangle: Triangle):
        return (triangle.getNormal().x * triangle.p1.x +
                triangle.getNormal().y * triangle.p1.y +
                triangle.getNormal().z * triangle.p1.z < 0)

    def projectTriangle(self, triangle: Triangle):
        return Triangle(
                    Point(triangle.p1.x * self.F / triangle.p1.z, triangle.p1.y * self.F / triangle.p1.z, 0),
                    Point(triangle.p2.x * self.F / triangle.p2.z, triangle.p2.y * self.F / triangle.p2.z, 0),
                    Point(triangle.p3.x * self.F / triangle.p3.z, triangle.p3.y * self.F / triangle.p3.z, 0)
                )

    def calculateBrightness(self, triangle: Triangle):
        dot = triangle.getNormal().dot(self.lightDir.reverse())
        return abs(dot) * 255

    def draw(self, triangles2D: list[Triangle], colors: list, drawLines: bool):
        self.screen.fill((32, 28, 36))

        for i, triangle in enumerate(triangles2D):
            pygame.draw.polygon(self.screen, colors[i], triangle.toScreenSpace(self.width, self.height))

        if drawLines:
            for triangle in triangles2D:
                pygame.draw.line(self.screen, "red", triangle.p1.toScreenSpace(self.width, self.height),
                                 triangle.p2.toScreenSpace(self.width, self.height))
                pygame.draw.line(self.screen, "red", triangle.p2.toScreenSpace(self.width, self.height),
                                 triangle.p3.toScreenSpace(self.width, self.height))
                pygame.draw.line(self.screen, "red", triangle.p1.toScreenSpace(self.width, self.height),
                                 triangle.p3.toScreenSpace(self.width, self.height))

        pygame.display.flip()

    def finish(self):
        pygame.quit()

    def addModel(self, model: Model):
        self.models.append(model)
