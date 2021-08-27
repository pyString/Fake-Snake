import random, pygame, sys
from pygame.locals import *

FPS = 15
WINDOWIDTH = 640
WINDOWHEIGHT = 480
CELLSIZE = 20
assert WINDOWIDTH % CELLSIZE == 0, "Window must be a multiple cell size"
assert WINDOWHEIGHT % CELLSIZE == 0, "Window must be a multiple cell size"
CELLWIDTH = int(WINDOWIDTH / CELLSIZE)
CELLHEIGHT = int(WINDOWHEIGHT / CELLSIZE)

#RGB

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
DARKG = (0, 155, 0)
DARKGRAY = (40, 40, 40)
BGCOLOR = BLACK

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

HEAD = 0 #head of the snake

def rtrn_func():
   return

def main():

    global FPSCLOCK, DISPLAYSURF, BASICFONT

    pygame.init()
    
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWIDTH, WINDOWHEIGHT))
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
    pygame.display.set_caption('Snake do Paraguai')

    showStartScreen()

    
    #while True:

    runGame()
    showGameOverScreen()

def runGame():

    #set random start point
    startx = random.randint(5, CELLWIDTH - 6)
    starty = random.randint(5, CELLHEIGHT - 6)
    snakeCoords = [{'x': startx, 'y': starty},
                   {'x': startx -1, 'y': starty},
                   {'x': startx -2, 'y': starty}]
    direction = RIGHT

    #Start apple in random loation
    apple = getRandomLocation()

    while True: #main game Loop
        for event in pygame.event.get():
            print(event)
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                if(event.key == K_LEFT or event.key == K_a) and direction != RIGHT:
                    direction = LEFT
                elif(event.key == K_RIGHT or event.key == K_d) and direction != LEFT:
                    direction = RIGHT
                elif(event.key == K_UP or event.key == K_w) and direction != DOWN:
                    direction = UP
                elif(event.key == K_DOWN or event.key == K_s) and direction != UP:
                    direction = DOWN
                elif event.key == K_ESCAPE:
                    terminate()
                print("Cabeça: ", snakeCoords[HEAD]['x'], snakeCoords[HEAD]['y'])


                #check if the snake has hit itself or the edge
                if snakeCoords[HEAD]['x'] == 0 or snakeCoords[HEAD]['x'] == CELLWIDTH or snakeCoords[HEAD]['y'] == 0 or snakeCoords[HEAD]['y'] == CELLHEIGHT:
                    print("GAME-OVER BATEU NA BORDA")
                    return

                    #rtrn_func() #game over
                for snakeBody in snakeCoords[1:]:
                    if snakeBody['x'] == snakeCoords[HEAD]['x'] and snakeBody == snakeCoords[HEAD]['y']:
                        print("GAME-OVER SE COMEU")
                        return
                        #rtrn_func() #game over

                # check if snake has eaten an apple
                if snakeCoords[HEAD]['x'] == apple['x'] and snakeCoords[HEAD]['y'] == apple['y']:
                    apple = getRandomLocation()
                else:
                    del snakeCoords[-1]

                #Move the fucking snake
                if direction == UP:
                    newhead = {'x': snakeCoords[HEAD]['x'], 'y': snakeCoords[HEAD]['y'] -1}
                elif direction == DOWN:
                    newhead = {'x': snakeCoords[HEAD]['x'], 'y': snakeCoords[HEAD]['y'] +1}
                elif direction == LEFT:
                    newhead = {'x': snakeCoords[HEAD]['x'] -1, 'y': snakeCoords[HEAD]['y']}
                elif direction == RIGHT:
                    newhead = {'x': snakeCoords[HEAD]['x'] +1, 'y': snakeCoords[HEAD]['y']}
                snakeCoords.insert(0, newhead)

                DISPLAYSURF.fill(BGCOLOR)
                drawGrid()
                drawSnake(snakeCoords)
                drawApple(apple)
                drawScore(len(snakeCoords)-3)
                pygame.display.update()
                FPSCLOCK.tick(FPS)



def drawPressKeyMsg():
    pressKeySurf = BASICFONT.render('Press a key to play.', True, DARKGRAY)
    pressKeyRect = pressKeySurf.get_rect()
    pressKeyRect.topleft = (WINDOWIDTH - 200, WINDOWHEIGHT - 30)
    DISPLAYSURF.blit(pressKeySurf, pressKeyRect)
    
def checkForKeyPress():
    if len(pygame.event.get(QUIT)) > 0:
        terminate()

    KeyUpEvents = pygame.event.get(KEYUP)

    if len(KeyUpEvents) == 0:
        return None

    if KeyUpEvents[0].key == K_ESCAPE:
        terminate()
    return KeyUpEvents[0].key

def showStartScreen():
    titleFont = pygame.font.Font('freesansbold.ttf', 50)
    titleSurf1 = titleFont.render('Snake do Paraguai', True, WHITE, DARKG)
    titleSurf2 = titleFont.render('Snake do Paraguai', True, GREEN)

    degrees1 = 0
    degrees2 = 0
    while True:
        DISPLAYSURF.fill(BGCOLOR)

        rotatedSurf1 = pygame.transform.rotate(titleSurf1, degrees1)
        rotatedRect1 = rotatedSurf1.get_rect()
        rotatedRect1.center = (WINDOWIDTH / 2, WINDOWHEIGHT / 2)
        DISPLAYSURF.blit(rotatedSurf1, rotatedRect1)

        rotatedSurf2 = pygame.transform.rotate(titleSurf2, degrees2)
        rotatedRect2 = rotatedSurf2.get_rect()
        rotatedRect2.center = (WINDOWIDTH / 2, WINDOWHEIGHT / 2)
        DISPLAYSURF.blit(rotatedSurf2, rotatedRect2)

        drawPressKeyMsg()

        if checkForKeyPress():
            pygame.event.get()
            return
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def terminate():
    pygame.quit()
    sys.exit()

def getRandomLocation():
    return{'x': random.randint(0, CELLWIDTH - 1), 'y': random.randint(0, CELLHEIGHT -1)}

def showGameOverScreen():
    gameOverFont = pygame.font.Font('freesansbold.ttf', 150)
    gameSurf = gameOverFont.render('Game', True, WHITE)
    overSurf = gameOverFont.render('Over', True, WHITE)
    gameRect = gameSurf.get_rect()
    overRect = overSurf.get_rect()
    gameRect.midtop = (WINDOWIDTH /2, 10)
    overRect.midtop = (WINDOWIDTH / 2,gameRect.height + 10 + 25)

    DISPLAYSURF.blit(gameSurf, gameRect)
    DISPLAYSURF.blit(overSurf, overRect)
    drawPressKeyMsg()
    pygame.display.update()

    pygame.time.wait(500)
    checkForKeyPress()

    while True:
        if checkForKeyPress():
            pygame.event.get()
            return

def drawScore(score):
    scoreSurf = BASICFONT.render('Score: %s' % (score), True, WHITE)
    scoreRect = scoreSurf.get_rect()
    scoreRect.topleft = (WINDOWIDTH - 120, 10)
    DISPLAYSURF.blit(scoreSurf, scoreRect)

def drawSnake(snakeCoords):
    for coord in snakeCoords:
        x = coord['x'] * CELLSIZE
        y = coord['y'] * CELLSIZE
        snakeSegmentRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
        pygame.draw.rect(DISPLAYSURF, DARKG, snakeSegmentRect)
        wormInnerSegmentRect = pygame.Rect(x + 4, y + 4, CELLSIZE - 8, CELLSIZE - 8)
        pygame.draw.rect(DISPLAYSURF, GREEN, wormInnerSegmentRect)

def drawApple(coord):
    x = coord['x'] * CELLSIZE
    y = coord['y'] * CELLSIZE
    appleRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
    pygame.draw.rect(DISPLAYSURF, RED, appleRect)

def drawGrid():
    for x in range(0, WINDOWIDTH, CELLSIZE):
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (x, 0), (x, WINDOWHEIGHT))
    for y in range(0, WINDOWHEIGHT, CELLSIZE):
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (0, y), (WINDOWIDTH, y))
    
if __name__ == '__main__':
    main()