import random
import sys    #since we'll use sys.exit to exit the program
import pygame
from pygame.locals import *  #basic pygame imports

#Global variables for the game

FPS=32 #Frames per second
SCREENWIDTH = 289
SCREENHEIGHT = 511
SCREEN = pygame.display.set_mode((SCREENWIDTH,SCREENHEIGHT)) #initializing a screen for display
GROUNDY = SCREENHEIGHT * 0.8
GAME_SPRITES = {}
GAME_SOUNDS = {}
PLAYER = 'Gallery/Sprites/fish.png'
BACKGROUND = 'Gallery/Sprites/background.png'
PIPE = 'Gallery/Sprites/pipe.png'
GAMEOVER = 'Gallery/Sprites/gameover.png'

def welcomeScreen():
    fishx  = int(SCREENWIDTH/5)
    fishy = int((SCREENHEIGHT - GAME_SPRITES['fish'].get_height())/2)
    messagex = int((SCREENWIDTH - GAME_SPRITES['message'].get_width())/2)
    messagey = int(SCREENHEIGHT*0.13)
    basex = 0
    while True:
        for event in pygame.event.get():   #pygame.event.get() tells us about all the event occuring during the game like the keys pressed on keyboard or something clicked on by mouse
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE): #if user clicks on cross button or Esc key is pressed,quit the game
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                return
            else:
                SCREEN.blit(GAME_SPRITES['background'], (0, 0)) 
                SCREEN.blit(GAME_SPRITES['fish'], (int(SCREENWIDTH/2.5), fishy)) 
                SCREEN.blit(GAME_SPRITES['message'], (messagex,messagey)) 
                SCREEN.blit(GAME_SPRITES['base'],(basex,GROUNDY)) 
                pygame.display.update() #unless until display.update() doesn't run, our screen won't change
                FPSCLOCK.tick(FPS) #setting my FPS
def playGame():
    score = 0
    fishx = int(SCREENWIDTH/5)
    fishy = int(SCREENWIDTH/2)
    basex = 0

    # Create 2 pipes for blitting on the screen
    newPipe1 = getRandompipe()
    newPipe2 = getRandompipe()

    # creating list of upper pipes
    upperPipes = [
        {'x': SCREENWIDTH+200, 'y':newPipe1[0]['y']},
        {'x': SCREENWIDTH+200+(SCREENWIDTH/2), 'y':newPipe2[0]['y']},
    ]
    # creating list of lower pipes
    lowerPipes = [
        {'x': SCREENWIDTH+200, 'y':newPipe1[1]['y']},
        {'x': SCREENWIDTH+200+(SCREENWIDTH/2), 'y':newPipe2[1]['y']},
    ]

    pipeVelx = -4
    fishVely = -9
    fishMaxVely = 10
    fishMinVely = -8
    fishAccy = 1

    fishvelFlapping = -8 #fish's velocity while flapping
    fishFlapped = False #True when fish is swimming else false

    
   #our game loop
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
                #if space or up key is pressed, our bird will start flapping
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if fishy > 0: #if my player is in the screen
                    fishVely = fishvelFlapping
                    fishFlapped = True
                    GAME_SOUNDS['wing'].play()


        crashTest = isCollide(fishx, fishy, upperPipes, lowerPipes) # This function will return true if the player is crashed
        if crashTest:
            SCREEN.blit(GAME_SPRITES['gameover'], (SCREENWIDTH/9,(SCREENHEIGHT-GAME_SPRITES['gameover'].get_height())/2))
            pygame.display.update()
            GAME_SOUNDS['hit'].play()
            return     

        #check for score
        fishcentre = fishx + GAME_SPRITES['fish'].get_width()/2
        for pipe in upperPipes:
            pipeCentre = pipe['x'] + GAME_SPRITES['pipe'][0].get_width()/2
            if pipeCentre<= fishcentre < pipeCentre+4:
                score +=1
                print(f"Your score is {score}") 
                GAME_SOUNDS['point'].play()


        if fishVely <fishMaxVely and not fishFlapped:
            fishVely += fishAccy

        if fishFlapped:
            fishFlapped = False            
        fishHeight = GAME_SPRITES['fish'].get_height()
        fishy = fishy + min(fishVely, GROUNDY - fishy - fishHeight)

        # move pipes to the left
        for upperPipe , lowerPipe in zip(upperPipes, lowerPipes):
            upperPipe['x'] += pipeVelx
            lowerPipe['x'] += pipeVelx

        # Add a new pipe when the first is about to cross the leftmost part of the screen
        if 0<upperPipes[0]['x']<5:
            newpipe = getRandompipe()
            upperPipes.append(newpipe[0])
            lowerPipes.append(newpipe[1])

        # if the pipe is out of the screen, remove it
        if upperPipes[0]['x'] < -GAME_SPRITES['pipe'][0].get_width():
            upperPipes.pop(0)
            lowerPipes.pop(0)
        
        

        #blitting our sprites
        SCREEN.blit(GAME_SPRITES['background'], (0,0))
        SCREEN.blit(GAME_SPRITES['base'], (basex,GROUNDY))
        SCREEN.blit(GAME_SPRITES['fish'], (fishx,fishy))
        for upperPipe, lowerPipe in zip(upperPipes,lowerPipes):
            SCREEN.blit(GAME_SPRITES['pipe'][1], (lowerPipe['x'],lowerPipe['y']))
            SCREEN.blit(GAME_SPRITES['pipe'][0], (upperPipe['x'],upperPipe['y']))
        
        #for blitting our score
        myDigits = [int(x) for x in list(str(score))]
        width = 0
        for digit in myDigits:
            width+=GAME_SPRITES['numbers'][digit].get_width() 
        digitXOffset = (SCREENWIDTH-width)/2 #to get the middle position for blitting score
        for digit in myDigits:
            SCREEN.blit(GAME_SPRITES['numbers'][digit], (digitXOffset,SCREENHEIGHT*0.12))
            digitXOffset += GAME_SPRITES['numbers'][digit].get_width() 
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def isCollide(fishx, fishy, upperPipes, lowerPipes):
    pipeHeight = GAME_SPRITES['pipe'][0].get_height()
    #if the fish hits the ground or touches the above screen, collision will occur and game will end
    if fishy > GROUNDY-30 or fishy<0:  
        return True
    
    #else if the bird hits any upperpipe or lowerpipe, collison occurs and game ends
    for pipe in upperPipes:
        if (fishy<pipeHeight+pipe['y']) and ((abs(fishx-pipe['x']))<GAME_SPRITES['fish'].get_width()):
            return True
    for pipe in lowerPipes:
        if (fishy + GAME_SPRITES['fish'].get_height() > pipe['y']) and ((abs(fishx-pipe['x']))<GAME_SPRITES['fish'].get_width()):
            return True
    else:
        return False

def getRandompipe():
    """
    Generate positions of two pipes(one bottom straight and one top rotated ) for blitting on the screen
    """
    pipeHeight = GAME_SPRITES['pipe'][0].get_height()
    offset = SCREENHEIGHT/3
    #For lower pipe.We are adding offset since we need atleast offset distance from above
    y2 = offset + random.randrange(0, int(SCREENHEIGHT - GAME_SPRITES['base'].get_height()  - 1.2 *offset))
    pipeX = SCREENWIDTH + 10
    #for upper pipe
    y1 = pipeHeight - y2 + offset*0.75
    pipe = [
        {'x': pipeX, 'y': -y1}, #we are taking y1 as negative since it is for the upper pipe
        {'x': pipeX, 'y': y2} #lower Pipe
    ]
    return pipe


#starting our game from here
if __name__ == "__main__":  
    pygame.init() #initializing all imported pygame modules
    FPSCLOCK = pygame.time.Clock() #to control our FPS
    pygame.display.set_caption('Make Way For Nemo by Shubhangi')
    GAME_SPRITES['numbers'] = (
    pygame.image.load('Gallery/Sprites/0.png').convert_alpha(),
    pygame.image.load('Gallery/Sprites/1.png').convert_alpha(),
    pygame.image.load('Gallery/Sprites/2.png').convert_alpha(),
    pygame.image.load('Gallery/Sprites/3.png').convert_alpha(),
    pygame.image.load('Gallery/Sprites/4.png').convert_alpha(),
    pygame.image.load('Gallery/Sprites/5.png').convert_alpha(),
    pygame.image.load('Gallery/Sprites/6.png').convert_alpha(),
    pygame.image.load('Gallery/Sprites/7.png').convert_alpha(),
    pygame.image.load('Gallery/Sprites/8.png').convert_alpha(),
    pygame.image.load('Gallery/Sprites/9.png').convert_alpha()
    )

    #giving values to GAME_SPRITES dictionary keys
    GAME_SPRITES['message'] = pygame.image.load('Gallery/Sprites/message.png').convert_alpha()
    GAME_SPRITES['base'] = pygame.image.load('Gallery/Sprites/base.png').convert_alpha()
    GAME_SPRITES['pipe'] =(pygame.transform.rotate(pygame.image.load( PIPE).convert_alpha(), 180), 
    pygame.image.load(PIPE).convert_alpha()
    )
    GAME_SPRITES['background'] = pygame.image.load(BACKGROUND).convert()
    GAME_SPRITES['fish'] = pygame.image.load(PLAYER).convert_alpha()
    GAME_SPRITES['gameover'] = pygame.image.load(GAMEOVER).convert_alpha()



    #game sounds
    GAME_SOUNDS['die'] = pygame.mixer.Sound('Gallery/audio/die.wav')
    GAME_SOUNDS['hit'] = pygame.mixer.Sound('Gallery/audio/hit.wav')
    GAME_SOUNDS['point'] = pygame.mixer.Sound('Gallery/audio/point.wav')
    GAME_SOUNDS['swoosh'] = pygame.mixer.Sound('Gallery/audio/swoosh.wav')
    GAME_SOUNDS['wing'] = pygame.mixer.Sound('Gallery/audio/wing.wav')

    while True:
        welcomeScreen()  #displays the welcome screen until any key is pressed
        playGame() #This is the main function of the game 





