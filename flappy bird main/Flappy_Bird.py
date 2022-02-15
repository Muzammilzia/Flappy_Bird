# importing the required modules(pygame, sys, random....):
import pygame, sys
import random
pygame.init()

goldfile = open("currencymemory.txt", "r")
currency = int(goldfile.read())
goldfile.close()
#Initializing Block for variables(all variables required in game):
FPS = 100
width = 288
height = 512
score = 0
x = 0
y = 0
speed = 0
x_base = 288
x_pipe = 288
y_pipe = random.choice([202, -10, -50, 242]) #4 random hieghts for pipe 
y_coin = random.choice([80, 35, 273, 315])
x_coin = x_pipe+100
i = 0
angle = 45

#Initializing pygame window, setting Caption and favicon icon:
screen = pygame.display.set_mode((width,height))
pygame.display.set_caption("Flappy Bird")
favicon = pygame.image.load(".\\FlappyBird\\favicon.ico").convert()
pygame.display.set_icon(favicon)

#Clock Object to control framerate in our game:
fpsClock = pygame.time.Clock()

#initializing font and loading all required images:
font = pygame.font.Font('freesansbold.ttf',20)
home_img = pygame.image.load(".\\FlappyBird\\sprites\\flappy_home.jpg").convert()
bird_up = pygame.image.load(".\\FlappyBird\\sprites\\yellowbird-upflap.png").convert()
bird_mid = pygame.image.load(".\\FlappyBird\\sprites\\yellowbird-midflap.png").convert()
bird_down = pygame.image.load(".\\FlappyBird\\sprites\\yellowbird-downflap.png").convert()
background = pygame.image.load(".\\FlappyBird\\sprites\\background-night.png").convert()
base = pygame.image.load(".\\FlappyBird\\sprites\\base.png").convert()
pipe_green = pygame.image.load(".\\FlappyBird\\sprites\\pipe-green.png").convert()
pipe_red = pygame.image.load(".\\FlappyBird\\sprites\\pipe-red.png").convert()
gameOver = pygame.image.load(".\\FlappyBird\\sprites\\gameover.png").convert()
coin_img = pygame.image.load(".\\FlappyBird\\sprites\\coin.png").convert()

#Scaling down the home page image because it is too large:
home = pygame.transform.scale(home_img, (288, 512))
coin = pygame.transform.scale(coin_img, (50, 50))
#lists of pipe and bird images
pipe_list = [pipe_green, pipe_red]
bird_list = [bird_up, bird_mid, bird_down]

#taking bird_up to start (bird_list[0] = bird_up):
bird = bird_list[0]

#choosing random colour pipe from list:
pipe = random.choice(pipe_list)

#Inverting the pipe image if pipe is coming from top side(if y_pipe <= 0):
if y_pipe <= 0:
    pipe = pygame.transform.rotate(pipe, 180)

#startup function containing home page and waiting for user to press start(space button):
def startup():
    start = False
    while not start:
        home_rect = home.get_rect(center = (144, 256))
        screen.blit(home, (home_rect))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    start = True
#startup call:        
startup()

#infinte Game Loop:
while True:
    #speed for bird which will work as gravity for example it will accelerate bird downwards(also up):
    speed = speed + 0.3
    
    #Initializing text(score) as an image: 
    text = font.render("{}".format(score), True, (255, 255, 255))
    textRect = text.get_rect(center = (144, 30))

    text1 = font.render("$ = {}".format(currency), True, (255, 255, 255))
    textRect1 = text1.get_rect(center = (250, 30))

    #bliting all images on pygame window(creating graphics):
    screen.blit(background,(x_base-288,0))
    screen.blit(background,(x_base,0))
    screen.blit(background,(x_base+288,0))
    screen.blit(pipe,(x_pipe,y_pipe))
    screen.blit(base,(x_base-288,400))
    screen.blit(base,(x_base,400))
    screen.blit(base,(x_base+288,400))
    screen.blit(bird,(x,y))
    screen.blit(text, textRect)
    screen.blit(text1, textRect1)
    screen.blit(coin, (x_coin,y_coin))

    #changing bird pic(up, ,mid, down flaps) every little while to give bird a flying look:
    if i <= 5:
        bird = bird_list[0]
    if i <= 10 and i >= 5:
        bird = bird_list[1]
    if i <= 15and i >= 10:
        bird = bird_list[2]

    #re-initializng images at initial points to make infinite background and pipes:
    if x_base < -288:
        x_base = 288
    if x_pipe < -52:
        x_pipe = 288
        pipe = random.choice(pipe_list) #new random pipe every time
        y_pipe = random.choice([222, -45, -85, 262]) #random heights
        if y_pipe <= 0:
            pipe = pygame.transform.rotate(pipe, 180) #inverting pipe
    if x_coin < -50:
        x_coin = x_pipe + 100
        if (y_pipe == 222 or y_pipe == 262):
            y_coin = random.choice([273, 315])
        if (y_pipe == -45 or y_pipe == -85):
            y_coin = random.choice([80, 35])
        
    x_pipe = x_pipe - 1
    x_base = x_base - 1
    x_coin = x_coin - 1

    #bird and pipe rectangles
    pipe_rect = pipe.get_rect(topleft = (x_pipe, y_pipe))
    bird_rect = bird.get_rect(topleft = (x, y))
    coin_rect = coin.get_rect(topleft = (x_coin, y_coin))
    #keeping track of user's input(keypress) and exit from game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                speed = -9 #to accelrate bird a upward
                angle = 45 
                bird = pygame.transform.rotate(bird, angle) # to give bird a look of facing up 

    #bird speed
    if y >= 0:
        y = y + speed
    if y < 0:
        y = y - speed

    i = i + 1
    if angle >= -45:
        angle += - 4
    if i >= 16:
        i = 0

    #to update window every iteration    
    pygame.display.update() 
    fpsClock.tick(FPS)  # sleep time
    bird = pygame.transform.rotate(bird, angle)# to give bird a look of facing down

    #Condition to check if bird pass through pipe without colliding:
    if ((bird_rect.left == pipe_rect.left) and ((bird_rect.top <= pipe_rect.top or bird_rect.top >= pipe_rect.bottom) or  (bird_rect.bottom <= pipe_rect.top and bird_rect.bottom >= pipe_rect.bottom))):
        score += 1


    if ((((bird_rect.left >= coin_rect.left and  bird_rect.left <= coin_rect.right) or(bird_rect.right >= coin_rect.left and  bird_rect.right <= coin_rect.right)) and ((bird_rect.top >= coin_rect.top and bird_rect.top <= coin_rect.bottom) or  (bird_rect.bottom >= coin_rect.top and bird_rect.bottom <= coin_rect.bottom)))):
        currency += 1
        x_coin = x_pipe+100
        if (y_pipe == 222 or y_pipe == 262):
            y_coin = random.choice([273, 315])
        if (y_pipe == -45 or y_pipe == -85):
            y_coin = random.choice([80, 35])
        
    #Condition to check if bird collides up or down or with pipe:
    if y >= 512 or (((bird_rect.left >= pipe_rect.left and  bird_rect.left <= pipe_rect.right) or(bird_rect.right >= pipe_rect.left and  bird_rect.right <= pipe_rect.right)) and ((bird_rect.top >= pipe_rect.top and bird_rect.top <= pipe_rect.bottom) or  (bird_rect.bottom >= pipe_rect.top and bird_rect.bottom <= pipe_rect.bottom))):
        speed = 0 
        flag = True
        k = angle

        scoresfile = open("score.txt","r")
        scorelist = scoresfile.read().split("\n")
        scoresfile.close()
        scorelist.pop()
        scorelist = map(int, scorelist)
        scorelist = list(scorelist)
        scorelist.append(score)
        scorelist.sort(reverse = True)
        scorelist.pop()
        highscore = scorelist[0]
        scoresfile = open("score.txt","w")
        for i in scorelist:
            scoresfile.write("{}\n".format(i))
        scoresfile.close()
        
        #loop to stop the game(Game Over):
        while flag:
            screen.blit(background,(x_base-288,0))
            screen.blit(background,(x_base,0))
            screen.blit(background,(x_base+288,0))
            screen.blit(pipe,(x_pipe,y_pipe))
            screen.blit(base,(x_base-288,400))
            screen.blit(base,(x_base,400))
            screen.blit(base,(x_base+288,400))
            screen.blit(gameOver,(50,440))
            screen.blit(text, textRect)
            screen.blit(text1, textRect1)
            screen.blit(coin, (x_coin,y_coin))
            text_try_again = font.render("Try Again? Pres H key", True, (255, 255, 255))
            text_try_again_Rect = text_try_again.get_rect(center = (144, 256))
            screen.blit(text_try_again,text_try_again_Rect)
            text_highscore = font.render("All Time High {}".format(highscore), True, (255, 255, 255))
            text_highscore_Rect = text_highscore.get_rect(center = (144, 300))
            screen.blit(text_highscore,text_highscore_Rect)
            speed = speed + 0.3

            #to rotate bird upside down:
            if k <= 180:
                rotated_bird= pygame.transform.rotate(bird, k)
                k = k+40
            if y <= 470:
                y = y + speed
            screen.blit(rotated_bird,(x,y))
            pygame.display.update()
            fpsClock.tick(FPS)

            #to get user input to quit or restart:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    goldfile = open("currencymemory.txt","w")
                    goldfile.write("{}".format(currency))
                    goldfile.close()
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_h:
                        flag = False  
                        x = 0      #reinitializing variables to start game again:
                        y = 0
                        x_pipe = 288
                        speed = 0
                        score = 0
                        startup()  #calling startup function again








