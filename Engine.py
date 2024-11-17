from Utils import Triangle, Model, Point, Vector, Camera, Rotation
import math
import pygame


class Engine:
    def __init__(self, width: int, height: int, fov: float, fps: int, windowName: str):
        pygame.init()
        self.__width = width
        self.__height = height
        self.__fps = fps
        self.__screen = pygame.display.set_mode([width, height])
        pygame.display.set_caption(windowName)
        self.__clock = pygame.time.Clock()
        self.drawLines = False
        pygame.event.set_grab(True)
        pygame.mouse.set_visible(False)

        self.__models = []
        self.__fov = fov
        self.__F = 1 / math.tan(fov / 2)
        self.__lightDir = Vector(0, -1, 1).getNormalized()
        self.camera = Camera(Point(0, 0, 0), Rotation(0, 0, 0), self.__fov, 0.25)

    def update(self):
        self.__clock.tick(self.__fps)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.finish()

        triangles2D = []

        for model in self.__models:
            for triangle in model.getTransformedTriangles():
                if not self.__isTriangleVisible(triangle):
                    continue

                cameraTransformedTriangle = (triangle
                                             .move(-self.camera.position.x, -self.camera.position.y, -self.camera.position.z)
                                             .rotate(self.camera.rotation.inverse(yaw=False)))

                if self.__isTriangleBehindCamera(cameraTransformedTriangle):
                    continue

                triangle2D = self.__projectTriangle(cameraTransformedTriangle)
                triangle2D.color = self.__calculateColor(triangle)
                triangles2D.append(triangle2D)

        triangles2D.sort(reverse=True, key=lambda t: (t.p1.z + t.p2.z + t.p3.z) / 3)
        self.__draw(triangles2D, self.drawLines)

        delta_x, delta_y = pygame.mouse.get_rel()
        return pygame.key.get_pressed(), (float(delta_x), float(delta_y))

    def __isTriangleVisible(self, triangle: Triangle):
        return (triangle.getNormal().x * (triangle.p1.x - self.camera.position.x) +
                triangle.getNormal().y * (triangle.p1.y - self.camera.position.y) +
                triangle.getNormal().z * (triangle.p1.z - self.camera.position.z) < 0)

    def __isTriangleBehindCamera(self, cameraTransformedTriangle: Triangle):
        return max(cameraTransformedTriangle.getPoints(), key=lambda p: p.z).z <= self.camera.cullingDist

    def __projectTriangle(self, triangle: Triangle):
        return Triangle(
                    Point(triangle.p1.x * self.__F / triangle.p1.z, triangle.p1.y * self.__F / triangle.p1.z, triangle.p1.z),
                    Point(triangle.p2.x * self.__F / triangle.p2.z, triangle.p2.y * self.__F / triangle.p2.z, triangle.p2.z),
                    Point(triangle.p3.x * self.__F / triangle.p3.z, triangle.p3.y * self.__F / triangle.p3.z, triangle.p3.z),
                    triangle.color
                )

    def __calculateColor(self, triangle: Triangle):
        dot = triangle.getNormal().dot(self.__lightDir.reverse())
        return triangle.color * max(dot, 0)

    def __draw(self, triangles2D: list[Triangle], drawLines: bool):
        self.__screen.fill((32, 28, 36))

        for triangle in triangles2D:
            pygame.draw.polygon(self.__screen, triangle.color.getAsTuple(), triangle.toScreenSpace(self.__width, self.__height))

        if drawLines:
            for triangle in triangles2D:
                pygame.draw.line(self.__screen, "red", triangle.p1.toScreenSpace(self.__width, self.__height),
                                 triangle.p2.toScreenSpace(self.__width, self.__height))
                pygame.draw.line(self.__screen, "red", triangle.p2.toScreenSpace(self.__width, self.__height),
                                 triangle.p3.toScreenSpace(self.__width, self.__height))
                pygame.draw.line(self.__screen, "red", triangle.p1.toScreenSpace(self.__width, self.__height),
                                 triangle.p3.toScreenSpace(self.__width, self.__height))

        pygame.display.flip()

    def finish(self):
        pygame.quit()

    def addModel(self, model: Model):
        self.__models.append(model)
