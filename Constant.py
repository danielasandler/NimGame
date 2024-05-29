ROWS, COLS = 5, 7
WIDTH =  700
SQUARE_SIZE = WIDTH//COLS
HEIGHT = SQUARE_SIZE * ROWS
LINE_WIDTH = 2
PADDING = SQUARE_SIZE //5


#RGB
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
LIGHTGRAY = (211,211,211)
GREEN = (0, 128, 0)

# epsilon Greedy
epsilon_start = 1
epsilon_final = 0.01
epsiln_decay = 1000