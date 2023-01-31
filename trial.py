import pygame
import random
import math
import heapq

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
        pygame.draw.circle(surface, WHITE, (self.x, self.y), 6)


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
        self.IDAStar()

    def calculate_route_distance(self):
        """
        Calculates the total distance of the route taken by the player.
        """
        self.route_distance = 0
        for i in range(len(self.optimal_route) - 1):
            dot1 = self.optimal_route[i]
            dot2 = self.optimal_route[i + 1]
            distance = math.sqrt((dot2.x - dot1.x) ** 2 + (dot2.y - dot1.y) ** 2)
            self.route_distance += distance


    def heuristic_cost_estimate(self, dot):
        """
        Calculates the estimated cost from the current dot to the goal dot.

        Parameters:
            dot: Dot, the current dot.

        Returns:
            The estimated cost as a float.
        """
        goal_dot = self.dots[-1]
        x_distance = abs(dot.x - goal_dot.x)
        y_distance = abs(dot.y - goal_dot.y)
        return math.sqrt(x_distance ** 2 + y_distance ** 2)


    def IDAStar(self):
        """
        Finds the optimal route using the IDA* algorithm.
        """
        g_scores = {dot: float('inf') for dot in self.dots}
        f_scores = {dot: float('inf') for dot in self.dots}
        came_from = {dot: None for dot in self.dots}
        g_scores[self.start_dot] = 0
        f_scores[self.start_dot] = self.heuristic_cost_estimate(self.start_dot)
        heap = [(f_scores[self.start_dot], self.start_dot)]
        heapq.heapify(heap)

        while heap:
            current = heapq.heappop(heap)[1]
            if current == self.dots[-1]:
                optimal_route = [current]
                while came_from[current]:
                    current = came_from[current]
                    optimal_route.append(current)
                self.optimal_route = list(reversed(optimal_route))
                self.calculate_route_distance()
                return

            for neighbor in self.dots:
                if neighbor != current:
                    tent_g_score = g_scores[current] + math.sqrt(
                        (neighbor.x - current.x) ** 2 + (neighbor.y - current.y) ** 2)

                    if tent_g_score < g_scores[neighbor]:
                        came_from[neighbor] = current
                        g_scores[neighbor] = tent_g_score
                        f_scores[neighbor] = g_scores[neighbor] + self.heuristic_cost_estimate(neighbor)
                        heapq.heappush(heap, (f_scores[neighbor], neighbor))


    def run(self):
        """
        Runs the game loop.
        """
        self.generate_dots(5)
        while not self.done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.done = True

            self.screen.fill(BLACK)
            self.draw_dots()
            self.draw_route()
            self.draw_distance()
            pygame.display.flip()
            self.clock.tick(60)


    def draw_dots(self):
        """
        Draws the dots on the screen.
        """
        for dot in self.dots:
            dot.draw(self.screen)

    def draw_route(self):
        """
        Draws the route on the screen.
        """
        for i in range(len(self.optimal_route) - 1):
            dot1 = self.optimal_route[i]
            dot2 = self.optimal_route[i + 1]
            pygame.draw.line(self.screen, GREEN, (dot1.x, dot1.y), (dot2.x, dot2.y), 5)

    def draw_distance(self):
        """
        Draws the distance on the screen.
        """
        distance_text = self.font.render("Distance: {:.2f}".format(self.route_distance), True, WHITE)
        self.screen.blit(distance_text, (10, 10))


if __name__ == "__main__":
    game = Game()
    game.run()





