import pygame, sys
from board import Board
import colour
pygame.init()

screen = pygame.display.set_mode((620,680))
pygame.display.set_caption('2048') 
game = Board()

FONT = pygame.font.Font('freesansbold.ttf', 28) 
SMALLFONT = pygame.font.Font('freesansbold.ttf', 17) 
IMAGESIZE = 130
IMAGES = []
NAMES = ["oliver", "owen", "cass", "alastair",
        "clare", "cath", "ben", "alexp", "alexs", "louise", "melissa", 
        "henry", "david",  "nic", "harry"]
for name in NAMES:
    im = pygame.image.load("images/" + name + ".jpeg").convert()
    im = pygame.transform.scale(im, (IMAGESIZE,IMAGESIZE))
    IMAGES.append(im)

TILECOORDS = [[(20+150*i, 80+150*j) for i in range(4)] for j in range(4)]

def draw_empty_tiles():
    screen.fill(colour.LIGHTGREY)
    for row in TILECOORDS:
        for coord in row:
            blank_tile = pygame.Rect(coord[0], coord[1], 130, 130)
            pygame.draw.rect(screen, colour.MEDIUMGREY, blank_tile)

def draw_tiles():
    for i in range(4):
        for j in range(4):
            tile = game.grid[i][j]
            if not tile.isEmpty():
                image = IMAGES[tile.image_index]
                if tile.scale < 1:
                    size = round(tile.scale * IMAGESIZE)
                    image = pygame.transform.scale(image, (size, size))
                    tile.scale += 0.1
                centre = (TILECOORDS[i][j][0] + 65, TILECOORDS[i][j][1] + 65)
                imRc = image.get_rect(center=centre)
                screen.blit(image, imRc)

def write_score():
    text = FONT.render('Score: ' + str(game.score), True, colour.WHITE)
    textRc = text.get_rect()
    textRc.left = 450
    textRc.top = 20

    goal = SMALLFONT.render('Combine tiles to reach the coveted Harry tile',
                        True, colour.BLACK)
    goalRc = goal.get_rect()
    goalRc.left = 20
    goalRc.bottom = textRc.bottom
    
    screen.blit(text, textRc)
    screen.blit(goal, goalRc)

def gameDialog(message):
    endTxt = FONT.render(message, True, colour.WHITE)
    endTxtRc = endTxt.get_rect(center = (310, 200))
    scoreTxt = FONT.render('Final Score: ' + str(game.score), True, colour.WHITE)
    scoreTxtRc = scoreTxt.get_rect(center = (310, 250))
    restartTxt = FONT.render('Restart', True, colour.WHITE, colour.DARKGREY)
    restartTxtRc = restartTxt.get_rect(center = (210,330))
    quitTxt = FONT.render('Quit', True, colour.WHITE, colour.DARKGREY)
    quitTxtRc = quitTxt.get_rect(center = (410,330))

    writing = [(endTxt, endTxtRc), (scoreTxt, scoreTxtRc), (restartTxt, restartTxtRc),
                (quitTxt, quitTxtRc)]
    mainBox = pygame.Rect(110, 170, 400, 200)
    pygame.draw.rect(screen, colour.TURQOUISE, mainBox)
    for txt in writing:
        screen.blit(txt[0], txt[1])
    return restartTxtRc,quitTxtRc

playMode = True
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN and playMode:
            direction = 'none'
            if event.key == pygame.K_UP:
                direction = 'u'
            elif event.key == pygame.K_DOWN:
                direction = 'd'
            elif event.key == pygame.K_LEFT:
                direction = 'l'
            elif event.key == pygame.K_RIGHT:
                direction = 'r'
            game.move(direction)
        if event.type == pygame.MOUSEBUTTONDOWN and not playMode:
            pos = event.pos
            if reRc.collidepoint(pos):
                game = Board()
                playMode = True
            elif quitRc.collidepoint(pos):
                sys.exit()
              
    draw_empty_tiles()
    draw_tiles()
    write_score()
    if game.checkWin():
        reRc, quitRc = gameDialog("You Win!")
        playMode = False
    if not game.stillAlive():
        playMode = False
        reRc, quitRc = gameDialog("Game Over")

    pygame.display.update()
    pygame.time.delay(30)