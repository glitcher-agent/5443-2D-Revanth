import pygame
import random
# Define colors
colors = [(255,211,155), (127,255,212), (155,205,155), (238,106,167), (255,106,106), (180, 34, 22), (100,149,237),]

class Block:
    x = 0
    y = 0
   
    # Define Tetrominos
    tetrimonis = [
         [[1, 2, 5, 9], [0, 4, 5, 6], [1, 5, 9, 8], [4, 5, 6, 10]],
         [[1, 2, 6, 10], [5, 6, 7, 9], [2, 6, 10, 11], [3, 5, 6, 7]],
         [[1, 2, 5, 6]],
         [[4, 5, 9, 10], [2, 6, 5, 9]],
         [[1, 5, 9, 13], [4, 5, 6, 7]],
         [[6, 7, 9, 10], [1, 5, 6, 10]],
         [[1, 4, 5, 6], [1, 4, 5, 9], [4, 5, 6, 9], [1, 5, 6, 9]],
    ]
# Initialize grid
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.type = random.randint(0, len(self.tetrimonis) - 1)
        self.color = random.randint(1, len(colors) - 1)
        self.rotation = 0

    def tetrisblock(self):
        return self.tetrimonis[self.type][self.rotation]
#Defining the rotation of the block
    def rotate(self):
        self.rotation = (self.rotation + 1) % len(self.tetrimonis[self.type])


class Tetris:
    # Initialize score,height,width,height
    def __init__(self, height, width):
        self.level = 1
        self.score = 0
        self.state = "start"
        self.field = []
        self.height = 0
        self.width = 0
        self.x = 100
        self.y = 60
        self.zoom = 20
        self.block = None
    
        self.height = height
        self.width = width
        self.field = []
        self.score = 0
        self.state = "start"
        for i in range(height):
            new_line = []
            for j in range(width):
                new_line.append(0)
            self.field.append(new_line)
    #define for the new tetris block
    def new_block(self):
        self.block = Block(3, 0)
    # define to determine whether two block collision
    def collision(self):
        collision = False
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.block.tetrisblock():
                    if i + self.block.y > self.height - 1 or \
                            j + self.block.x > self.width - 1 or \
                            j + self.block.x < 0 or \
                            self.field[i + self.block.y][j + self.block.x] > 0:
                        collision = True
        return collision
    #define to remove the whole line
    def remove_lines(self):
        lines = 0
        for i in range(1, self.height):
            zeros = 0
            for j in range(self.width):
                if self.field[i][j] == 0:
                    zeros += 1
            if zeros == 0:
                lines += 1
                for i1 in range(i, 1, -1):
                    for j in range(self.width):
                        self.field[i1][j] = self.field[i1 - 1][j]
                        screen.blit(text_game_over, [40, 200])
                        
        self.score += lines ** 2
    def freeze(self):
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.block.tetrisblock():
                    self.field[i + self.block.y][j + self.block.x] = self.block.color
        self.remove_lines()
        self.new_block()
        if self.collision():
            self.state = "gameover"
#key actions

    def go_down(self):
        self.block.y += 1
        if self.collision():
            self.block.y -= 1
            self.freeze()

    def go_side(self, dx):
        old_x = self.block.x
        self.block.x += dx
        if self.collision():
            self.block.x = old_x

    def rotate(self):
        old_rotation = self.block.rotation
        self.block.rotate()
        if self.collision():
            self.block.rotation = old_rotation


# Initialize the gameGrid engine
pygame.init()

# Define some colors
black = (0, 0, 0)
white = (255, 255, 255)
gray = (128, 128, 128)

size = (400, 500)
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Tetris gameGrid")

done = False
clock = pygame.time.Clock()
speed = 20
gameGrid = Tetris(20, 10)
counter = 0

pressing_down = False

# Start gameGrid loop
while not done:
    if gameGrid.block is None:
        gameGrid.new_block()
    counter += 1
    if counter > 100000:
        counter = 0

    if counter % (speed // gameGrid.level // 1) == 0 or pressing_down:
        if gameGrid.state == "start":
            gameGrid.go_down()
     # Check for key press events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                gameGrid.rotate()
            if event.key == pygame.K_DOWN:
                pressing_down = True
            if event.key == pygame.K_LEFT:
                gameGrid.go_side(-1)
            if event.key == pygame.K_RIGHT:
                gameGrid.go_side(1)
            if event.key == pygame.K_ESCAPE:
                gameGrid.__init__(20, 10)

    if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                pressing_down = False
    # Clear the screen
    screen.fill(black)

    for i in range(gameGrid.height):
        for j in range(gameGrid.width):
            pygame.draw.rect(screen, white, [gameGrid.x + gameGrid.zoom * j, gameGrid.y + gameGrid.zoom * i, gameGrid.zoom, gameGrid.zoom], 1)
            if gameGrid.field[i][j] > 0:
                pygame.draw.rect(screen, colors[gameGrid.field[i][j]],
                                 [gameGrid.x + gameGrid.zoom * j + 1, gameGrid.y + gameGrid.zoom * i + 1, gameGrid.zoom - 2, gameGrid.zoom - 1])
     # Draw the current Tetromino
    if gameGrid.block is not None:
        for i in range(4):
            for j in range(4):
                p = i * 4 + j
                if p in gameGrid.block.tetrisblock():
                    pygame.draw.rect(screen, colors[gameGrid.block.color],
                                     [gameGrid.x + gameGrid.zoom * (j + gameGrid.block.x) + 1,
                                      gameGrid.y + gameGrid.zoom * (i + gameGrid.block.y) + 1,
                                      gameGrid.zoom - 2, gameGrid.zoom - 2])

    font = pygame.font.SysFont('Calibri', 25, True, False)
    font1 = pygame.font.SysFont('Calibri', 65, True, False)
    text = font.render("Score: " + str(gameGrid.score), True, white)
    text_game_over = font1.render("gameGrid Over", True, (255, 125, 0))
    text_game_over1 = font1.render("Press ESC", True, (255, 215, 0))

    screen.blit(text, [0, 0])
    if gameGrid.state == "gameover":
        screen.blit(text_game_over, [40, 200])
        screen.blit(text_game_over1, [40, 275])

    pygame.display.flip()
    clock.tick(speed)

pygame.quit()