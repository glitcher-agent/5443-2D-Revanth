################
#TETRIS
#Course: CMPS 5443
################
import pygame
import random

# Define colors
colors = [
    (255,211,155),
    (127,255,212),
    (155,205,155),
    (238,106,167),
    (255,106,106),
    (180, 34, 22),
    (100,149,237),
]

class MySprite(pygame.sprite.Sprite):
    def __init__(self):
        super(MySprite, self).__init__()
 
        self.images = []
        self.images.append(pygame.image.load('D:/Users/revan/Downloads/Sprites/images/walk1.png'))
        self.images.append(pygame.image.load('D:/Users/revan/Downloads/Sprites/images/walk2.png'))
        self.images.append(pygame.image.load('D:/Users/revan/Downloads/Sprites/images/walk3.png'))
        self.images.append(pygame.image.load('D:/Users/revan/Downloads/Sprites/images/walk4.png'))
        self.images.append(pygame.image.load('D:/Users/revan/Downloads/Sprites/images/walk5.png'))
        self.images.append(pygame.image.load('D:/Users/revan/Downloads/Sprites/images/walk6.png'))
        self.images.append(pygame.image.load('D:/Users/revan/Downloads/Sprites/images/walk7.png'))
        self.images.append(pygame.image.load('D:/Users/revan/Downloads/Sprites/images/walk8.png'))
        self.images.append(pygame.image.load('D:/Users/revan/Downloads/Sprites/images/walk9.png'))
        self.images.append(pygame.image.load('D:/Users/revan/Downloads/Sprites/images/walk10.png'))
 
        self.index = 0
 
        self.image = self.images[self.index]
        self.rect = pygame.Rect(1, 1, 1, 1)
 
    def update(self):
        self.index += 1
 
        if self.index >= len(self.images):
            self.index = 0
        
        self.image = self.images[self.index]
class Block:
    x = 0
    y = 0
   
    # Define Tetrominos that have list of lists of blocks 
    # the main list contains block types, and the inner lists contain their rotations. 
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
#randomly pick a type and a color
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
        self.x = 200
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
#check if the currently flying figure intersecting with something fixed on the field
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
                        linesound.play ()
                        
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


# Initialize the game engine
pygame.init()
#sound
linesound = pygame.mixer.Sound("D:/Users/revan/Desktop/5443-2D-Revanth/Assignments/02-P01/beep.wav")
#sound
gameover = pygame.mixer.Sound("D:/Users/revan/Desktop/5443-2D-Revanth/Assignments/02-P01/gameover.wav")

# Define some colors
black = (0, 0, 0)
white = (255, 255, 255)
gray = (128, 128, 128)
#teris grid size
size = (600, 500)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Tetris Game by Revanth and Nageswar")
my_sprite = MySprite()
my_group = pygame.sprite.Group(my_sprite)
done = False
clock = pygame.time.Clock()
fps = 25
game = Tetris(20, 10)
counter = 0
pressing_down = False

# Start game loop
while not done:
    if game.block is None:
        game.new_block()
    counter += 1
    if counter > 100000:
        counter = 0

    if counter % (fps // game.level // 2) == 0 or pressing_down:
        if game.state == "start":
            game.go_down()
     # Check for key press events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                game.rotate()
            if event.key == pygame.K_DOWN:
                pressing_down = True
            if event.key == pygame.K_LEFT:
                game.go_side(-1)
            if event.key == pygame.K_RIGHT:
                game.go_side(1)
            if event.key == pygame.K_ESCAPE:
                game.__init__(20, 10)

    if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                pressing_down = False
    # Clear the screen
    screen.fill(black)
   
    for i in range(game.height):
        for j in range(game.width):
            pygame.draw.rect(screen, white, [game.x + game.zoom * j, game.y + game.zoom * i, game.zoom, game.zoom], 1)
            if game.field[i][j] > 0:
                pygame.draw.rect(screen, colors[game.field[i][j]],
                                 [game.x + game.zoom * j + 1, game.y + game.zoom * i + 1, game.zoom - 2, game.zoom - 1])
     # Draw the current Tetromino
    if game.block is not None:
        for i in range(4):
            for j in range(4):
                p = i * 4 + j
                if p in game.block.tetrisblock():
                    pygame.draw.rect(screen, colors[game.block.color],
                                     [game.x + game.zoom * (j + game.block.x) + 1,
                                      game.y + game.zoom * (i + game.block.y) + 1,
                                      game.zoom - 2, game.zoom - 2])

    fonttetris=pygame.font.SysFont('Calibri', 30, True, False)
    font = pygame.font.SysFont('Calibri', 30, True, False)
    font1 = pygame.font.SysFont('Calibri', 55, True, False)
    namegame = font.render("Tetris ", True, white)
    score = font.render("Score: " + str(game.score), True, white)
    text_game_over = font1.render("Game Over", True, (255, 125, 0))
    text_game_over1 = font.render("Press ESC to Start Again", True, (255, 215, 0))
    screen.blit(namegame, [250, 0])
    screen.blit(score, [480, 0])
    if game.state == "gameover":
        screen.fill(black)
        screen.blit(text_game_over, [40, 200])
        screen.blit(text_game_over1, [40, 275])
        score=font1.render("Your Score: " + str(game.score), True, white)
        screen.blit(score, [40, 350])
        gameover.play()
        my_group.update()
        my_group.draw(screen)
        pygame.display.update()
        
    clock.tick(20)
    pygame.display.flip()

pygame.quit()