from PIL import Image
from PIL import ImageColor
from random import shuffle, randrange
import sys

N = 1
E = 2
S = 8
W = 4
DIRECTIONS = {
    N: (0, -1),
    E: (1, 0),
    S: (0, 1),
    W: (-1, 0)
}

def draw_maze(maze, w, h, start_and_end = False, cell_list = []):
    picture = Image.new("RGB", (4*w + 1, 4*h + 1), "#000")
    for i in range(w):
        for j in range(h):
            x = 4 * i + 2
            y = 4 * j + 2
            picture.putpixel( (x, y), (255, 255, 255))

            # Corners
            picture.putpixel( (x-1, y-1), (0, 0, 255))
            picture.putpixel( (x-1, y+1), (0, 0, 255))
            picture.putpixel( (x+1, y+1), (0, 0, 255))
            picture.putpixel( (x+1, y-1), (0, 0, 255))

            print("{}, {}: {}".format(i, j, maze[j][i]))
            # North Wall
            check = maze[j][i] & N
            if check != 0 and check & (check - 1) == 0:
                picture.putpixel( (x, y-1), (255, 255, 255))
                picture.putpixel( (x, y-2), (255, 255, 255))
                picture.putpixel( (x-1, y-2), (0, 0, 255))
                picture.putpixel( (x+1, y-2), (0, 0, 255))
            else:
                picture.putpixel( (x, y-1), (0, 0, 255))

            # East Wall
            check = maze[j][i] & E
            if check != 0 and check & (check - 1) == 0:
                picture.putpixel( (x+1, y), (255, 255, 255))
                picture.putpixel( (x+2, y), (255, 255, 255))
                picture.putpixel( (x+2, y-1), (0, 0, 255))
                picture.putpixel( (x+2, y+1), (0, 0, 255))
            else:
                picture.putpixel( (x+1, y), (0, 0, 255))
            # South Wall
            check = maze[j][i] & S
            if check != 0 and check & (check - 1) == 0:
                picture.putpixel( (x, y+1), (255, 255, 255))
                picture.putpixel( (x, y+2), (255, 255, 255))
                picture.putpixel( (x-1, y+2), (0, 0, 255))
                picture.putpixel( (x+1, y+2), (0, 0, 255))
            else:
                picture.putpixel( (x, y+1), (0, 0, 255))

            # West Wall
            check = maze[j][i] & W
            if check != 0 and check & (check - 1) == 0:
                picture.putpixel( (x-1, y), (255, 255, 255))
                picture.putpixel( (x-2, y), (255, 255, 255))
                picture.putpixel( (x-2, y-1), (0, 0, 255))
                picture.putpixel( (x-2, y+1), (0, 0, 255))
            else:
                picture.putpixel( (x-1, y), (0, 0, 255))
    # mazestuff here

    if start_and_end:
        start = (4 * randrange(0, w//2) + 2, 4 * randrange(0, h) + 2)
        end = (4 * randrange(w//2, w) + 2, 4 * randrange(0, h) + 2)
        picture.putpixel( start, (255, 0, 0) )
        picture.putpixel( end, (255, 0, 0) )

    if len(cell_list) > 0:
        for cell in cell_list:
            picture.putpixel( cell, (255, 100, 200))
    return picture.save("./maze.png")

def draw_maze_dense(maze, w, h, cell_list = []):
    picture = Image.new("RGB", (2*w + 1, 2*h + 1), "#000")
    for j in range(h):
        for i in range(w):
            x = 2 * i + 1
            y = 2 * j + 1
            picture.putpixel( (x, y), (255,255,255))

            # North Wall
            check = maze[j][i] & N
            if check != 0 and check & (check - 1) == 0:
                picture.putpixel( (x, y-1), (200,200,200))

            # East Wall
            check = maze[j][i] & E
            if check != 0 and check & (check - 1) == 0:
                picture.putpixel( (x+1, y), (200,200,200))
            # South Wall
            check = maze[j][i] & S
            if check != 0 and check & (check - 1) == 0:
                picture.putpixel( (x, y+1), (200,200,200))

            # West Wall
            check = maze[j][i] & W
            if check != 0 and check & (check - 1) == 0:
                picture.putpixel( (x-1, y), (200,200,200))

    if len(cell_list) > 0:
        for cell in cell_list:
            picture.putpixel( (2*cell[0] + 1, 2*cell[1] + 1), (255, 100, 200))
    return picture.save("./maze.png")

def make_maze(w, h):
    return [[0 for j in range(w)] for i in range(h)]

    # Generate the maze

def carve_maze(cx, cy, maze):
    directions = [N, E, S, W]
    shuffle(directions)
    for d in directions:
        nx = cx + DIRECTIONS[d][0]
        ny = cy + DIRECTIONS[d][1]
        if nx >= 0 and nx < len(maze[0]) and ny >= 0 and ny < len(maze) and maze[ny][nx] == 0:
            # print("{}, {}: {}".format(cx, cy , d))
            maze[ny][nx] |= 8//d
            maze[cy][cx] |= d
            carve_maze(nx, ny, maze)

def carve_maze_iterative(start_x, start_y, maze):
    directions = [N, E, S, W]
    # shuffle(directions)
    c = (start_x, start_y)
    stack = []
    cells_visited = 1
    w = len(maze[0])
    h = len(maze)
    number_of_cells = w * h
    number_of_iterations = 0
    last_direction = 0
    while cells_visited < number_of_cells:
        directions_left = []
        cx = c[0]
        cy = c[1]
        for d in directions:
            # check if north or south
            lx = cx + DIRECTIONS[d][0]
            ly = cy + DIRECTIONS[d][1]
            if clamp(0, w, lx) and clamp(0, h, ly) and maze[ly][lx] == 0:
                directions_left.append(d)
        print("Directions left for {}, {}: {}".format(cx, cy, directions_left))
        len_left = len(directions_left)
        if len_left != 0:
            shuffle(directions_left)
            chosen_dir = directions_left[0]
            # if chosen_dir == last_direction and len_left > 1:
            #     directions_left.append(directions_left[-1])
            #     shuffle(directions_left)
            #     chosen_dir = directions_left[0]
            print("Chosen dir: {}".format(chosen_dir))
            nx = cx + DIRECTIONS[chosen_dir][0]
            ny = cy + DIRECTIONS[chosen_dir][1]
            print("Going to {}, {}".format(nx, ny))
            chosen = (nx, ny)
            maze[cy][cx] |= chosen_dir
            maze[ny][nx] |= 8//chosen_dir
            stack.append(c)
            c = chosen
            cells_visited += 1
            number_of_iterations += 1
            last_direction = chosen_dir
        elif len(stack) != 0:
            c = stack.pop()
            number_of_iterations += 1
            last_direction = 0
        else:
            print("{} visited, {} iterations".format(cells_visited, number_of_iterations))
            number_of_iterations += 1
            break

def loop_deadends(maze, w, h, number_of_points = -1):
    # Get all deadends
    ends = []
    outside_ends = []
    for j in range(h):
        for i in range(w):
            check = maze[j][i]
            if check & (check - 1) == 0:
                print("deadend at {}, {}: {}".format(i, j, check))
                if not (clamp(0, w, i + DIRECTIONS[check][0]) and clamp(0, h, j + DIRECTIONS[check][1]) ):
                    outside_ends.append( (i, j) )
                else:
                    ends.append( (i, j) )

    e = len(ends)
    if number_of_points == -1 or e <= number_of_points:
        parts = ends
    else:
        shuffle(ends)
        parts = ends[:number_of_points]

    print("List of parts: {}".format(parts))
    cell_list = []
    shuffle(parts)
    while len(parts) > 0:
        part = parts.pop(0)
        end = maze[part[1]][part[0]]
        # print("end: {} at {}, {}".format(end, part[0], part[1]))
        # nx = part[0] + DIRECTIONS[8//end][0]
        # ny = part[1] + DIRECTIONS[8//end][1]
        # print("{}, {}".format(nx, ny))
        # if clamp(0, w, nx) and clamp(0, h, ny):
        #     __n = maze[ny][nx]
        #     maze[ny][nx] |= end
        #     print( "{}, {}: {} -> {}, {}: {} | {} -> {}".format( part[0], part[1], end, nx, ny, 8//end, __n, maze[ny][nx]))
        # if (nx, ny) in parts:
        #     parts.remove( (nx, ny) )
        # cell_list.append( part )

        '''
            A dead end is a cell that only has one direction (points to the cell that leads to it)

            To determine which walls to break down, we must first see if there is a path to the cell behind the wall
        from the center. The cell is surrounded by four walls, and each wall is surrounded by two corners. We can draw it as:

            C 1 C
            4 X 2
            C 8 C

            We can abstract the numbered and corner cell's other connections as they are currently irrelevant.
        From X to any numbered cell N, we can form two 'squares'. Both 'squares' have two of their corners as X and N,
        and one other numbered cell and a corner. If either of these 'squares' contains a path from X to N,
        then we cannot break the wall down between X and N, as the whole square will be connected.
        Technically, this is just a design choice. Is this a lot of work for no reason? Probably!

        '''
    return cell_list

def clamp(a, b, c):
    return a <= c and c < b


# sys.setrecursionlimit(10000) # would love to optimize


w = 15
h = 15
maze = make_maze(w, h)
carve_maze_iterative(0, 0, maze)
# carve_maze(0, 0, maze)
cl = []
# cl = loop_deadends(maze, w, h)
draw_maze_dense(maze, w, h, cl)

