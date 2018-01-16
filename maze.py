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

sys.setrecursionlimit(10000) # would love to optimize
w = 127
h = 127
maze = make_maze(w, h)
carve_maze(0, 0, maze)
draw_maze(maze, w, h, True)
