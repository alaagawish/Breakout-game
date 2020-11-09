import sys
import pygame
##initialize width ,height  of screen,block box and the radius of the ball
screenWidth, screenHeight = 640, 480
boxWidth, boxHeight = 40, 20
plateWidth, plateHeight = 100, 20
radiusofBall = 5


yplate = screenHeight - plateHeight - 10
xplate = screenWidth - plateWidth
Xballmax = screenWidth - 2*radiusofBall
Yballmax = screenHeight - 2*radiusofBall

##some colors
black = (0, 0, 0)
white = (255, 255, 255)
darkblue = (36, 90, 190)
blue = (0, 176, 240)
c1 = ( 255, 0, 0)

#levels to check player wants hard or easy level
Hard='h'
Easy='e'

##define states
StateStart = 0
StatePlaying = 1
StateWon = 2
StateGameOver = 3


class Plate:

    def __init__(self,level):
        pygame.init()
        self.level=level  ##char which refers to level
        self.screen = pygame.display.set_mode((screenWidth, screenHeight))  ##size of window
        pygame.display.set_caption("Breakout game") ##name of game window

        self.clock = pygame.time.Clock()

        self.font = pygame.font.Font(None, 35)

        self.newgame(level)

    def newgame(self,level):
        self.hearts = 3
        self.score = 0
        self.state = 0
        self.level=level
##position of plate and ball at the beganining
        self.plate = pygame.Rect(270, yplate, plateWidth, plateHeight)
        self.ball = pygame.Rect(270, yplate - 2*radiusofBall, 2*radiusofBall, 2*radiusofBall)

## check the level if hard >>ball is fast
        if (self.level == Hard):
            self.ballspeed = [10, -10]
        elif self.level == Easy:
            self.ballspeed = [5, -5]

        self.createbox()

    def createbox(self):
        m = 35
        ##create shape of blocks , this is a design for 55 blocks
        self.box = []
        for i in range(5):
            l = 35
            for j in range(11):
                self.box.append(pygame.Rect(l, m, boxWidth, boxHeight))
                l += boxWidth + 10
            m += boxHeight + 5
##color of blocks on the screen
    def designbox(self):
        for b in self.box:
            pygame.draw.rect(self.screen, darkblue, b)
##check the button that player pressed (space or enter ,left ,right
    def check_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.plate.left -= 5
            if self.plate.left < 0:
                self.plate.left = 0

        if keys[pygame.K_RIGHT]:
            self.plate.left += 5
            if self.plate.left > xplate:
                self.plate.left = xplate


        if keys[pygame.K_SPACE] and self.state == StateStart:
            if (self.level==Hard):
                self.ballspeed = [10, -10]
            elif self.level==Easy:
                self.ballspeed = [5, -5]
            self.state = StatePlaying
        elif keys[pygame.K_RETURN] and (self.state == StateGameOver or self.state == StateWon):
            self.newgame(self.level)
## moving of the ball
    def move_ball(self):
        self.ball.left += self.ballspeed[0]
        self.ball.top += self.ballspeed[1]

        if self.ball.left <= 0:
            self.ball.left = 0
            self.ballspeed[0] = -self.ballspeed[0]
        elif self.ball.left >= Xballmax:
            self.ball.left = Xballmax
            self.ballspeed[0] = -self.ballspeed[0]

        if self.ball.top < 0:
            self.ball.top = 0
            self.ballspeed[1] = -self.ballspeed[1]
        elif self.ball.top >= Yballmax:
            self.ball.top = Yballmax
            self.ballspeed[1] = -self.ballspeed[1]
## determine score when ball clashes the blocks and remove these blocks
    def handle_collisions(self):
        for b in self.box:
            if self.ball.colliderect(b):
                self.score += 1
                if self.score<55:
                    self.ballspeed[1] = -self.ballspeed[1]
                    self.box.remove(b)
                    break
                else:
                    self.state=StateWon
                    break
##if ball didnt toouch any block
        if len(self.box) == 0:
            self.state = StatePlaying
##if the ball touched the floor >>heart-=1
        if self.ball.colliderect(self.plate):
            self.ball.top = yplate - 2*radiusofBall
            self.ballspeed[1] = -self.ballspeed[1]
        elif self.ball.top > self.plate.top:
            self.hearts -= 1
##if hearts==0 if means u finished all tries else start new try
            if self.hearts > 0:
                self.state = StateStart
            else:
                self.state = StateGameOver

## the position and appearance of score and no.of tries
    def showstats(self):
        if self.font:

            text = self.font.render("your score: " + str(self.score),False,c1)
            text2=self.font.render("hearts: " + str(self.hearts),False,c1)
            self.screen.blit(text, (0, 5))
            self.screen.blit(text2, (500, 5))
##position of the message on the screen
    def show_message(self, message):
        if self.font:
            size = self.font.size(message)
            font_surface = self.font.render(message, False, c1)
            x = (screenWidth - size[0]) / 2
            y = (screenHeight - size[1]) / 2
            self.screen.blit(font_surface, (x, y))

    def run(self):
        while 1:
            ##if player clicked quit close the game
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            self.clock.tick(50) ##means that while loop runs 50 times per second
            self.screen.fill(black) ##color of window
            self.check_input()
##check which message should display depending on the state

            if self.state == StatePlaying:
                self.move_ball()
                self.handle_collisions()
            elif self.state == StateStart:
                self.ball.left = self.plate.left + self.plate.width / 2
                self.ball.top = self.plate.top - self.ball.height
                self.show_message("Enter Space to start")
            elif self.state == StateGameOver:
                self.show_message("GAME OVER")
            elif self.state == StateWon:
                self.show_message("Great")

            self.designbox()
##color of ball  and plate
            pygame.draw.rect(self.screen, darkblue, self.plate)
            pygame.draw.circle(self.screen, white, (self.ball.left + radiusofBall, self.ball.top + radiusofBall), radiusofBall)
            self.showstats()
            pygame.display.flip()

##let the player choose hard level or easy one by writing h or e
ch=input("enter h for hard level and e for easy one\n")
Plate(ch).run()