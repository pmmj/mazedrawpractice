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

def draw_maze(maze, w, h, start_and_end = False):
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
        if len(directions_left) != 0:
            shuffle(directions_left)
            chosen_dir = directions_left[0]
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
        elif len(stack) != 0:
            c = stack.pop()
            number_of_iterations += 1
        else:
            print("{} visited, {} iterations".format(cells_visited, number_of_iterations))
            number_of_iterations += 1
            break

def clamp(a, b, c):
    return a <= c and c < b


# sys.setrecursionlimit(10000) # would love to optimize


w = 15
h = 15
maze = make_maze(w, h)
carve_maze_iterative(0, 0, maze)
# carve_maze(0, 0, maze)
draw_maze(maze, w, h, True)
