import pygame
import random
import math

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

class Dot():
    """
    A class that represents a dot in the game.
    It has two attributes x and y to represent the coordinates of the dot on the screen.
    """

    def __init__(self, x, y):
        """
        Initialize a new instance of the Dot class.

        Parameters:
            x: int, the x-coordinate of the dot on the screen.
            y: int, the y-coordinate of the dot on the screen.
        """
        self.x = x
        self.y = y

    def draw(self, surface):
        """
        Draw the dot on the surface.

        Parameters:
            surface: the surface on which the dot is drawn.
        """
        pygame.draw.circle(surface, WHITE, (self.x, self.y), 6.9)

class Game():
    """
    A class that represents the game.
    """
    def __init__(self):
        """
        Initialize a new instance of the Game class.
        """
        pygame.init()
        self.width = 800
        self.height = 600
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Dot Game")
        self.clock = pygame.time.Clock()
        self.done = False
        self.dots = []
        self.lines = []
        self.start_dot = None
        self.current_dot = None
        self.route_distance = 0
        self.font = pygame.font.SysFont(None, 25)
        self.optimal_lines = []

    def generate_dots(self, num_dots):
        """
        Generates random dots on the screen.

        Parameters:
            num_dots: int, the number of dots to generate.
        """
        for i in range(num_dots):
            x = random.randint(20, self.width - 20)
            y = random.randint(20, self.height - 20)
            dot = Dot(x, y)
            self.dots.append(dot)
        self.start_dot = self.dots[0]
        self.current_dot = self.start_dot

    def calculate_route_distance(self):
        """
        Calculates the total distance of the route taken by the player.
        """
        self.route_distance = 0
        for i in range(len(self.lines) - 1):
            line1 = self.lines[i]
            line2 = self.lines[i + 1]
            distance = math.sqrt((line2[0] - line1[0]) ** 2 + (line2[1] - line1[1]) ** 2)
            self.route_distance += distance

    def nearest_neighbor(self):
        """
        Finds the optimal route according to the nearest neighbor algorithm.
        """
        optimal_route = []
        unvisited_dots = self.dots.copy()
        current_dot = self.start_dot
        optimal_route.append(current_dot)
        unvisited_dots.remove(current_dot)
        while unvisited_dots:
            closest_dot = None
            closest_distance = None
            for dot in unvisited_dots:
                distance = math.sqrt((dot.x - current_dot.x) ** 2 + (dot.y - current_dot.y) ** 2)
                if closest_distance is None or distance < closest_distance:
                    closest_distance = distance
                    closest_dot = dot
            optimal_route.append(closest_dot)
            unvisited_dots.remove(closest_dot)
            current_dot = closest_dot
        self.optimal_route = optimal_route
        self.optimal_lines = []
        for i in range(len(self.optimal_route)):
            if i + 1 < len(self.optimal_route):
                dot1 = self.optimal_route[i]
                dot2 = self.optimal_route[i + 1]
                line = pygame.draw.line(self.screen, GREEN, (dot1.x, dot1.y), (dot2.x, dot2.y))
                self.optimal_lines.append(line)

    def calculate_optimal_distance(self):
        """
        Calculates the total distance of the optimal route.
        """
        self.optimal_distance = 0
        for i in range(len(self.optimal_route)):
            if i + 1 < len(self.optimal_route):
                dot1 = self.optimal_route[i]
                dot2 = self.optimal_route[i + 1]
                distance = math.sqrt((dot2.x - dot1.x) ** 2 + (dot2.y - dot1.y) ** 2)
                self.optimal_distance += distance
        self.optimal_distance += math.sqrt(
            (self.start_dot.x - self.optimal_route[-1].x) ** 2 + (self.start_dot.y - self.optimal_route[-1].y) ** 2)

    def animate_optimal_route(self):
        """
        Animates the optimal route on the screen.
        """
        for i in range(1, len(self.optimal_route)):
            dot1 = self.optimal_route[i - 1]
            dot2 = self.optimal_route[i]
            pygame.draw.line(self.screen, BLUE, (dot1.x, dot1.y), (dot2.x, dot2.y), 2)
            pygame.display.update()
            self.clock.tick(3)

    def run(self):
        """
        The main game loop that handles the game logic and event handling.
        """
        self.generate_dots(5)
        while not self.done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.done = True
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    for dot in self.dots:
                        if math.sqrt((dot.x - pos[0]) ** 2 + (dot.y - pos[1]) ** 2) <= 6.9:
                            if self.current_dot != dot:
                                self.lines.append((self.current_dot.x, self.current_dot.y))
                                self.lines.append((dot.x, dot.y))
                                self.current_dot = dot
                                if dot == self.start_dot:
                                    self.calculate_route_distance()
                                    self.nearest_neighbor()
                                    self.calculate_optimal_distance()
                                    self.animate_optimal_route()

            self.screen.fill(BLACK)

            for dot in self.dots:
                dot.draw(self.screen)

            pygame.draw.circle(self.screen, GREEN, (self.start_dot.x, self.start_dot.y), 6.9)

            if len(self.lines) > 0:
                pygame.draw.lines(self.screen, RED, False, self.lines, 2)
                if len(self.lines) > 2:
                    if self.current_dot == self.start_dot:
                        route_distance_text = self.font.render("Route Distance: " + str(round(self.route_distance, 2)),
                                                               True, WHITE)
                        optimal_distance_text = self.font.render("Optimal Distance: " + str(round(self.optimal_distance, 2)), True, WHITE)
                        self.screen.blit(route_distance_text, [self.width / 2 - 100, self.height / 2 - 50])
                        self.screen.blit(optimal_distance_text, [self.width / 2 - 100, self.height / 2 - 25])

                        if self.route_distance > self.optimal_distance:
                            difference_text = self.font.render(
                                "Difference: " + str(round(self.route_distance - self.optimal_distance, 2)), True,
                                WHITE)

                            self.screen.blit(difference_text, [self.width / 2 - 100, self.height / 2])
            for line in self.optimal_lines:
                pygame.draw.line(self.screen, GREEN, line[0], line[1])

            pygame.display.flip()
            self.clock.tick(60)

game = Game()
game.run()
pygame.quit()
