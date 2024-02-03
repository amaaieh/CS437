import numpy as np

def astar_numpy(bit_array, start, end):
    start = (start[1], start[0])
    end = (end[1], end[0])

    def heuristic(a, b):
        return np.sqrt((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2)

    def get_neighbors(current_node):
        neighbors = []
        for d in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            neighbor = (current_node[0] + d[0], current_node[1] + d[1])
            if 0 <= neighbor[0] < bit_array.shape[0] and 0 <= neighbor[1] < bit_array.shape[1] and bit_array[neighbor[0], neighbor[1]] == 0:
                neighbors.append(neighbor)
        return neighbors

    open_list = [start]
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, end)}

    while open_list:
        current = min(open_list, key=lambda x: f_score[x])

        if current == end:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            p = path[::-1]
            new_path = []
            for tup in p:
              new_tup = (tup[1], tup[0])
              new_path.append(new_tup)
            return new_path

        open_list.remove(current)
        for neighbor in get_neighbors(current):
            tentative_g_score = g_score[current] + 1
            if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + heuristic(neighbor, end)
                if neighbor not in open_list:
                    open_list.append(neighbor)
                    
    return None