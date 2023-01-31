import pytest
import math
from main import *

def test_dot_init():
    dot = Dot(10, 20)
    assert dot.x == 10
    assert dot.y == 20

def test_game_init():
    game = Game()
    assert game.width == 800
    assert game.height == 600
    assert game.done == False
    assert game.dots == []
    assert game.lines == []
    assert game.start_dot == None
    assert game.current_dot == None
    assert game.route_distance == 0
    assert game.font is not None

def test_game_generate_dots():
    game = Game()
    game.generate_dots(5)
    assert len(game.dots) == 5
    for dot in game.dots:
        assert isinstance(dot, Dot)
    assert game.start_dot == game.dots[0]
    assert game.current_dot == game.dots[0]

def test_calculate_route_distance():
    game = Game()
    game.lines = [(10, 20), (20, 30), (30, 40)]
    game.calculate_route_distance()
    assert math.isclose(game.route_distance, 22.360679774997898, rel_tol=1e-9)

def test_nearest_neighbor():
    game = Game()
    game.dots = [Dot(10, 20), Dot(20, 30), Dot(30, 40)]
    game.start_dot = game.dots[0]
    game.nearest_neighbor()
    assert game.optimal_route == [game.dots[0], game.dots[1], game.dots[2]]

def test_calculate_optimal_distance():
    game = Game()
    game.optimal_route = [Dot(10, 20), Dot(20, 30), Dot(30, 40)]
    game.calculate_optimal_distance()
    assert math.isclose(game.optimal_distance, 44.72135954999579, rel_tol=1e-9)
