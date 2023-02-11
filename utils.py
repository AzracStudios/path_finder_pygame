from config import *
from cell import Cell


## UTILS ##
def get_neighbours(pos, _map, ignore_type="wall"):
    neighbours = [
        _map[pos[0] + 1 if pos[0] < MAP_SIZE - 1 else pos[0]][pos[1]],
        _map[pos[0] - 1 if pos[0] > 0 else pos[0]][pos[1]],
        _map[pos[0]][pos[1] + 1 if pos[1] < MAP_SIZE - 1 else pos[1]],
        _map[pos[0]][pos[1] - 1 if pos[1] > 0 else pos[1]],
    ]

    for i, neighbour in enumerate(neighbours):
        if neighbour == _map[pos[0]][pos[1]] or neighbour.type == ignore_type:
            del neighbours[i]

    return neighbours

def update_neighbours(_map):
    for row in _map:
        for cell in row:
            cell.neighbours = get_neighbours(cell.position, _map)

def flood_fill(pos, _map):
    node = _map[pos[0]][pos[1]]
    node.update_type("wall")
    node_neighbours = get_neighbours(pos, _map)

    for i in node_neighbours:
        if i.type == "empty":
            flood_fill(i.position, _map)

    return _map


## HELPER FUNCTIONS ##
def generate_map(cell_type="empty"):
    _map = []

    for i in range(MAP_SIZE):
        _map.append([])
        for j in range(MAP_SIZE):
            _map[i].append(Cell("empty", (i, j)))
            _map[i][j].update_type(cell_type)

    return _map


def render_frame(_map):
    for i in range(MAP_SIZE):
        for j in range(MAP_SIZE):
            pygame.draw.rect(SCREEN, _map[i][j].tile_color, _map[i][j].tile)

def reconstruct_path(came_from, current, render, clock):
    while current in came_from:
        clock.tick(60)
        current = came_from[current]
        current.update_type("path")
        render()