from Utils import Triangle, Model, Point, Vector, Camera, Rotation
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
        pygame.event.set_grab(True)
        pygame.mouse.set_visible(False)

        self.models = []
        self.fov = fov
        self.F = 1 / math.tan(fov / 2)
        self.lightDir = Vector(0, -1, 1).getNormalized()
        self.camera = Camera(Point(0, 0, 0), Rotation(0, 0, 0), self.fov)

    def update(self):
        self.clock.tick(self.fps)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.finish()

        triangles2D = []

        for model in self.models:
            for triangle in model.getTransformedTriangles():
                if not self.isTriangleVisible(triangle):
                    continue

                cameraTransformedTriangle = (triangle
                                             .move(-self.camera.position.x, -self.camera.position.y, -self.camera.position.z)
                                             .rotate(self.camera.rotation.inverse(yaw=False)))

                triangle2D = self.projectTriangle(cameraTransformedTriangle)
                triangle2D.color = self.calculateColor(triangle)
                triangles2D.append(triangle2D)

        triangles2D.sort(reverse=True, key=lambda t: (t.p1.z + t.p2.z + t.p3.z) / 3)
        self.draw(triangles2D, self.drawLines)

        delta_x, delta_y = pygame.mouse.get_rel()
        return pygame.key.get_pressed(), (float(delta_x), float(delta_y))

    def isTriangleVisible(self, triangle: Triangle):
        return (triangle.getNormal().x * (triangle.p1.x - self.camera.position.x) +
                triangle.getNormal().y * (triangle.p1.y - self.camera.position.y) +
                triangle.getNormal().z * (triangle.p1.z - self.camera.position.z) < 0)

    def projectTriangle(self, triangle: Triangle):
        return Triangle(
                    Point(triangle.p1.x * self.F / triangle.p1.z, triangle.p1.y * self.F / triangle.p1.z, triangle.p1.z),
                    Point(triangle.p2.x * self.F / triangle.p2.z, triangle.p2.y * self.F / triangle.p2.z, triangle.p2.z),
                    Point(triangle.p3.x * self.F / triangle.p3.z, triangle.p3.y * self.F / triangle.p3.z, triangle.p3.z),
                    triangle.color
                )

    def calculateColor(self, triangle: Triangle):
        dot = triangle.getNormal().dot(self.lightDir.reverse())
        return triangle.color * max(dot, 0)

    def draw(self, triangles2D: list[Triangle], drawLines: bool):
        self.screen.fill((32, 28, 36))

        for triangle in triangles2D:
            pygame.draw.polygon(self.screen, triangle.color.getAsTuple(), triangle.toScreenSpace(self.width, self.height))

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
