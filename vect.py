'''
vect.py

Vector Space:
A Vectrex influenced, score attack shooter

By Nicholas Ruggles
'''

from __future__ import division
import pygame, sys
from pygame.locals import *

FPS = 60
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 480

RED =   (255, 0, 0)
BLACK = (0  , 0, 0)

# Linelists are a list of tuples, where each tuple is composed of 4 integers
# formatted thus (x1, y1, x2, y2), creating a line from (x1,y1) to (x2,y2)

BOX_LINELIST = [(-8, -8, 8, -8),
                ( 8, -8, 8,  8),
                ( 8,  8,-8,  8),
                (-8,  8,-8, -8)]

VERT_LINELIST = [(0, 8, 0, -8)]

HORIZ_LINELIST = [(8, 0, -8, 0)]

DIAG_LINELIST = [(2, 2, -2, -2)]

PLAYER_POS = (WINDOW_WIDTH/2, WINDOW_HEIGHT/2)
PLAYER_SPEED = 2
ENEMY_SPEED = 2

def main():

    global DISPLAYSURF, FPSCLOCK    
    
    # Initialize shit    
    pygame.init()
    DISPLAYSURF = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_caption("Vector Space")
    playerOne = player(PLAYER_POS, BOX_LINELIST)
    testEnemy = vertEnemy((WINDOW_WIDTH/2, 0), VERT_LINELIST)

    # Game Loop
    while True:

        # Event handling code

        for event in pygame.event.get():

            # Check for quit event
            if event.type == QUIT:
                terminate()

        pygame.event.get() # Clear event queue

        # Collision code
        if doesCollide(playerOne, testEnemy):
            terminate()

        # Player movement code
        pressedKeys = pygame.key.get_pressed()
        if pressedKeys[K_UP] and pressedKeys[K_RIGHT]:
            playerOne.move((PLAYER_SPEED**0.5, -PLAYER_SPEED**0.5))
        elif pressedKeys[K_UP] and pressedKeys[K_LEFT]:
            playerOne.move((-PLAYER_SPEED**0.5, -PLAYER_SPEED**0.5))
        elif pressedKeys[K_DOWN] and pressedKeys[K_RIGHT]:
            playerOne.move((PLAYER_SPEED**0.5, PLAYER_SPEED**0.5))
        elif pressedKeys[K_DOWN] and pressedKeys[K_LEFT]:
            playerOne.move((-PLAYER_SPEED**0.5, PLAYER_SPEED**0.5))
        elif pressedKeys[K_UP]:
            playerOne.move((0, -PLAYER_SPEED))
        elif pressedKeys[K_DOWN]:
            playerOne.move((0, PLAYER_SPEED))
        elif pressedKeys[K_RIGHT]:
            playerOne.move((PLAYER_SPEED, 0))
        elif pressedKeys[K_LEFT]:
            playerOne.move((-PLAYER_SPEED, 0))

        # Enemy movement code
        testEnemy.move(ENEMY_SPEED)

        # Draw code
        DISPLAYSURF.fill(BLACK)
        playerOne.draw()
        testEnemy.draw()

        # Frame & display update code
        pygame.display.update()
        FPSCLOCK.tick(FPS)

# Superclass for bullet, enemy, player
class entity(object):
    
    def __init__(self, pos, lineList):

        self.pos = pos
        self.lineList = lineList

    # Calls drawing function with the list of lines as argument
    def draw(self):
        drawLines(self.pos, self.lineList)
    
    def getPos(self):
        return self.pos

    def getLineList(self):
        return self.lineList

    # Move function is individually defined in each subclass
    def move(self):
        pass

class player(entity):

    def move(self, (deltaX, deltaY)):
        x, y = self.pos
        self.pos = (x + deltaX, y + deltaY)

class vertEnemy(entity):
    
    def move(self, deltaY):
        x, y = self.pos
        self.pos = (x, y + deltaY)

class bullet(entity):
    pass

# Takes a list of lines, draws them to DISPLAYSURF object
def drawLines(pos, lineList):
    for line in lineList:
        # Draw line!
        x1 = pos[0] + line[0]
        y1 = pos[1] + line[1]
        x2 = pos[0] + line[2]
        y2 = pos[1] + line[3]
        pygame.draw.line(DISPLAYSURF, RED, (x1, y1), (x2, y2))

def doesCollide(entity1, entity2):
    pos1 = entity1.getPos()
    lineList1 = entity1.getLineList()
    pos2 = entity2.getPos()
    lineList2 = entity2.getLineList()
    
    return collideLines(pos1, lineList1, pos2, lineList2)

# Returns true if any line in List1 crosses List2
def collideLines(pos1, lineList1, pos2, lineList2):

    for line1 in lineList1:

        # Convert line1 into board coords
        x1i = line1[0] + pos1[0]
        x1f = line1[2] + pos1[0]
        y1i = line1[1] + pos1[1]
        y1f = line1[3] + pos1[1]

        newLine1 = (x1i, y1i, x1f, y1f)

        for line2 in lineList2:

            # Convert line2 into board coords
            x2i = line2[0] + pos2[0]
            x2f = line2[2] + pos2[0]
            y2i = line2[1] + pos2[1]
            y2f = line2[3] + pos2[1]

            newLine2 = (x2i, y2i, x2f, y2f)

            if checkCross(newLine1, newLine2):
                return True

    return False

# Return true if line1 crosses line2
def checkCross(line1, line2):

    m1, b1 = slopeIntersect(line1)
    m2, b2 = slopeIntersect(line2)

    if m1 == m2:
        return False

    x, y = findIntersect(m1, b1, m2, b2)

    # if initial x is greater than final x
    if line1[0] > line1[2]:
        xmax1 = line1[0]
        xmin1 = line1[2]
    else:
        xmax1 = line1[2]
        xmin1 = line1[0]

    # if initial y is greater than final y
    if line1[1] > line1[3]:
        ymax1 = line1[1]
        ymin1 = line1[3]
    else:
        ymax1 = line1[3]
        ymin1 = line1[1]

    # if initial x is greater than final x
    if line2[0] > line2[2]:
        xmax2 = line2[0]
        xmin2 = line2[2]
    else:
        xmax2 = line2[2]
        xmin2 = line2[0]

    # if initial y is greater than final y
    if line2[1] > line2[3]:
        ymax2 = line2[1]
        ymin2 = line2[3]
    else:
        ymax2 = line2[3]
        ymin2 = line2[1]

    if ((xmin1 <= x <= xmax1) and (ymin1 <= y <= ymax1) and
       (xmin2 <= x <= xmax2) and (ymin2 <= y <= ymax2)):
        return True

    return False

# Convert line from 2 points into slope intercept form
def slopeIntersect(line):
    xi, yi, xf, yf = line
    
    # If line is vertical
    if xi == xf:
        # No slope or y-intersect exists
        m = None
        b = xi
        # Return None for slope, and x intercept instead of y
        return (m, b)

    m = (yf - yi)/(xf -xi)
    b = yi - m*xi

    return (m, b)

# Find intersect of two lines in slope intercept form
def findIntersect(m1, b1, m2, b2):
    
    # If line1 is vertical
    if m1 == None:
        x = b1
        y = m2*x + b2

    # If line2 is vertical
    elif m2 == None:
        x = b2
        y = m1*x + b1
    
    # If neither lines are vertical
    else:
        x = (b2 - b1)/(m1 - m2)
        y = m1*x + b1

    #print x, y
    return (x, y)

def terminate():
    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
